# Group Assignment 6

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
This repo contains code, tests, and documentation for Group Assignment 6. In this assignment, we fit a Poisson regression model for all of Alameda County, West Alameda, and East Alameda, separately. We regressed crime counts on binned counts for temperature and precipitation for each month and year combination. We then devised and performed a permutation test to check whether the regressions on East and West Alameda are consistent with a single model. Using the permutation bootstrap test, we wanted to check if the relationship between weather and crime is meaningfully different for the two parts of Alameda County.

### Data Collection
First, we collected and binned temperature data from each data point within Alameda County (from Assignments 2 and 3). We then split this data up into East and West Berkeley based on the (lat, lon) points (from Assignment 4). This gave us our explanatory data, which included counts for temperature and precipation bins for each month and year combination, which is a dataframe with shape 360 x 10 (7 temperature and 3 precipation bins). We gathered crime data from the provided [Open ICPSR link](https://www.openicpsr.org/openicpsr/project/100707/version/V7/view); the specific dataset we downloaded was `ucr_offenses_known_monthly_1960_2016_dta.zip`. We filtered for data points in Alameda County and between the years 1980 - 2009. To get crime counts, we summed up all crimes for all zipcodes that fell into our three groups (West Alameda, East Alameda, and all of Alameda County). Combining the binned data and crime data, we have the full dataset to perform our Poisson regression.

### Poisson Regression
[TODO: Kunal] We used the out-of-the-box GLM functions from the `statsmodel` module.

### Permutation Test

We devised and performed a permutation test to check whether the regressions on East and West Alameda are consistent with a single model. Using the permutation bootstrap test, we wanted to check if the relationship between weather and crime is meaningfully different for the two parts of Alameda County. To do this, we used the RMSE of West and East Alameda as our test statistic to measure the two models of West and East Alameda. The combined RMSE is a good measure of the combined fit of the two models, and it's a good way to check if fitting two separate models fits the crime data "surprisingly better" than if the relationship were the same everywhere. We calculated the test statistic for our original split, and we compared this value to the empirical CDF of test statistics after randomly permutating the data and rerunning the test many times. For our permutation, we randomly assigned data points to West and East Alameda using a PRNG (p = 0.5). Then, we fit two Poisson regression models to these two sets of randomized data and computed the combined RMSE. We performed this procedure many times (roughly 10,000 times). We performed a one-sided test to get the p-value, which is the portion of test statistics that are smaller than our original value. If the p-value is low, then the RMSE calculated from the randomly assigned data is typically much larger than it is for the original data, which is evidence that the relationship between weather and crime is truly different in West Alameda and East Alameda.

#### Randomization Strategy

Our permutation test involves creating 10,000 pseudo-randomly generated splits of the data in Alameda County. We calculate the RMSE for each of these generated samples to create an empirical CDF of errors and use this to find a p-value for the errors found in our east and west samples.

Although non-cryptographic PRNGs have obvious flaws, in this particular project, the flaws are not as consequential. Since our random permutations are not used for security, it is not necessary to randomize in a way such that it cannot be decrypted.

For our test to work, we have to assume:
* Randomness - Python's random number generator is strong enough based on what we've tested. Even though Mersenne Twister has a state space that cannot generate all permutations of over 2084 things, our data only contains about 700 rows, so we can still generate all the permutations. We have also checked that there is a balanced distribution between even and odd rows picked. We have also recorded the seed for reproducibility.
* Large enough sample size.
* Variance in our samples are approximately equal.


## Instructions to Duplicate Results
To run this assignment, go to the root directory of the project (cwcc-g11) and run the following command: `python -m Assignment6.assignment6`. To run the unit tests, run the following command: `python -m unittest Assignment6.test_assignment6`. To run the unit tests with coverage, run the following command: `coverage run -m unittest Assignment6.test_assignment6` followed by `coverage report -m`. For this to work, place the data files at `cwcc-g11/Assignment6/data`. The weather station data can be found in this [OSF link](https://osf.io/kwtem/). The crime data can be found in this [Open ICPSR link](https://www.openicpsr.org/openicpsr/project/100707/version/V7/view); the specific dataset we downloaded was `ucr_offenses_known_monthly_1960_2016_dta.zip`.

1. Import the necessary packages denoted specified above and in the `environment.yml` file. 
    - import Nominatim from geopy.geocoders and declare a global geolocator object
    - import the necessary functions from Assignments 1 - 5
2. Create a folder called `data` and place data files there. You should have `cwcc-g11/Assignment6/data/stations_ca.csv` and `cwcc-g11/Assignment6/data/weather_data_ca.csv` in your path. The data can be found in this [OSF link](https://osf.io/kwtem/) You should also have the crime data `cwcc-g11/Assignment6/data/ucr_offenses_known_monthly_1960_2016_dta`, which can be found in this [Open ICPSR link](https://www.openicpsr.org/openicpsr/project/100707/version/V7/view).
3. Collect and clean the data that will go into our Poisson regression model. This involves binning the temperature and precipitation data, filtering and cleaning the crime data, and joining the explanatory and response variables data.
4. We perform this regression on all Alameda County, West Alameda, and East Alameda data points. Record the test statistic (combined RMSE) of West and East Alameda data.
5. Run the permutation test 


