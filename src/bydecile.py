import numpy as np
import pandas as pd

import sys; sys.path.append('/home/mitch/util/python/')
sys.path.append('/home/mitch/school/data/mexico_enigh/src')

def income_consumption_by_decile(data):
    """
    Returns average consumption and average income within each income decile

    Requires: 'income', 'consumption', and 'weight'

    """
    average_income_by_decile = utils.indicator_by_decile(data, 'income', 'income', 'weight')
    average_consumption_by_decile = utils.indicator_by_decile(data, 'income', 'consumption', 'weight')
    return average_income_by_decile, average_consumption_by_decile

def elasticity_by_decile(consumption_1, consumption_0, income_1, income_0):
    elasticity = ((consumption_1 - consumption_0) / consumption_0) / ((income_1 - income_0) / income_0)
    return elasticity
