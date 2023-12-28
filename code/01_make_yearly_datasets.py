"""
This file creates household datasets at the yearly level
using the main, population, and income subdatasets

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sys; sys.path.append('/home/mitch/school/data/mexico_enigh/src/')
sys.path.append('/home/mitch/util/python/')
import json_utils

import utils
import os

from simpledbf import Dbf5

dicts = '/home/mitch/school/data/mexico_enigh/dicts/'

os.chdir(dicts)
rename_main = json_utils.load_json('rename_main.json')
rename_population = json_utils.load_json('rename_population.json')
rename_income = json_utils.load_json('rename_income.json')
hhm_ids = json_utils.load_json('hhm_ids.json')
education = json_utils.load_json('education.json')


#years = ['1992', '1994', '1996', '1998', '2000', '2002', '2004', '2006', '2008']
years = ['1992', '1994', '1996', '1998', '2000']
raw = '/home/mitch/Dropbox/data/mexico_enigh/raw/'
interim = '/home/mitch/Dropbox/data/mexico_enigh/interim/'

toint = ['Y', 'hhid', 'location', 'relationship_to_hhm', 'weight', 'location_size', 'hh_size', 'sex', 'age', 'type_of_education']
tofloat = [
    'consumption_food', 'consumption_clothing', 'consumption_house',
           'consumption_health', 'consumption_transportation', 'consumption_education', 'consumption_personal',
           'income_salary', 'income_business', 'income_rental', 'income_transfers', 'income_other'
           ]

for year in years:
    print('cleaning ' + str(year))
    os.chdir(raw + year)
    main = Dbf5('main.dbf').to_dataframe()
    #income = Dbf5('income.dbf').to_dataframe()

    if year =='2006':
        population = pd.read_csv('population.csv')
        population.columns = [x.split(',')[0] for x in population.columns]
    else:
        population = Dbf5('population.dbf').to_dataframe()

    # force lowercase names
    main.columns = [x.lower() for x in main.columns]
    population.columns = [x.lower() for x in population.columns]

    # rename columns
    main = main.rename(columns = rename_main)
    population = population.rename(columns = rename_population)

    # hhid to int for merge
    main['hhid']       = main['hhid'].astype('float').astype('Int64')
    population['hhid'] = population['hhid'].astype('float').astype('Int64')

    population['relationship_to_hhm'] = population['relationship_to_hhm'].astype('int')
    population['ishhm'] = population['relationship_to_hhm'].apply(lambda x : x in hhm_ids[year])

    # simple restrictions to drop most nans
    population = population.query('ishhm == True')
    population = population.query('age >= 25').query('age <= 60')
    population['education'] = population['education'].astype(int).apply(lambda x : education[year][str(x)])

    main = main.reset_index(drop=True)
    population = population.reset_index(drop=True)

    # merge population into main dataframe
    df = main.merge(population, on='hhid', how='inner')
          #.merge(income, on='hhid', how='inner')

    if year in ['2008']:
        df['consumption_clothing'] = df['consumption_clothing_c']

    df[tofloat] = df[tofloat].astype(float)
    df['Y'] = int(year)
    df[toint] = df[toint].astype(int)

    os.chdir(interim)
    df.to_csv(year + '.csv', index=False)