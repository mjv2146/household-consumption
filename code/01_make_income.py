
"""
this notebook studies how asset possession varies with income
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys; sys.path.append('/home/mitch/school/data/mexico_enigh/src/')

import utils
import os

import statsmodels.stats.weightstats as ws

plotdir = '/home/mitch/school/data/mexico_enigh/fig/'
dicts= '/home/mitch/school/data/mexico_enigh/dicts/'

processed = '/home/mitch/Dropbox/data/mexico_enigh/processed/'
spec = '/home/mitch/Dropbox/data/mexico_enigh/spec/'
raw = '/home/mitch/Dropbox/data/mexico_enigh/raw/'

cpidir = '/home/mitch/Dropbox/data/cpi/'
os.chdir(cpidir)
cpi = pd.read_csv('cpi_monthly.csv', index_col=[0])
cpi = cpi.query('country == "MX"').reset_index(drop=True).drop(columns='country')
cpi = cpi.rename(columns={'PCPI_IX':'cpi'})
cpi['Y'] = cpi.time.apply(lambda x : int(x[:4]))
cpi['month'] = cpi.time.apply(lambda x : int(x[-2:]))
cpi = cpi.drop(columns='time')
cpi


os.chdir(dicts)
#from income_sources import income

income = [
    "P001",
    "P002",
    "P003",
    "P004",
    "P005",
    "P006",
    "P007",
    "P008",
    "P009",
    "P010",
    "P011",
    "P012",
    "P013",
    "P014",
    "P015",
    "P027",
    "P028"
]

dfs = []

years = ['1994', '1996']
from simpledbf import Dbf5
ids = ['hhid', 'hhmemberid']

for year in years:
    print(f'Making consumption for year {year}')
    os.chdir(raw + year)

    df = Dbf5('income.dbf').to_dataframe()
    df.columns = [x.lower() for x in df.columns]

    rename = {
        'folio':'hhid',
        'folioviv':'hhid',
        'num_ren':'hhmemberid',
        'clave':'category',
        'ing_tri':'quarterly_income',
        'meses':'months',
        'ing1' :'mes1',
        'ing2' :'mes2',
        'ing3' :'mes3',
        'ing4' :'mes4',
        'ing5' :'mes5',
        'ing6' :'mes6',
    }
    df = df.rename(columns = rename)
    df[ids] = df[ids].astype(int)

    pop = Dbf5('population.dbf').to_dataframe()
    pop.columns = [x.lower() for x in pop.columns]
    pop_rename = {
        'folio':'hhid',
        'folioviv':'hhid',
        'num_ren':'hhmemberid',
        'edad':'age'
    }
    pop = pop.rename(columns = pop_rename)
    pop = pop[['hhid', 'hhmemberid', 'age']]

    pop[ids] = pop[ids].astype(int)

    df = df.merge(pop, on=['hhid', 'hhmemberid'], how='inner')

    df_quarterly = df.copy()
    df = df.query('age >= 25').query('age <= 60').drop(columns = ['age', 'quarterly_income', 'empleo'])

    value_vars = ['mes1', 'mes2', 'mes3', 'mes4', 'mes5', 'mes6']
    id_vars = [x for x in df.columns if x not in value_vars]

    df = pd.melt(df, id_vars, value_vars, var_name='reference_month', value_name='income')
    df['reference_month'] = df['reference_month'].apply(lambda x : int(x[-1:]))
    df['base_month'] = df['months'].apply(lambda x : int(x[:2]))
    df['month'] = df['base_month'] - (df['reference_month'] - 1)
    df = df.drop(columns='base_month')

    df['Y'] = int(year)

    print(len(df))
    df = df.merge(cpi, on=['Y', 'month'], how='inner')

    df['income_nominal'] = df['income']
    df['income_real'] = df['income'] / df['cpi']

    out = df.groupby('hhid')[['income_real', 'income_nominal']].apply(np.sum).reset_index()

    os.chdir(spec + year)
    out.to_csv('income_guntin.csv', index=False)

    dfs.append(out)

interim = '/home/mitch/Dropbox/data/mexico_enigh/interim/'
processed = '/home/mitch/Dropbox/data/mexico_enigh/processed/'

merged = pd.concat(dfs, ignore_index=True) 
os.chdir(processed)
merged.to_csv('income.csv', index=False)




