# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 14:48:19 2020

@author: elisa
"""

import covid_02 as cvd

################################################################
# Examples using functions in covid_02
#################################################################

# Load list of countries and population data 
countries = cvd.get_pop_data()

# Load COVID-19 case data from COVID19API for given countries 
df = cvd.load_countries_basic(['sweden', 'australia', 'switzerland', 'united-states', 'france', 'germany', 'united-kingdom', 'italy'])

# Plot cumulative cases for given countries
cvd.plot_cum_cases(df)

# As above, but since the day of the 100th case for each country
since100 = cvd.from100cases(df)
cvd.plot_cum_cases(since100, True)

# Normalise number of cases by country population and plot
dfn = cvd.normalise_pop(df)
cvd.plot_cum_cases(dfn)


