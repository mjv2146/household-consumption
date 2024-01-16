"""
This file creates household datasets at the yearly level
using the main, population, and income subdatasets

"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sys; 
sys.path.append('/home/mitch/school/data/mexico_enigh/src/')
sys.path.append('/home/mitch/school/data/mexico_enigh/dicts/')
sys.path.append('/home/mitch/util/python/')
import json_utils

import utils
import os

from simpledbf import Dbf5

dicts = '/home/mitch/school/data/mexico_enigh/dicts/'
os.chdir(dicts)
#from consumption import span, specific
import consumption
#from consumption import span, specific
from consumption import food, household_cleaning, personal_care, recreation, communications_fuel, medical
from consumption import whole

span = [food, household_cleaning, personal_care, recreation, communications_fuel, medical]
span = [food]


#years = ['1992', '1994', '1996', '1998', '2000', '2002', '2004', '2006', '2008']
years = ['1994', '1996']
raw  = '/home/mitch/Dropbox/data/mexico_enigh/raw/'
spec = '/home/mitch/Dropbox/data/mexico_enigh/spec/'

for year in years:
    print(f'Making consumption for year {year}')
    os.chdir(raw + year)

    df = Dbf5('expenses.dbf').to_dataframe()
    df.columns = [x.lower() for x in df.columns]

    rename = {
        'folio':'hhid',
        'folioviv':'hhid',
        'clave':'category',
        'gas_tri':'consumption',
        'lu_com':'shop_place'
    }

    df = df.rename(columns=rename)
    df = df[['hhid', 'category', 'consumption']]

    keep = []

    in_whole = df.category.apply(lambda x : str(x)[:1] in whole)
    keep += df.category[in_whole].unique().tolist()

    local_span = (
        food[year] + 
        household_cleaning[year] + 
        personal_care[year] + 
        recreation[year] + 
        communications_fuel[year] + 
        medical[year] 
    )

        
    for s in local_span:
        main = s[0]
        min = s[1]
        max = s[2]

        ints = np.arange(min, max+1)
        keep += [main + str(x).zfill(3) for x in ints]

    #keep += specific
        
    tokeep = df.category.apply(lambda x : x in keep)
    df = df.loc[tokeep, :]

    consumption_by_hh = df.groupby(['hhid'])['consumption'].sum().reset_index()

    os.chdir(spec + year)
    consumption_by_hh.to_csv('consumption_guntin.csv', index=False)