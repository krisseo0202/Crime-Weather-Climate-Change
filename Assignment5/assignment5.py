import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy import stats
from permute.core import two_sample

from Assignment2.assignment2 import get_alameda_county_points
from Assignment3.assignment3 import filter_ranson_criteria, clean_data, get_weather_data


def get_data():
    """ Return DataFrame containing weather data in Alameda county based on Ranson's criteria
    return:
        DataFrame: weather data
    """
    points = get_alameda_county_points()
    return filter_ranson_criteria(clean_data(get_weather_data(points)))

def get_city_data(df, id, element='TMAX'):
    """ Return a DataFrame that is filtered by element and ID

    return:
        DataFrame: weather data
    """
    hcn_city = df[df['ID'] == id]
    return hcn_city[hcn_city['ELEMENT'] == element]

def convert_to_fahrenheit(df):
    """ Return a DataFrame that converts DATA VALUE to FAHRENHEIT

    return:
        DataFrame: weather data
    """
    df['FAHRENHEIT'] = ((df['DATA VALUE'] / 10) * 1.8) + 32
    return df

def bin_data(df):
    """ Return a DataFrame that groups the data by year and month and bins FAHRENHEIT

    return:
        DataFrame: binned weather data
    """
    grouped_df = df.groupby(['year', 'month', pd.cut(df['FAHRENHEIT'], range(0, 110, 10))])
    return grouped_df.size().unstack().sort_index(axis = 1).fillna(0.0)

def get_intersected(df1, df2, intersect_on='date'):
    """ Returns two DataFrames that include only rows which have the same intersect_on values

    return:
        DataFrame: filtered weather data
        DataFrame: filtered weather data
    """
    intersection = np.intersect1d(df1[intersect_on], df2[intersect_on])
    return df1[df1[intersect_on].isin(intersection)], df2[df2[intersect_on].isin(intersection)]

def stratify(df, by=['year', 'month']):
    """ Returns a list of DataFrame that are the groups from the by criteria

    return:
        List[DataFrame]: grouped weather data
    """
    df_grouped = df.groupby(by)
    return [df_grouped.get_group(group) for group in df_grouped.groups]

def permutation_test(a, b):
    """ Returns p-value for a two-sided two sample permutation test using Fisher combining function

    return:
        Double: p-value of the chi squared statistic
    """
    min_p = 10 ** -20
    fisher_statistic = 0.0

    for stratum in range(len(a)):
        p, _ = two_sample(a[stratum]['FAHRENHEIT'], b[stratum]['FAHRENHEIT'], alternative='two-sided')
        print('Finished stratum %d got p-value %f' % (stratum, p))
        fisher_statistic += -2 * np.log(max(p, min_p))

    return 1 - stats.chi2.cdf(fisher_statistic, 2 * len(a))

def main():
    # Filtered dataframe meeting Ranson's criteria
    df = get_data()
    # get data for berkeley and livermore
    berkeley = get_city_data(df, 'USC00040693')
    livermore = get_city_data(df, 'USC00044997')
    # add fahrenheit column
    berkeley = convert_to_fahrenheit(berkeley)
    livermore = convert_to_fahrenheit(livermore)

    # bin data
    berkeley_bins = bin_data(berkeley)
    livermore_bins = bin_data(livermore)
    # select only dates that exist in both cities
    berkeley_intersected, livermore_intersected = get_intersected(berkeley, livermore)
    # stratify by
    berkeley_stratified = stratify(berkeley_intersected)
    livermore_stratified = stratify(livermore_intersected)
    # H0: Berkeley and Livermore have the same weather.
    # H1: Berkeley and Livermore have different weather.
    # get p-value from permutation test using fisher combining function
    fisher_statistic = 0.0
    p = permutation_test(berkeley_stratified, livermore_stratified)

    print('P-value under H0: Berkeley and Livermore have the same weather is %f' % p)
    return p


if __name__ == '__main__':
    print(main())
