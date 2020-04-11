import os
import re
import pandas as pd
import numpy as np
import reverse_geocoder as rg
import geopy
import geopy.distance as gd
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
from Assignment3.assignment3 import main
from Assignment1.weighted_avg import calc_inv_weighted_avg
from Assignment2.assignment2 import get_alameda_county_points, get_stations, get_station_weights
from Assignment4.assignment4 import divide_alameda_points, run_assignment4
import unittest

class TestDivide(unittest.TestCase):
	def test_divide(self):

		d_west, d_east = divide_alameda_points()

		west = [(37.78251014815997, -122.30865472093605),
		(37.855007660508896, -122.30856533862595),
		(37.710011741493524, -122.21748756662697),
		(37.6375124410803, -122.12649758092323)]

		east = [(37.56501224749678, -121.6713676250229),
		(37.56501224749678, -121.58028857815076),
		(37.6375124410803, -121.76182768882086)]

		for point in west:
			self.assertTrue(point in d_west)

		for point in east:
			self.assertTrue(point in d_east)

	def test_run_assn_4(self):
		run_assignment4()
