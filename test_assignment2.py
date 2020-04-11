import unittest
import numpy as np
import reverse_geocoder as rg
import pandas as pd

# functions from previous assignments
from Assignment1.weighted_avg import calc_inv_weighted_avg
from Assignment2.assignment2 import get_alameda_county_points, get_stations, get_station_weights, main


class TestAssignment2(unittest.TestCase):

    grid = get_alameda_county_points()

    def test_get_alameda_county_points(self):
        """ Test get_alameda_county_points function and confirms border of Alameda County points 
        1) Tests that all points are within bounding box
        3) Tests that points within grid are actually in Alameda County 
        """
        grid = TestAssignment2.grid
        north, west, south, east = 38, -122.4, 37.4, -121.4 # bounding box
        # check that all points are within bounding box
        for coord in grid:
            self.assertTrue(west < coord[1] < east)
            self.assertTrue(south < coord[0] < north)
        # check that points within grid are actually in Alameda County 
        for i in range(1,5):
            self.assertTrue(rg.search(grid[i*3])[0]['admin2'] == "Alameda County")


    def test_get_stations(self):
        """ Take "randomly" handpicked weather stations from stations_ca and use Google Maps 
        to measure distance from Alameda County. Check that test_stations confirms this.
        """
        grid = TestAssignment2.grid
        stations = get_stations(grid, 6)
        #USC00046333, 37.8, -122.2667, should be inside
        #US1CACC0003, 37.9485, -122.0541, should be outside
        #US1CACC0001, 37.9898, -122.1085, should be outside
        #US1CAAL0031, 37.5685, -121.9654, should be inside
        #USC00046332, 37.7833, -122.1667, should be inside
        #USC00046336, 37.7983, -122.2642, should be inside
        #US1CABT0002, 39.514, -121.518, should be outside 

        stations_indices = []
        for i in stations:
            stations_indices.append(i['ID'])

        inside = ["USC00046333", "US1CAAL0031", "USC00046332", "USC00046336"]
        outside = ["US1CACC0003", "US1CACC0001", "US1CABT0002"]

        for index in inside:
            self.assertTrue(index in stations_indices)

        for index in outside:
            self.assertTrue(index not in stations_indices)


    def test_get_station_weights(self):
        """ 
        Test the station weights produced by get_station_weights
        """
        grid = TestAssignment2.grid
        weights = get_station_weights(grid)
        # check that station weights are >= 0
        for weight in weights:
            self.assertGreater(weight, 0)


    def test_main(self):
        """ Test the main function in assignment2 to make sure it runs.
        The functions used in main are already tested above.
        """
        main()
    

if __name__ == '__main__':
    unittest.main()
