from Assignment1.weighted_avg import *
from Assignment3.assignment3 import *
import unittest
import numpy as np
import reverse_geocoder as rg
import pandas as pd

class TestGetWeatherData(unittest.TestCase):
    #Tests if we get the dataframe we want and merge.

    def test_weather(self):
        merged_name = set(get_weather_data().columns)
        expected_name = set(['Unnamed: 0_x', 'ID', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'STATE',
       'NAME', 'GSN FLAG', 'HCN/CRN FLAG', 'WMO ID', 'Unnamed: 0_y',
       'YEARMONTHDAY', 'ELEMENT', 'DATA VALUE', 'M-FLAG', 'Q-FLAG', 'S-FLAG',
       'OBS-TIME'])
        self.assertTrue(merged_name.issuperset(expected_name))
        self.assertIsInstance(get_weather_data(),pd.DataFrame)

class TestCleanData(unittest.TestCase):
    #Tests if we clean the data correctly and in the appropriate range of time.

    def test_clean(self):
        cleaned = clean_data(get_weather_data())
        self.assertTrue((1980 <= cleaned['year']).all() and (cleaned['year'] <= 2009).all())
        self.assertTrue((1 <= cleaned['month']).all() and (cleaned['month'] <= 12).all())
        self.assertTrue((1 <= cleaned['day']).all() and (cleaned['day'] <= 31).all())
        self.assertSetEqual(set(cleaned['ELEMENT']),{'TMAX','TMIN'})


class TestFilter(unittest.TestCase):
    #Tests if the data was filtered correctly.
    
    def test_filter(self):
        filtered = filter_ranson_criteria(clean_data(get_weather_data()))
        self.assertIsInstance(filtered,pd.DataFrame)
        self.assertTrue(set(filtered.columns).issuperset(set(['NAME','year','ELEMENT'])))

class TestBiasCorrection(unittest.TestCase):
    #Tests if bias correction algorithm is working

    def test_bias_sanity(self):
        data = bias_correction(filter_ranson_criteria(clean_data(get_weather_data())))
        self.assertTrue('adjusted_data' in data.columns)

class TestMain(unittest.TestCase):
    # Tests main as sanity check

    def test_main_sanity(self):
        data = main()
        self.assertTrue(len(data) == 2)

if __name__ == "__main__":
    unittest.main()