import numpy as np
import pandas as pd
from Assignment2.assignment2 import get_stations, get_alameda_county_points, get_station_weights
from Assignment1.weighted_avg import calc_inv_weighted_avg

def get_weather_data(points = get_alameda_county_points(), max_distance = 10):
    """Gets weather data for a given set of grid points

    args:
        points: list of grid points (lat, lon) (default alameda county grid)
        max_distance: max distance to search around each grid point (default 10)
    return:
        pd.DataFrame: dataframe with data from weather and stations
    """

    # load data from csv
    stations = pd.DataFrame(get_stations(points, max_distance))
    weather = pd.read_csv('Assignment3/data/weather_data_ca.csv')

    # merge data on the ID
    merged = stations.merge(weather, on='ID', how='inner')
    return merged

def clean_data(df):
    """ Cleans data from original dataframe

    args:
        df: dataframe of data
    return:
        df: cleaned dataframe
    """

    # clean the date data
    df['date'] = pd.to_datetime(df['YEARMONTHDAY'].astype(str), format='%Y%m%d')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day

    # convert to fahrenheit
    df.ix[df['ELEMENT'] != 'PRCP', 'DATA VALUE'] = ((df.ix[df['ELEMENT'] != 'PRCP', 'DATA VALUE'] / 10) * 1.8) + 32
    return df

def filter_ranson_criteria(df):
    """Filters the rows based on Ranson's criteria which states
    to only include year, station, element combinations that have
    more than 100 points
    
    args:
        df: dataframe of data
    return:
        df: dataframe of data with only ranson criteria satisfying rows
    """
    
    yearly_count = df.groupby(['NAME','year', 'ELEMENT']).count()
    new_df = yearly_count.reset_index()
    new_df = new_df[new_df['ID'] >= 100][['NAME', 'year', 'ELEMENT']]
    return new_df.merge(df, how='inner', on=['NAME', 'year', 'ELEMENT'])

def station_intersection(station1_name, station2_name, df):
    """Gets the intersection of rows between station1 and station2

    args:
        station1_name: name of station 1
        station2_name: name of station 2
        df: dataframe of data
    return:
        int: length of the merged data
        df: dataframe of intersected data
    """
    
    # find the days that the stations intersect
    station1_rows = df[df['NAME'] == station1_name]
    station2_rows = df[df['NAME'] == station2_name]
    merged = station1_rows.merge(station2_rows, on='date', how='inner')
    return len(merged['date']), merged


def bias_correction(df):
    """Adjusts the data by doing a bias correction

    args:
        df: dataframe to run bias correction on
    return:
        df: dataframe with bias corrected data
    """

    stations = df['NAME'].unique()

    # initialize intercepts
    intercepts = [0 for _ in range(len(stations))]
    old_intercepts = intercepts[:]
    count = 0

    # iterate till convergence
    while True:

        # pick random point in reference
        reference_idx = np.random.randint(0, len(stations))
        reference_station = stations[reference_idx]

        # iterate through all stations to update intercept
        for station_idx in range(len(stations)):
            station = stations[station_idx]

            # get intersection of stations
            n, k = station_intersection(reference_station, station, df)

            # calculate sum for all intersected rows
            curr_sum = 0.0
            for _, row in k.iterrows():
                station1_data = row['DATA VALUE_x']
                station2_data = row['DATA VALUE_y']
                curr_sum += station1_data + intercepts[reference_idx] - (station2_data + intercepts[station_idx])

            # update the stations intercept
            if n != 0:
                intercepts[station_idx] = intercepts[station_idx] + curr_sum / n

        if count % (2 * len(stations)) == 0 and count != 0:
            # check if it converges by calculating loss
            loss = np.sum((np.array(intercepts) - np.array(old_intercepts)) ** 2)
            old_intercepts = intercepts[:]
            # set convergence criteria
            if loss < 0.000001:
                break
        count += 1

    # map station name to intercept value
    bias = dict(zip(stations, intercepts))

    # get latitude and longitude of stations
    lat_lon = []
    for station in stations:
        data = df[df['NAME'] == station].iloc[0]
        latitude, longitude = data['LATITUDE'], data['LONGITUDE']
        lat_lon.append((latitude, longitude))

    # get station weights
    weights = np.array(calc_inv_weighted_avg(get_alameda_county_points(), lat_lon))
    weights = weights * np.array(intercepts) / np.sum(weights)

    # calculate C
    C = dict(zip(stations, weights))

    # apply formula to calculate adjusted data
    df['adjusted_data'] = df.apply(lambda x: x['DATA VALUE'] + bias[x['NAME']] - C[x['NAME']], axis = 1)

    return df

def main(elements=['TMAX', 'TMIN'], points = get_alameda_county_points()):
    """Bins adjusted data for each element. Binning idea received
    by: https://stackoverflow.com/questions/34317149/pandas-groupby-with-bin-counts
    
    args:
        elements: specifies elements to calculate data for (default ['TMAX', 'TMIN'])
    return:
        list: returns list of binned data as dataframe
    """

    df = filter_ranson_criteria(clean_data(get_weather_data(points)))
    result = []
    bin_map = {
        'PRCP' : (0, 4, 14, 29, 2000), 
        'TMAX' : range(0, 100, 10),
        'TMIN' : range(0, 100, 10)
    }
    for element in elements:
        filtered = df[df['ELEMENT'] == element]
        corrected = bias_correction(filtered)

        # average data from the same day
        grouped = corrected.groupby(['year', 'month', 'day']).aggregate({'adjusted_data' : np.mean}).reset_index()

        # bin the data
        final = grouped.groupby(['year', 'month', pd.cut(grouped['adjusted_data'], bin_map[element], right=True)]).size().unstack().fillna(0.0)
        result.append(final)
    return result

if __name__ == '__main__':
    print(main())
