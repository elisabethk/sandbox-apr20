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
cvd.plot_cases(df)

# As above, but since the day of the 100th case for each country
since100 = cvd.from100cases(df)
cvd.plot_cases(since100, logplot = True) 

# Normalise number of cases by country population and plot
dfn = cvd.normalise_pop(df)
cvd.plot_cases(dfn)

# Track deaths instead of total cases
df = cvd.load_country_basic('australia', status = 'deaths')
df = cvd.load_countries_basic(['australia', 'italy'], status = 'deaths')
cvd.plot_cases(df)

#################################################################
# Doodles 
#################################################################

# Some data comes with province (state) level data, others don't

aus = cvd.load_country_region('australia')
us = cvd.load_country_region('united-states')

cvd.plot_cases(aus)

aus_states = cvd.top_by_state(aus)
cvd.plot_cases(aus_states, logplot = False)
cvd.plot_newcases(aus_states)

us_states = cvd.top_by_state(us, top_n = 5)
cvd.plot_cases(us_states, logplot = False)

# plot new cases daily

aus_new = cvd.get_newcases(aus)
cvd.plot_cases(aus_new, logplot = False)



# to get US population by state
# https://www.census.gov/data/developers/data-sets/popest-popproj/popest.html




# Deaths by state/province/region 

# Basic modelling... 









