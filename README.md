# Group Assignment 2

**Due: 11/4/18**

### Group Members:
* Kunal Desai
* Chris Fan
* Brandon Huang
* Kris Seo
* Andrew Tan

Dependencies:
 * Python **3.5**
 * Numpy version **1.14.5**
 * Pandas **0.22.0**
 * Geopy **1.17.0**
 * Reverse Geocoder **1.5.1**
 * Other dependencies can be found in `environment.yml`

## Project Description
This repo contains code, tests, and documentation for Group Assignment 2. In this assignment, we drew out a bigger box that includes all Alameda county points. We ran reverse geocoder to locate the points that are within Alameda county by 5 miles to create a list of grid points for Alameda county. Next, we created a function to identify all weather stations within 10 miles of any of the grid points in Alameda county. Furthermore, this function is scalable to input any x miles and input any number of grid point(s). Next, we developed a function called get_station_weights to calculate the inverse weighted average from weather stations within a x mile vicinity to a certain grid point(s). 

## Instructions to Duplicate Results
To run this assignment, go to the root directory of the project (cwcc-g11) and run the following command: `python -m Assignment2.assignment2`. To run the unit tests, run the following command: `python -m Assignment2.test_assignment2`. For this to work, place the data files at `cwcc-g11/Assignment2/data`. The data can be found from [this OSF link](https://osf.io/kwtem/).

1. Import the necessary packages denoted specified above and in the `environment.yml` file. 
    - specifically for reverse_geocoders, "pip install reverse_geocoders", rest of the packages should be pre-installed
    - from Assignment1, import the function calc_inv_weighted_avg
2. Create a folder called `data` and place data files there. You should have `cwcc-g11/Assignment2/data/stations_ca.csv` and `cwcc-g11/Assignment2/data/weather_data_ca.csv` in your path. The data can be found from [this OSF link](https://osf.io/kwtem/).
3. Perform the function get_alameda_county_points() to return a list of alameda county grid points.
4. Use the function get_stations to acquire a list of stations that are x miles away from a grid point(s).
5. Use the function get_station_weights() to acquire the inverse average weights for each weather station to a grid point(s).
6. Perform unit test to confirm a 99% coverage rate for all functions in assignmnet2.py.
