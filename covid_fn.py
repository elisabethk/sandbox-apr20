# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 13:19:39 2020

@author: elisa

Some functions to analyse COVID-19 case data from covid19api.com
"""

#################################################################
# Load libraries 
#################################################################

import pandas as pd
import json
import world_bank_data as wb 
import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib 
import random
import copy

################################################################
# Set up look-up table of country names and population
# I: List of countries
# O: Dataframe
#################################################################

# Get a list of country names and populations from world_bank_data
def get_pop_data():
    countries = wb.get_countries()
    population = wb.get_series('SP.POP.TOTL', mrv=1).reset_index()
    countries = countries[['region', 'name']].rename(columns={'name': 'country'}).loc[countries.region != 'Aggregates']
    countries = pd.merge(left = countries,
                   right = population,
                   left_on = 'country',
                   right_on = 'Country',
                   how = 'left')
    countries = countries[['Country','SP.POP.TOTL']]
    countries.columns = ['Country', 'Population']
    
    # Match country names with COVID API data
    countries['Country_std'] = countries['Country']
    countries['Country_std'].replace({
            'United States' : 'United States of America',
            'Iran, Islamic Rep.' : 'Iran, Islamic Republic of',
            'Hong Kong SAR, China': 'Hong Kong, SAR China',
            'Korea, Rep.' : 'Korea (South)',
            'Vietnam' : 'Viet Nam',
            'Egypt, Arab Rep.' : 'Egypt',
            'Yemen, Rep.' : 'Yemen',
            'Syrian Arab Republic' : 'Syrian Arab Republic (Syria)',
            'Kyrgyz Republic' : 'Kyrgyzstan',
            'Venezuela, RB' : 'Venezuela (Bolivarian Republic)'
            }, inplace = True)
    
    # Get list of countries from COVID API and merge on population 
    covid_countries = requests.get("https://api.covid19api.com/countries")
    covid_countries = pd.DataFrame(json.loads(covid_countries.text))
    
    countries = pd.merge(
            how = 'left',
            left = covid_countries,
            right = countries,
            left_on = 'Country',
            right_on = 'Country_std')
    
    countries = countries[['Country_x', 'Slug', 'Population']].rename({
            'Country_x' : 'Country'
            }, axis = 1)
    
    return countries

################################################################
# Load data given a country (drop latitude, longitude, status, countrycode)
# I: List of countries
# O: Dataframe (long)
#################################################################

def load_country_region(country):
    response = requests.get("https://api.covid19api.com/country/" + country + "/status/confirmed")

    # convert to a dataframe
    
    df = pd.DataFrame(json.loads(response.text))
    
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    df = df.drop(['Lat','Lon', 'City', 'CityCode', 'CountryCode','Status'], axis = 1)
    
    df = df.pivot_table(values = 'Cases', columns = 'Province', index = 'Date', aggfunc = np.sum).reset_index()   

    return df

################################################################
# Load data given a list of countries (basic: keep cases, country, date) 
# Some countries don't have province data
# I: List of countries
# O: Dataframe (wide - columns are country names)
#################################################################

def load_country_basic(country, status = 'confirmed'):
    response = requests.get("https://api.covid19api.com/country/" + country + "/status/" + status)

    # convert to a dataframe
    
    df = pd.DataFrame(json.loads(response.text))
    
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    
    # Flatten province level data if applicable
    df = df.pivot_table(values = 'Cases', index = ['Country', 'Date'], aggfunc = np.sum).reset_index()
   
    return df

def load_countries_basic(countries, status = 'confirmed'):
    
    df = pd.DataFrame()
    
    for country in countries:
        new_country = load_country_basic(country, status)
        df = df.append(new_country)
        
    df = pd.pivot_table(df, values = 'Cases', index = 'Date', columns = 'Country', aggfunc = np.sum).reset_index()
    
    # Fill nans
    countrylist = df.columns.drop(['Date'])
    for country in countrylist:
        df[country] = df[country].ffill()
        df[country] = df[country].fillna(0)
        
    return df 

################################################################
# Reshape data to start count from 100th case (countries)
# I: Dataframe (Date col, wide format - countries on columns)
# O: Dataframe (Date col, wide format - countries on columns)
#################################################################

def from100cases(df):
    
    countries = get_pop_data()
    
    countrylist = countries[countries['Country'].isin(df.columns)]

    # Find the day of 100th case for each country
    countrylist['dayof100'] = 0
    countrylist['dayof100'] = countrylist.apply(lambda x: df[df[x['Country']].gt(99)].index[0], axis = 1)
    
    # Append the case numbers since the 100th case for each country into since100
    since100 = pd.DataFrame()
    
    for country in countrylist['Country']:
        # Pull out the day of 100th case for given country
        start = countrylist[countrylist['Country'] == country]['dayof100']
        start = start.reset_index()
        start = start['dayof100'][0]
        
        # Cut out the count of cases since 100th case
        counts = df[country][start:].reset_index()
        counts.drop(['index'], axis = 1, inplace = True)
        
        since100 = pd.concat([since100,counts], axis = 1)
        
    return since100

################################################################
# Plots cumulative cases against time 
# I: Dataframe
# O: Null
#################################################################

def plot_cum_cases(df, logplot = False):
    df.plot(logy = logplot)
    

################################################################
# Take case data for countries, normalises for population
# I: Dataframe (Date col, wide format - countries on columns)
# O: Dataframe (Date col, wide format - countries on columns)
#################################################################

def normalise_pop(df):
    country_list = df.columns.drop(['Date'])
    countries = get_pop_data()
    
    dfn = pd.melt(df,
                 id_vars = ['Date'],
                 value_vars = country_list,
                 value_name = 'Cases',
                 var_name = 'Country'
                 )
    
    dfn = pd.merge(left = dfn,
                  right = countries,
                  left_on = 'Country',
                  right_on = 'Country',
                  how = 'left'
                  )
    
    dfn['Cases_norm'] = 100000*dfn['Cases']/dfn['Population']
    
    dfn = dfn[['Date', 'Country', 'Cases_norm']]
    
    dfn = pd.pivot_table(dfn, 
                        values = 'Cases_norm', 
                        index = 'Date',
                        columns = 'Country',
                        aggfunc = np.sum).reset_index()
    
    return dfn

################################################################
# Plots new cases against total cases
# I: Dataframe (Date col, wide format - countries on columns)
# O: Null
#################################################################

def plot_newcases(df):
    dfnew = copy.deepcopy(df)
    country_list = dfnew.columns.drop(['Date'])
    
    for country in country_list:
        dfnew[country + '_newCases'] = dfnew[country].diff()
        dfnew[country + '_newCases'] = dfnew[country + '_newCases'].replace({
                0: np.nan})
    
    colors = ['black', 'red', 'm', 'orange', 'skyblue', 'darkblue', 'lawngreen', 'navy', 'lightcoral', 'grey', 'lightslategrey']
    random.shuffle(colors)
    colors = iter(colors)
    
    for country in country_list:
        if country == country_list[0]:
           ax = dfnew.plot(
                     kind = 'scatter',
                     x = country,
                     y = country + '_newCases', 
                     color = next(colors), 
                     logy = True,
                     logx = True,
                     label = country)
        else:
           dfnew.plot(
                 kind = 'scatter',
                 x = country,
                 y = country + '_newCases', 
                 color = next(colors), 
                 label = country, 
                 logy = True,
                 logx = True,
                 ax = ax)
    
    ax.set_xlabel("Cases")
    ax.set_ylabel("New cases")
    ax.set_xlim(0.9,)
    ax.set_ylim(0.9,)
    ax.legend(loc = 'upper left')
    plt.show()
    
    return dfnew
    



