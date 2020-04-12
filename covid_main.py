# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 14:48:19 2020

@author: elisa
"""

import covid_fn as cvd

################################################################
# Examples using functions in covid_fn
#################################################################

# Load list of countries and population data 
countries = cvd.get_pop_data()

my_countries = ['sweden', 'australia', 'switzerland', 'united-states', 'france', 'germany', 'united-kingdom', 'italy']

# Load COVID-19 case data from COVID19API for given countries 
df = cvd.load_countries_basic(my_countries)

# Plot cumulative cases for given countries
cvd.plot_cum_cases(df)

# As above, but since the day of the 100th case for each country
since100 = cvd.from100cases(df)
cvd.plot_cum_cases(since100, logplot = True) 

# Normalise number of cases by country population and plot
dfn = cvd.normalise_pop(df)
cvd.plot_cum_cases(dfn)

# Track deaths instead of total cases
df = cvd.load_country_basic('australia', status = 'deaths')
df = cvd.load_countries_basic(['australia', 'italy'], status = 'deaths')
cvd.plot_cum_cases(df)

#################################################################
# Doodles 
#################################################################


# Some data comes with province (state) level data, others don't

aus = cvd.load_country_region('australia')
us = cvd.load_country_region('united-states')

cvd.plot_cum_cases(aus)


# Pick out the largest cases amongst US states
us.columns
#us = us[['New York', 'New Jersey', 'Texas', 'Illinois', 'Florida']]
cvd.plot_cum_cases(us, logplot = True)

us_latest = pd.DataFrame.transpose(us.tail(1)).drop('Date')
us_latest.columns = ['Cases']
us_top = pd.Series(us_latest.sort_values(by = 'Cases', ascending = False)[0:10].index)

us_filtered = us[pd.concat([pd.Series(['Date']),us_top])]

cvd.plot_cum_cases(us_filtered, logplot = False)

cvd.plot_newcases(aus)

# do state things 

# to get US population by state
# https://www.census.gov/data/developers/data-sets/popest-popproj/popest.html

# Plot new cases against days
# Deaths by state/province/region 

# Basic modelling... 



