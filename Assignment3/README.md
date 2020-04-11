# Group Assignment 3

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
This repo contains code, tests, and documentation for Group Assignment 3. In this assignment, we merged the weather data set with the stations dataset. Then we were able to identify the data that was valid for analysis based on Ranson's criteria and adjusted these points based on the bias algorithm provided in class. Finally, we binned the data so that it can be easily used to fit a regression model in our next assignment.

## Instructions to Duplicate Results
To run this assignment, go to the root directory of the project (cwcc-g11) and run the following command: `python -m Assignment3.test_assignment3`. For this to work, place the data files at `cwcc-g11/Assignment3/data` and `cwcc-g11/Assignment3/data`.

1. Import the necessary packages denoted specified above and in the environment.yml file. 
    - specifically for reverse_geocoders, "pip install reverse_geocoders", rest of the packages should be pre-installed
    - import the necessary functions from Assignments 1 and 2
2. Create a folder called `data` and place data files there. You should have `cwcc-g11/Assignment3/data/stations_ca.csv` and `cwcc-g11/Assignment3/data/weather_data_ca.csv` in your path.
3. Perform the `get_weather_data` function to get the relevant weather data given points and a distance.
4. Run the `filter_ranson_criteria` function to get the relevant data that meets the criteria.
5. Calculate the bias adjustment for the weather data by using the `bias_correction` function.
6. Bin the average adjusted temperature data and run all the above commands using the `main` function.
7. Perform unit test to confirm a 99% coverage rate for all functions in assignmnet3.py.
