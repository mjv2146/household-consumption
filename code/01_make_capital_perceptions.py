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

raw = '/home/mitch/Dropbox/data/mexico_enigh/raw/'
dicts = '/home/mitch/school/data/mexico_enigh/dicts/'
spec = '/home/mitch/Dropbox/data/mexico_enigh/spec/'
interim = '/home/mitch/Dropbox/data/mexico_enigh/interim/'
processed = '/home/mitch/Dropbox/data/mexico_enigh/processed/'


os.chdir(dicts)
income_cat = json_utils.load_json("capital_perceptions.json")
rename_income = json_utils.load_json("rename_income.json")

years = ['1994', '1996', '1998', '2000']

dfs_out = []

for year in years:
    os.chdir(raw + year)
    df = Dbf5('income.dbf').to_dataframe()
    df.columns = [x.lower() for x in df.columns]
    df = df.rename(columns = rename_income)
    df['category'] = df['category'].astype('str')

    df['hhid'] = df['hhid'].astype(str)
    df = df[df['hhid'].apply(lambda x : x.isnumeric())]
    hhid     = np.sort(df['hhid'].unique()).astype('int')

    # only keep capital income
    keep = income_cat.keys()
    # this is too restrictive
    df = df[df.category.apply(lambda x: str(x) in keep)]

    # note: need to add interest, etc

    df = df[['hhid', 'category', 'income']]
    df = df.sort_values(['hhid', 'category'])

    # problem: this excludes people if they do not receive income from it ...
    # makes sense !

    df['hhid'] = df['hhid'].astype('int')
    df['category'] = df['category'].astype('str')

    df = df[df['category'].apply(lambda x : x in income_cat.keys())]
    df['category'] = df['category'].apply(lambda x : income_cat[x]).astype('str')
    category = np.sort(df['category'].unique()).astype('str')

    df = df.groupby(['hhid', 'category'])['income'].apply(np.sum).reset_index()

    #new_index = pd.MultiIndex.from_product([hhid, category], names=['hhid', 'category'])
    #df = df.set_index(['hhid', 'category'])
    #df = df.reindex(new_index, fill_value=0.0).reset_index()

    df = df.sort_values(['hhid', 'category'])
    df['has'] = (df['income'] > 0) + 0

    df_has = df[['hhid', 'category', 'has']].pivot(index='hhid', columns='category', values='has').reset_index()

    df_has = df_has.astype(np.float)
    df_has[np.isnan(df_has)] = 0.0
    df_has['hhid'] = df_has['hhid'].astype(int)

    os.chdir(spec + year)
    df_has.to_csv('capital_income.csv', index=False)

    dfs_out.append(df_has)


df_merged = pd.concat(dfs_out, ignore_index=True)
os.chdir(processed)
df_merged.to_csv('capital_income.csv', index=False)
