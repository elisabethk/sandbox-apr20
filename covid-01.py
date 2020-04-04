# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 10:38:06 2020

@author: elisa
"""

## Let's see if we can get some data
# https://realpython.com/python-json/
# https://stackoverflow.com/questions/19483351/converting-json-string-to-dictionary-not-list

import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

##

#response = requests.get("https://api.covid19api.com/")
#
#response.status_code
#response.json()

##

all_data = requests.get("https://api.covid19api.com/all")

#all_data.json()

##

mydata = json.loads(all_data.text)
#
#mydata[100]['Country']
#
### https://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search
#
#sample = list(filter(lambda item: item['Country'] == 'Australia', mydata))

## 

# https://stackoverflow.com/questions/20638006/convert-list-of-dictionaries-to-a-pandas-dataframe
df = pd.DataFrame(mydata)

####################################################

df = df.drop(['Lat','Lon'], axis=1)

#countries = df['Country'].value_counts()

df = df[df['Country'].isin(['US','Australia','United Kingdom', 'Canada', 'France', 'Germany', 'Italy', 'New Zealand'])]

df['Date'] = pd.to_datetime(df['Date']).dt.date

###### Number of confirmed cases in Australia

aus = df[df['Country'] == 'Australia']

aus['Province'].unique()

type(aus.iloc[2,2])


# Get total by day

aus_total = pd.pivot_table(aus, values = 'Cases', index = ['Country', 'Date'], columns = ['Status'], aggfunc = np.sum).reset_index()

# Plot 
#
#plt.bar(aus_total['Date'], aus_total['confirmed'])
#
#plt.show()

##### Line charts comparing states

states = df[df['Country'] == 'Australia']

states = states[states['Province'].isin(['New South Wales', 'Victoria', 'South Australia', 'Queensland', 'Western Australia'])]

state_totals = pd.pivot_table(states, values = 'Cases', index = ['Province', 'Date'], columns = ['Status'], aggfunc = np.sum).reset_index()

state_totals = pd.pivot_table(state_totals, values = 'confirmed', index = 'Date', columns = 'Province', aggfunc = np.sum).reset_index()

# Plot

state_totals.plot()
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
state_totals[state_totals['Date'] > dt.date(2020,3,1)].plot(logy = True)

######### Comparing states - days from 100th case

# states 

my_states = pd.DataFrame(state_totals.columns.drop(['Date']))
my_states['day100'] = 0

## Very un-pythonic
#num = 0
#for state in my_states['Province']:
#    my_states.iloc[num, 1] = state_totals[state_totals[state].gt(99)].index[0]
#    num += 1

my_states['day100'] = my_states.apply(lambda x: state_totals[state_totals[x['Province']].gt(99)].index[0], axis = 1)

since100 = pd.DataFrame(columns = pd.concat([
        pd.Series(['ndays']),
        my_states['Province']]
    ))

## This puts the nans at the top, want it at the end 
for state in my_states['Province']:
    start = my_states[my_states['Province'] == state]['day100']
    start = start.reset_index()
    start = start['day100'][0]
    since100[state] = state_totals[state][start:]

## https://stackoverflow.com/questions/27126511/add-columns-different-length-pandas/33404243
    






