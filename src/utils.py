import statsmodels.formula.api as smf
import statsmodels.stats.weightstats as ws
import numpy as np
from patsy import dmatrix
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import patsy

durables = ['I', 'K', 'L', 'Q', 'M', 'T']
# TODO: what is T?

def isdurable(x):
    return any([y in x for y in durables])

Z = 'age + I(age**2) + C(sex) + C(location_size)'
#Z = 'age + I(age**2) + C(sex) + C(education) + C(hh_size) + C(location_size)'
#D = 'Y:C(education) + Y:C(sex)'
#D = 'Y + Y:C(sex)'
D = 'Y'