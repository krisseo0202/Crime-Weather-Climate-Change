import numpy as np
import pandas as pd
import statsmodels.api as sm
import pickle
import os

from Assignment3.assignment3 import main
from Assignment4.assignment4 import divide_alameda_points

classify_zip = {
    'west': [94539,94552,94544,94536,94537,94538,94568,94550,94566,94551,94612,94501,94706,94704,94608,94544,94560,94607,94611,94587,94546,94542,94720,94804,94619,94623,94541,94703,94577],
    'east': [94568,94566,94586,94536,94537,94538,94545,94130,94578,94708,94552,94618,94555,94506]
}

def get_corrected_weather_data(load_pickle=False):
    """ Get corrected weather data for the areas of interest

    return
        DataFrame: df from west Alameda
        DataFrame: df from east Alameda
        DataFrame: df from Alameda
    """
    w_pts, e_pts = divide_alameda_points()

    alameda = pickle.load(open('Assignment6/alameda_weather', 'rb'))
    east_weather = pickle.load(open('Assignment6/east_weather_file', 'rb'))
    west_weather = pickle.load(open('Assignment6/west_weather_file', 'rb'))

    # load from assignment 3 function
    if not load_pickle:
        alameda = main(elements=['TMAX', 'PRCP'])
        east_weather = main(points = e_pts, elements=['TMAX', 'PRCP'])
        west_weather = main(points = w_pts, elements=['TMAX', 'PRCP'])
    return west_weather, east_weather, alameda

def get_crime_data(load_pickle=False):
    """ Creates a DataFrame of crime data for Alameda County from 1980 to 2009
        Pickle this dataframe for future use

    return:
        DataFrame: Crime data DF
    """
    if load_pickle:
        return pickle.load(open('Assignment6/df_1980_2009.pkl', 'rb'))

    # get list of dta files for 1980 - 2009 data
    crime_data_path = "Assignment6/data/ucr_offenses_known_monthly_1960_2016_dta/"
    dta_files = [f for f in os.listdir(crime_data_path) if f[-4:] == '.dta']
    dta_files_80_09 = [f for f in dta_files if int(f[-8:-4]) >= 1980 and int(f[-8:-4]) <= 2009]

    # 1980 - 2009 crime data
    df_list = []
    for f in dta_files_80_09:
        df = pd.read_stata(crime_data_path + f)
        # get only Alameda County data point
        df = df[(df['fips_state_code'] == '06') & (df['fips_county_code'] == '001')]
        df_list.append(df)
    df_80_09 = pd.concat(df_list)
    df_80_09.to_pickle("Assignment6/data/df_1980_2009.pkl")

    return df_80_09

def clean_crime_data(alameda_crime):
    """ Take crime data, clean it, and divide it into the areas of interest

    args:
        DataFrame: crime data DF
    return:
        DataFrame: df from west Alameda
        DataFrame: df from east Alameda
        DataFrame: df from Alameda
    """
    # get sum of crime incidences
    alameda_crime['total_crime'] = alameda_crime.filter(regex='_total').sum(axis=1)
    east = alameda_crime[alameda_crime['zip_code'].isin(classify_zip['east'])]
    west = alameda_crime[alameda_crime['zip_code'].isin(classify_zip['west'])]

    # get cleaned data
    east_cleaned = east.groupby(['year', 'month']).sum()[['total_crime']].reset_index()
    west_cleaned = west.groupby(['year', 'month']).sum()[['total_crime']].reset_index()
    alameda_cleaned = alameda_crime.groupby(['year', 'month']).sum()[['total_crime']].reset_index()

    # change month name to month number
    east_cleaned['month'] = pd.to_datetime(east_cleaned['month'], format='%B').dt.month
    west_cleaned['month'] = pd.to_datetime(west_cleaned['month'], format='%B').dt.month
    alameda_cleaned['month'] = pd.to_datetime(alameda_cleaned['month'], format='%B').dt.month

    return west_cleaned, east_cleaned, alameda_cleaned

def get_data_matrix(weather, crime):
    """ Gets the regression data matrix from the weather and crime data

    args:
        weather: weather DataFrame
        crime: crime DataFrame
    return:
        ndarray: design matrix
        ndarray: dependent variable
    """
    # merge temperature with precipitation
    a_temp, a_prcp = weather
    a_temp.columns = a_temp.columns.astype(str)
    a_prcp.columns = a_prcp.columns.astype(str)
    merged_weather = a_temp.join(a_prcp)

    # merge crime with weather
    merged = pd.merge(crime, merged_weather.reset_index(), on=['year', 'month'], how='inner').fillna(0.0)
    merged_data = merged.sort_values(by=['year', 'month']).reset_index(drop=True).drop(['year', 'month'], axis=1)

    # get x and y values
    y = merged_data['total_crime']
    x = merged_data.drop('total_crime', axis=1).values

    return x, y

def get_model(x, y):
    """ Gets fitted GLM Poisson regression from x and y

    args:
        x: design matrix
        y: dependent variable
    return:
        GLM: model
    """
    return sm.GLM(y, x, family=sm.families.Poisson()).fit()

def run_assignment6():
    """ Run assignment 6 to get the models

    return:
        GLM: west
        GLM: east
        GLM: alameda
    """
    west, east, alameda = get_corrected_weather_data(load_pickle=True)
    crime_data = get_crime_data(load_pickle=True)
    west_crime, east_crime, alameda_crime = clean_crime_data(crime_data)

    west_x, west_y = get_data_matrix(west, west_crime)
    east_x, east_y = get_data_matrix(east, east_crime)
    alameda_x, alameda_y = get_data_matrix(alameda, alameda_crime)

    return get_model(west_x, west_y).summary(), get_model(east_x, east_y).summary(), get_model(alameda_x, alameda_y).summary()

if __name__ == '__main__':
    print(run_assignment6())
