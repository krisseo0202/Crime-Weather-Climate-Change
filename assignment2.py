import os
import pandas as pd
import numpy as np
import reverse_geocoder as rg
import geopy
import geopy.distance as gd
from geopy.distance import vincenty

# import from previous assignments
from Assignment1.weighted_avg import calc_inv_weighted_avg


def get_alameda_county_points():
    """ Calculates all the grid points (lat, lon) inside Alameda County
    Grid automatically includes Summit Reservoir (37.905098, -122.272225)
    Begin at northwest corner of bounding box and move in increment of 5 miles
    in the south and east directions until we reach the southeast corner,
    recording all grid points that fall inside Alameda County.

    return:
        list: list of (lat, lon) points inside Alameda County
    """
    # bounding box around Alameda County
    north = 38
    west = -122.4
    south = 37.4
    east = -121.4

    # grid automatically includes Summit Reservoir (37.905098, -122.272225)
    grid_points = [(37.905098, -122.272225)]
    curr = [north, west]

    # while current point is within the north / south bounds
    while curr[0] > south:
        # dynamically update lat and lon increment based on curr point
        destE = vincenty(miles=5).destination(curr, 90) # point 5 miles east of curr
        lon_increment = destE.longitude - curr[1]
        destS = vincenty(miles=5).destination(curr, 180) # point 5 miles south of curr
        lat_increment = curr[0] - destS.latitude

        # while current point is within the east / west bounds
        while curr[1] < east:
            if (rg.search(curr)[0]['admin2'] == "Alameda County"):
                grid_points.append(tuple(curr))
            curr[1] += lon_increment
        curr[0] -= lat_increment
        curr[1] = west

    return grid_points


def get_stations(grid_points, max_distance=10):
    """ Find all weather stations within max_distance (miles) from each of the grid points

    args:
        grid_points: list of grid points (lat, lon)
        max_distance: max distance to search around each grid point (default 10)
    return:
        list: list of weather stations (Series objects)
    """
    
    station_data = pd.read_csv('Assignment2/data/stations_ca.csv')

    seen_stations = set()
    stations = []

    for point in grid_points:
        for index, station in station_data.iterrows():
            station_pos = (station['LATITUDE'], station['LONGITUDE'])
            if gd.distance(point, station_pos).miles <= max_distance and index not in seen_stations:
                seen_stations.add(index)
                stations.append(station)
    
    return stations


def get_station_weights(grid_points, max_distance=10):
    """ Returns a list of weights corresponding to all the weather stations around grid points

    args:
        grid_points: list of grid points (lat, lon)
        max_distance: max distance to search around each grid point (default 10) 
    return:
        list: list of station weights (floats), one for each station
    """
    stations = get_stations(grid_points, max_distance)
    station_pos = [(station['LATITUDE'], station['LONGITUDE']) for station in stations]
    station_weights = calc_inv_weighted_avg(grid_points, station_pos)
    return station_weights

def main():
    grid_points = get_alameda_county_points()
    stations = get_stations(grid_points, max_distance=10)
    station_weights = get_station_weights(grid_points, max_distance=10)
    print(station_weights)

if __name__ == "__main__":
    main()
    