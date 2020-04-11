import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import unittest

from scipy import stats
from permute.core import two_sample

from Assignment2.assignment2 import get_alameda_county_points
from Assignment3.assignment3 import filter_ranson_criteria, clean_data, get_weather_data
from Assignment5.assignment5 import *

class TestAssignment5(unittest.TestCase):

    def test_get_data(self): # Test whether we get the ranson's filtered dataframe.
        df = get_data()
        col_name = ['ID', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'STATE',
       'NAME']
        self.assertTrue(set(df.columns).issuperset(col_name))
        self.assertIsInstance(df,pd.DataFrame)

    def test_get_city_data(self):
        berkeley = get_city_data(get_data(), 'USC00040693')
        livermore = get_city_data(get_data(), 'USC00044997')

        self.assertEqual(set(berkeley['ELEMENT']), {'TMAX'})
        self.assertEqual(set(livermore['ELEMENT']), {'TMAX'})
        self.assertTrue(np.all(berkeley['ID'] == 'USC00040693'))
        self.assertTrue(np.all(livermore['ID'] == 'USC00044997'))

    def test_convert_Fahrenheit(self):
        berkeley = convert_to_fahrenheit(get_city_data(get_data(), 'USC00040693'))
        livermore = convert_to_fahrenheit(get_city_data(get_data(),'USC00044997'))

        d = {'DATA VALUE': [10, 20, 30, 40, 50, 60,70,80,90,100]}
        examples = pd.DataFrame(data = d)
        examples = convert_to_fahrenheit(examples)
        expected = [33.8,35.6,37.4,39.2,41,42.8,44.6,46.4,48.2,50]
        self.assertTrue(set(examples['FAHRENHEIT']) == set(expected))
        self.assertTrue(all(isinstance(x,float) for x in berkeley['FAHRENHEIT']))
        self.assertTrue(all(isinstance(x,float) for x in livermore['FAHRENHEIT']))


    def test_bin(self):
        berkeley_bins = bin_data(convert_to_fahrenheit(get_city_data(get_data(), 'USC00040693')))
        livermore_bins = bin_data(convert_to_fahrenheit(get_city_data(get_data(),'USC00044997')))
        expected_berk_bins = pd.interval_range(start=30, end = 100, periods=7).tolist()
        expected_liver_bins = pd.interval_range(start = 20, end = 100, periods = 8).tolist()
        self.assertLessEqual(len(set(berkeley_bins.columns)),10)
        self.assertLessEqual(len(set(livermore_bins.columns)),10)
        self.assertTrue(list(berkeley_bins.columns.values), expected_berk_bins)
        self.assertTrue(list(livermore_bins.columns.values), expected_liver_bins)

        self.assertTrue(1980 <= x <= 2009 for x in list(set(berkeley_bins.index.get_level_values(0))))
        self.assertTrue(1 <= x <= 12 for x in list(set(berkeley_bins.index.get_level_values(1))))
        self.assertTrue(1980 <= x <= 2009 for x in list(set(livermore_bins.index.get_level_values(0))))
        self.assertTrue(1 <= x <= 12 for x in list(set(livermore_bins.index.get_level_values(1))))


    def test_intersection(self):
        berkeley_intersected, livermore_intersected = get_intersected(convert_to_fahrenheit(get_city_data(get_data(), 'USC00040693')),convert_to_fahrenheit(get_city_data(get_data(),'USC00044997')))

        self.assertEqual(len(berkeley_intersected),len(livermore_intersected))
        self.assertEqual(set(berkeley_intersected['date']),set(livermore_intersected['date']))

    def test_stratify(self):
        berkeley_intersected, livermore_intersected = get_intersected(convert_to_fahrenheit(get_city_data(get_data(), 'USC00040693')),convert_to_fahrenheit(get_city_data(get_data(),'USC00044997')))
        berkeley_stratified = stratify(berkeley_intersected)
        livermore_stratified = stratify(livermore_intersected)
        self.assertEqual(len(berkeley_stratified),len(livermore_stratified))
        for i in range(len(berkeley_stratified)):
            self.assertTrue(len(berkeley_stratified[i]) == len(livermore_stratified[i]))
            self.assertSetEqual(set(berkeley_stratified[i]['date']),set(livermore_stratified[i]['date']))

    def test_permutation_test(self):
        berkeley_intersected, livermore_intersected = get_intersected(convert_to_fahrenheit(get_city_data(get_data(), 'USC00040693')),convert_to_fahrenheit(get_city_data(get_data(),'USC00044997')))
        berkeley_stratified = stratify(berkeley_intersected)
        livermore_stratified = stratify(livermore_intersected)
        self.assertTrue(0<= permutation_test(berkeley_stratified, livermore_stratified) <= 1)

    def test_assignment5(self):
        main()

    if __name__ == "__main__":
        unittest.main()
