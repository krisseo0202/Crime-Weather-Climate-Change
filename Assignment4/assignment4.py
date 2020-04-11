import os
import re
import pandas as pd
import numpy as np
import reverse_geocoder as rg
import geopy
import geopy.distance as gd
from geopy.distance import vincenty
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent = "andrewtan-stat159")

# import from previous assignments
from Assignment1.weighted_avg import calc_inv_weighted_avg
from Assignment2.assignment2 import get_alameda_county_points, get_stations, get_station_weights
from Assignment3.assignment3 import main


def divide_alameda_points():
    """ Return a list of West Alameda points and a list of East Alameda points

    return:
        list: list of West Alameda (lat, lon) points
        list: list of East Alameda (lat, lon) points
    """
    grid_points = get_alameda_county_points()
    border_west = -122.06 # westernmost point of "East Alameda", points to the left are in West Alameda
    border_east = -121.82 # easternmost point in "West Alameda", points to the right are in East Alameda

    # zipcodes identified to be in West or East Alameda based on Google Maps
    zip_loc = {
        'west': [94539, 94552, 94544, 94536, 94537, 94538],
        'east': [94568, 94566, 94586]
    }

    west_alameda = []
    east_alameda = []
    for point in grid_points:
        if point[1] < border_west:
            west_alameda.append(point)
        elif point[1] > border_east:
            east_alameda.append(point)
        else:
            # classify ambiguous points that lie between border_west and border_east
            try:
                # get zipcode of unknown point
                unknown_zip = int(re.findall(r'\d+', geolocator.reverse(point).raw['address']['postcode'])[0])
                if unknown_zip in zip_loc['west']:
                    west_alameda.append(point)
                elif unknown_zip in zip_loc['east']:
                    east_alameda.append(point)
            except:
                # Some points represent landmarks or roads that stretch multiple zipcodes, 
                # causing the above code to error. We handle these cases separately.
                unknown_loc = geolocator.reverse(point).raw['address']['hamlet']
                if unknown_loc == 'Kilkare Woods':
                    west_alameda.append(point)
            
    return west_alameda, east_alameda


def run_assignment4():
    west_points, east_points = divide_alameda_points()

    # assignment 2
    west_weights = get_station_weights(west_points)
    east_weights = get_station_weights(east_points)

    print('West Weights: {}'.format(west_weights))
    print('East Weights: {}'.format(east_weights))

    # assignment 3
    west_bins = main(points=west_points)
    east_bins = main(points=east_points)
    
    print('West Bins: {}'.format(west_bins))
    print('East Bins: {}'.format(east_bins))

    
if __name__ == "__main__":
    run_assignment4()
