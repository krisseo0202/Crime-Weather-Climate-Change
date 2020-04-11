# Group Assignment 5

**Due: 12/2/18**

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

This repo contains code, tests, and documentation for Group Assignment 5. In this assignment, we are looking to test if Berkeley and Livermore have the same weather data. We will first import the necessary functions from the past assignments. Specifically, we import get_almeda_county_points, filter_randon_criteria, clean_data, and get_weather_data. 

### Capturing Data and Binning

We first bin the maximum temperature for the weather stations using Ranson's categories: 0°F-10°F, 10°F-20°F, 20°F-30°F, 30°F-40°F, 40°F-50°F, 50°F-60°F, 60°F-70°F, 70°F-80°F, 80°F-90°F, and 90°F-100°F. We do this through the functions `get_data()` and `get_city_data(df, id, element='TMAX')`. Then we convert the data points to fahrenheit using `convert_to_fahrenheit(df)`. 

### Intersecting Livermore's and Berkeley's DataFrame

The above creates the initial data frame that bins the maximum temperature. To perform a two sample test, the length of the data sets have to be the same. Since Livermore contains more data than Berkeley, we use get_intersected to shorten Livermore's data to match Berkley's data frame. Essentially, we create one data frame with both Berkeley's data frame and Livermore's data frame. We then split the data frame into two. The intersection formula is denoted below.

### Stratification

**What did you stratify on? Why is that a good choice? Why stratify at all?**

After we have both dataframes, we stratify the data by year and month. We believe that these are good stratas because they are mutually exclusive and collectively exhaustive. Furthermore, this accounts for climate change. On a larger yearly scope, this accounts for global warming. On a smaller monthly scope, this accounts for seasonality. 

### Chi-Squared Distribution 

**Can you use the chi-square distribution to calibrate the test? Why or why not?**

After the stratification of the data, we use the fisher combining formula. The value from the formula is chi-square distributed therefore you can use chi-square distribution to calibrate the test. We can then use a chi-squared distribution to determine how well our data's distribution compares to a normal, binomial, or poisson distribution. 

From there, we calculate the p-value. Below is the function for the above process.

### Taking into Account Simulation Uncertainty 

**Discuss how to take into account simulation uncertainty in estimating the overall P-value**

To reduce uncertainty in estimating the overall p-value, we can generate PRNG on the data for certain amount of times until p-values converge or use bias-correction as Ranson mentioned. 
Essentially, using the two-sample function provided by Professor Stark.

### Conclusion

**Discuss what your findings mean for Ranson's approach**

Since our findings include a p-value that is lower than alpha, we must reject the null hypothesis. Therefore, we conclude that the weather in Livermore and in Berkeley is not the same. In Ranson's paper, he assumed that the weather within a county is the same. However, this is not the case according to our findings. 

Since Ranson assumed that the weather within a county is the same, his results could be misleading. Mainly, the positive correlation between crime rate and high temperature could be exagerrated since the cities within a county could have differing temperatures. The vice versa holds true also. 

## Instructions to Duplicate Results
To run this assignment, go to the root directory of the project (cwcc-g11) and run the following command: `python -m Assignment5.assignment5`. To run the unit tests, run the following command: `python -m unittest Assignment5.test_assignment5`. To run the unit tests with coverage, run the following command: `coverage run -m unittest Assignment5.test_assignment5` followed by `coverage report -m`. For this to work, place the data files at `cwcc-g11/Assignment5/data`. The weather station data can be found in this [OSF link](https://osf.io/kwtem/).

1. Import the necessary packages denoted specified above and in the `environment.yml` file. 
    - import Nominatim from geopy.geocoders and declare a global geolocator object
    - import the necessary functions from Assignments 1 - 4
2. Create a folder called `data` and place data files there. You should have `cwcc-g11/Assignment5/data/stations_ca.csv` and `cwcc-g11/Assignment5/data/weather_data_ca.csv` in your path. The data can be found in this [OSF link](https://osf.io/kwtem/).
3. Run the `main` in `assignment5.py`.
    a. Run `get_data` to get data from Fanson's criteria.
    b. Run `get_city_data` to get data for Berkeley and Livermore.
    c. Run `convert_to_fahrenheit` to add the fahrenheit column to the data.
    d. Run `bin_data` to bin the data by temperature and precipitation.
    e. Run `stratify` to stratify the data by month and year.
    f. Run `permutation_test` to perform the stratified permutation test and get the p-value using fisher combining function.
