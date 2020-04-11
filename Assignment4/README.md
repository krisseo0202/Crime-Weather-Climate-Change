# Group Assignment 4

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
This repo contains code, tests, and documentation for Group Assignment 4. In this assignment, we split Alameda County into West Alameda and East Alameda based on the 2 zipcodes 94552 and 94539. The points we're interested in classifying are the same Alameda County grid points we collected in Assignment 2. All points in or west of those 2 zipcodes are considered West Alameda. All points east of those 2 zipcodes are considered East Alameda. Given these 2 new sets of grid points, repeat the procedures from Assignments 2 and 3 for East Alameda and West Alameda separately. It took two key steps to divide the grid points into east and west. First, we found the westernmost point of East Alameda (border_west) and the easternmost point of West Alameda (border_east) using Google Maps. All points to the west of border_west are considered West Alameda, and all points to the east of this border_east are considered East Alameda. For points that lie between border_west and border_east, we looked up their zipcodes using `geolocator` and manually checked if they are east or west of the divider. One point did not produce a zipcode, so we visually checked its location on Google Maps.

## Instructions to Duplicate Results
To run this assignment, go to the root directory of the project (cwcc-g11) and run the following command: `python -m Assignment4.assignment4`. To run the unit tests, run the following command: `python -m unittest Assignment4.test_assignment4`. For this to work, place the data files at `cwcc-g11/Assignment4/data`. The data can be found from [this OSF link](https://osf.io/kwtem/).

1. Import the necessary packages denoted specified above and in the `environment.yml` file. 
    - import Nominatim from geopy.geocoders and declare a global geolocator object
    - import the necessary functions from Assignments 1, 2, and 3
2. Create a folder called `data` and place data files there. You should have `cwcc-g11/Assignment4/data/stations_ca.csv` and `cwcc-g11/Assignment4/data/weather_data_ca.csv` in your path. The data can be found from [this OSF link](https://osf.io/kwtem/).
3. Run `divide_alameda_points()` to divide the Alameda County grid points into West Alameda and East Alameda. You will have 2 separate sets of data now.
4. Perform the experiments from Assignment 2 on West Alameda and East Alameda grid points separately.
5. Perform the experiments from Assignment 3 on West Alameda and East Alameda grid points separately.
6. Perform unit test to confirm a 99% coverage rate for all functions in `assignment4.py`.

