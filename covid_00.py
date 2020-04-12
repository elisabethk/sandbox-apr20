# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 10:38:06 2020

@author: elisa
"""

#  TEST COMMENT 

## Let's see if we can get some data
# https://realpython.com/python-json/
# https://stackoverflow.com/questions/19483351/converting-json-string-to-dictionary-not-list

import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import world_bank_data as wb

##

#response = requests.get("https://api.covid19api.com/")
#
#response.status_code
#response.json()

##

#all_data = requests.get("https://api.covid19api.com/all")

#print(all_data.text)

#all_data.json()

##

#mydata = json.loads(all_data.text)
#
#mydata[100]['Country']
#
### https://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search
#
#sample = list(filter(lambda item: item['Country'] == 'Australia', mydata))

## 

# https://stackoverflow.com/questions/20638006/convert-list-of-dictionaries-to-a-pandas-dataframe
#df = pd.DataFrame(mydata)
#
#####################################################
#
#df = df.drop(['Lat','Lon'], axis=1)
#
##countries = df['Country'].value_counts()
#
#df = df[df['Country'].isin(['US','Australia','United Kingdom', 'Canada', 'France', 'Germany', 'Italy', 'New Zealand'])]
#
#df['Date'] = pd.to_datetime(df['Date']).dt.date


################################################
################## Only get Australia ########## 
################################################

#response = requests.get("https://api.covid19api.com/country/australia/status/confirmed")
#
## convert to a dataframe
#
#df = pd.DataFrame(json.loads(response.text))
#
#df = df.drop(['Lat','Lon','CountryCode','Country','City','CityCode','Status'], axis = 1)
#
#df['Date'] = pd.to_datetime(df['Date']).dt.date

################################################
###### Number of confirmed cases in Australia ##
################################################

#aus = df
#
#aus['Province'].unique()
#
### Get total by day
#
#aus_total = pd.pivot_table(aus, values = 'Cases', index = ['Date'], aggfunc = np.sum).reset_index()
#
## Plot 
##
#plt.bar(aus_total['Date'], aus_total['Cases'])
##
#plt.show()

################################################
##### Line charts comparing states #############
################################################

#states = df
#
#states = states[states['Province'].isin(['New South Wales', 'Victoria', 'South Australia', 'Queensland', 'Western Australia'])]
#
#state_totals = pd.pivot_table(states, values = 'Cases', index = ['Date'], columns = ['Province'], aggfunc = np.sum).reset_index()
#
## Plot
#
#state_totals.plot()

#
#num = 0
#palette = plt.get_cmap('Set1')
#for column in state_totals.drop('Date', axis = 1):
#    num +=1 
#    plt.plot(state_totals['Date'], state_totals[column], marker = '', color = palette(num), linewidth = 1, label = column)
#    
#plt.legend(loc = 2, ncol = 2)
#plt.xlabel("Date")
#plt.ylabel("Cumulative cases")
#
#plt.show()
#
## Log scale
#
#state_totals[state_totals['Date'] > dt.date(2020,3,1)].plot(logy = True)

################################################
##### Australia - new cases vs all cases    ####
################################################

#aus = df
#
#aus_total = pd.pivot_table(aus, values = 'Cases', index = 'Date', aggfunc = np.sum).reset_index()
#
#aus_total['NewCases'] = aus_total['Cases'].diff()
#
## plot new cases against total cases 
#
#aus_total.plot()
#
#plt.scatter(aus_total['Cases'],
#        aus_total['NewCases'])

##############################################
##### A function takes country and plots 
##### New cases against all cases 
##############################################

#def country_scatter(country):
#    response = requests.get("https://api.covid19api.com/country/" + country + "/status/confirmed")
#
#    # convert to a dataframe
#    
#    df = pd.DataFrame(json.loads(response.text))
##    
##    df = df.drop(['Lat','Lon','CountryCode','Country','City','CityCode','Status'], axis = 1)
#
#    df['Date'] = pd.to_datetime(df['Date']).dt.date
#
#    country_total = pd.pivot_table(df, values = 'Cases', index = 'Date', aggfunc = np.sum).reset_index()
#
#    country_total['NewCases'] = country_total['Cases'].diff()
#
#    # plot new cases against total cases 
#
#    plt.scatter(country_total['Cases'],
#            country_total['NewCases'])
# 
##########################################
#
## Call the function 
#all_data = requests.get("https://api.covid19api.com/countries")
#
#country_list = pd.DataFrame(json.loads(all_data.text))
#
#country_scatter("italy")


##############################################
##### A function that 
##### Loads the data for a particular country
##############################################

#def load_country(country):
#    response = requests.get("https://api.covid19api.com/country/" + country + "/status/confirmed")
#
#    # convert to a dataframe
#    
#    df = pd.DataFrame(json.loads(response.text))
#    
#    df['Date'] = pd.to_datetime(df['Date']).dt.date
#
#    df = df.drop(['Lat','Lon','CountryCode','Status'], axis = 1)
#
#    return df
#
##### Second version - only pick bare minimum of cols
#def load_country_basic(country):
#    response = requests.get("https://api.covid19api.com/country/" + country + "/status/confirmed")
#
#    # convert to a dataframe
#    
#    df = pd.DataFrame(json.loads(response.text))
#    
#    df['Date'] = pd.to_datetime(df['Date']).dt.date
#    
#    df = df.pivot_table(values = 'Cases', index = ['Country', 'Date'], aggfunc = np.sum).reset_index()
#
##    df = df[['Country','Date','Cases']]
#
#    return df

##############################################
##### A function that 
##### Loads the data for particular countries
##############################################

#def load_countries(countries):
#    
#    df = pd.DataFrame()
#    
#    for country in countries:
#        new_country = load_country_basic(country)
#        df = df.append(new_country)
#        
#    return df 

####################################################
######### Comparing states - days from 100th case ##
####################################################
#
#aus = load_country('australia')
#
#states = aus[aus['Province'].isin(['New South Wales', 'Victoria', 'South Australia', 'Queensland', 'Western Australia'])]
#
## Pivot states into columns
#state_totals = pd.pivot_table(states, values = 'Cases', index = ['Date'], columns = ['Province'], aggfunc = np.sum).reset_index()
#
## Get dataframe of states and find the day of 100th case
#my_states = pd.DataFrame(state_totals.columns.drop(['Date']))
#my_states['day100'] = 0
#
### Very un-pythonic
##num = 0
##for state in my_states['Province']:
##    my_states.iloc[num, 1] = state_totals[state_totals[state].gt(99)].index[0]
##    num += 1
#
### Pythonic way 
#my_states['day100'] = my_states.apply(lambda x: state_totals[state_totals[x['Province']].gt(99)].index[0], axis = 1)
#
## Initialise an empty dataframe
#since100 = pd.DataFrame()
#
## Append the case numbers since the 100th case for each state into since100
### https://stackoverflow.com/questions/27126511/add-columns-different-length-pandas/33404243
#
#for state in my_states['Province']:
#    # Pull out the day of 100th case for given state
#    start = my_states[my_states['Province'] == state]['day100']
#    start = start.reset_index()
#    start = start['day100'][0]
#    
#    # Cut out the count of cases since 100th case
#    counts = state_totals[state][start:].reset_index()
#    counts.drop(['index'], axis = 1, inplace = True)
#    
#    since100 = pd.concat([since100,counts], axis = 1)
#
#since100.plot()
    
####################################################
######### Normalise to population ##################
####################################################

# get population 
# Countries and associated regions
#countries = wb.get_countries()
#
## Population dataset, by the World Bank (most recent value)
#population = wb.get_series('SP.POP.TOTL', mrv=1)
#
## Aggregate region, country and population
#pop = countries[['region', 'name']].rename(columns={'name': 'country'}).loc[countries.region != 'Aggregates']
#pop['population'] = population
#
## clean pop names 
#
#pop['Country_std'] = pop['country']
#pop['Country_std'].replace({
#        'United States' : 'United States of America',
#        'Iran, Islamic Rep.' : 'Iran, Islamic Republic of',
#        'Hong Kong SAR, China': 'Hong Kong, SAR China',
#        'Korea, Rep.' : 'Korea (South)',
#        'Vietnam' : 'Viet Nam'
#        }, inplace = True)
#
## Get list of countries from covid api
#
#raw_countries = requests.get("https://api.covid19api.com/countries")
#
#country_list = pd.DataFrame(json.loads(raw_countries.text))
#
#country_list = country_list.merge(
#        how = 'left',
#        right = pop,
#        left_on = 'Country',
#        right_on = 'Country_std')

# Countries of interest 
#   
#df = load_countries(['australia','italy', 'united-states','france', 'germany', 'switzerland', 'united-kingdom','singapore','korea-south', 'iran','china','sweden'])
#
#df = df.merge(
#        right = country_list[['Country','population']],
#        left_on = 'Country',
#        right_on = 'Country')

#df['Cases_norm'] = 100000*df['Cases']/df['population']
#
#df_toplot = df.pivot_table(values = 'Cases_norm', 
#                           columns = 'Country',
#                           index = 'Date',
#                           aggfunc = np.sum).reset_index()
#
#df_toplot.plot()
#
## Get current rate by country - number of cases per 100,000 people
#
#today_rate = df.pivot_table(
#        values = 'Cases_norm',
#        index = ['Country'],
#        aggfunc = np.max).reset_index()




