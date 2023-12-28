"""
This file merges yearly datasets into a pseudo-panel dataset
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

#years = ['1992', '1994', '1996', '1998', '2000', '2002', '2004', '2006', '2008']
years = ['1994', '1996', '1998', '2000']

interim = '/home/mitch/Dropbox/data/mexico_enigh/interim/'
processed = '/home/mitch/Dropbox/data/mexico_enigh/processed/'

os.chdir(interim)

dfs = []
for year in years:
    dfs.append(pd.read_csv(year + '.csv'))

df = pd.concat(dfs, ignore_index=True) 
os.chdir(processed)
df.to_csv('data.csv', index=False)
