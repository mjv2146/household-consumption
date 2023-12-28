"""

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

raw       = '/home/mitch/Dropbox/data/mexico_enigh/raw/'
dicts     = '/home/mitch/school/data/mexico_enigh/dicts/'
spec      = '/home/mitch/Dropbox/data/mexico_enigh/spec/'
interim   = '/home/mitch/Dropbox/data/mexico_enigh/interim/'
processed = '/home/mitch/Dropbox/data/mexico_enigh/processed/'


os.chdir(dicts)
expend_cat = json_utils.load_json("capital_expenditures.json")
rename_capital_expenditures = json_utils.load_json("rename_capital_expenditures.json")

years = ['1994', '1996', '1998', '2000']

dfs_out = []

for year in years:
    os.chdir(raw + year)
    df = Dbf5('capital_expenditures.dbf').to_dataframe()
    df.columns = [x.lower() for x in df.columns]
    df = df.rename(columns = rename_capital_expenditures)
    df = df.sort_values(['hhid', 'category'])
    hhid     = np.sort(df['hhid'].unique()).astype('int')

    df['hhid'] = df['hhid'].astype(str)
    df = df[df['hhid'].apply(lambda x : x.isnumeric())]

    df['category'] = df['category'].astype('str')
    df = df[df['category'].apply(lambda x : x in expend_cat.keys())]
    df['category'] = df['category'].apply(lambda x : expend_cat[x])

    category = expend_cat.values()

    df = df.groupby(['hhid', 'category'])['expenses'].apply(np.sum).reset_index()

    #new_index = pd.MultiIndex.from_product([hhid, category], names=['hhid', 'category'])
    #df = df.set_index(['hhid', 'category'])
    #df = df.reindex(new_index, fill_value=np.nan)#.reset_index()

    df = df.sort_values(['hhid', 'category'])
    df['has'] = (df['expenses'] > 0) + 0
    df_has = df[['hhid', 'category', 'has']].pivot(index='hhid', columns='category', values='has').reset_index()

    df_has = df_has.astype(np.float)
    df_has[np.isnan(df_has)] = 0.0
    df_has['hhid'] = df_has['hhid'].astype(int)

    os.chdir(spec + year)
    df_has.to_csv('capital_expenditures.csv', index=False)

    dfs_out.append(df_has)

df_merged = pd.concat(dfs_out, ignore_index=True)
os.chdir(processed)
df_merged.to_csv('capital_expenditures.csv', index=False)