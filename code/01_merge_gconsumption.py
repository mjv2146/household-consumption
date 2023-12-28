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

#years = ['1992', '1994', '1996', '1998', '2000', '2002', '2004', '2006', '2008']
years = [ '1994', '1996']
raw  = '/home/mitch/Dropbox/data/mexico_enigh/raw/'
spec = '/home/mitch/Dropbox/data/mexico_enigh/spec/'
processed = '/home/mitch/Dropbox/data/mexico_enigh/processed/'

dfs = []

for year in years:
    os.chdir(spec + year)
    df = pd.read_csv('consumption_guntin.csv')
    df['Y'] = year
    dfs.append(df)

df = pd.concat(dfs)

os.chdir(processed)
df.to_csv('consumption_guntin.csv', index=False)


    