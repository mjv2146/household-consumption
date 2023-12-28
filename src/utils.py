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

def residualize_income_singleyear(data):
    """Residualize income measure of predictable components 
    Predictable components:
        sex
        education
        age
        hh_size
        location_size

    lhs includes log_income: log of whatever income measure is used
    weights are given by 'weight'

    """


    formula = 'log_income ~ ' + 'Y' + '+' + Z + '+' + D 
    formula =  'Y' + '+' + Z + '+' + D 
    X = dmatrix(formula, data)
    model = LinearRegression(fit_intercept=False)
    fit = model.fit(X, data['log_income'], data['weight'])

    #model = smf.wls(formula, data, weights=data['weight'], const=False).fit()
    #print(model.summary)
    return  model.resid

def residualize_y(data, y):
    """Residualize income measure of predictable components 
    Predictable components:
        sex
        education
        age
        hh_size
        location_size

    lhs includes log_income: log of whatever income measure is used
    weights are given by 'weight'

    """

    formula = y +  ' ~ ' + 'Y' + '+' + Z 
    model = smf.wls(formula, data, weights=data['weight']).fit()
    print(model.summary())
    return  model.resid


def residualize_income(data):
    """Residualize income measure of predictable components 
    Predictable components:
        sex
        education
        age
        hh_size
        location_size

    lhs includes log_income: log of whatever income measure is used
    weights are given by 'weight'

    """

    formula = 'log_income ~ ' + '+' + 'Y' + '+' + D + '+' + Z 
    #model = smf.wls(formula, data, weights=data['weight']).fit()
    model = smf.glm(formula, data, freq_weights=data['weight']).fit()
    print(model.summary())
    return  model.resid_pearson

def residualize_consumption(data):
    """Residualize income measure of predictable components 
    Predictable components:
        sex
        education
        age
        hh_size
        location_size

    lhs includes log_consumption: log of whatever consumption measure is used
    weights are given by 'weight'
    """

    #formula = 'log_consumption ~ ' + '+' + D + '+' + Z 
    formula = 'log_consumption ~ ' + '+' + 'Y' + '+' + D + '+' + Z 
    #model = smf.wls(formula, data, weights=data['weight']).fit()
    model = smf.glm(formula, data, freq_weights=data['weight']).fit()
    print(model.summary())
    return  model.resid_pearson

def get_deciles(x, weights=None):
    stats = ws.DescrStatsW(x, weights=weights)

    deciles =  np.arange(0.1, 1.1, .1)
    income_deciles = stats.quantile(deciles).values
    x_deciles = np.array([np.argmax(income_deciles > xi) for xi in x])
    return x_deciles + 1

def get_quartiles(x, weights=None):
    stats = ws.DescrStatsW(x, weights=weights)

    deciles =  np.arange(0.25, 1.25, .25)
    income_deciles = stats.quantile(deciles).values
    x_deciles = np.array([np.argmax(income_deciles > xi) for xi in x])
    return x_deciles + 1
   
def indicator_by_decile(data, metric, key, weight):
    metric_decile = get_deciles(data[metric], data[weight])
    deciles = np.sort(np.unique(metric_decile))
    key_by_decile = np.ones_like(deciles).astype('object')

    ii = 0
    for decile in deciles:
        data2 = data.loc[metric_decile == decile, [key, weight]].dropna()
        stats = ws.DescrStatsW(data2[key], weights=data2[weight])
        key_by_decile[ii] = stats.mean
        ii +=1
    return key_by_decile 

def clean_pobalicion(data):
    toint = ['relationship_to_hhm', 'sex', 'age', 'type_of_education', 'education', 'education_technical']
    data[toint] = data[toint].astype('int')


    data = data.query('relationship_to_hhm == 1')
    return data

def clean_concen(data):
    toint = ['location_size']
    data[toint] = data[toint].astype('int')

    income = ['salary_income', 'business_income', 'rental_income', 'transfers_income']
    data['income'] = data[income].sum(axis=1)
    data['log_income'] = np.log(data['income'])

    consumption = ['consumption_food', 'consumption_clothing', 'consumption_health', 'consumption_personal']
    data['consumption'] = data[consumption].sum(axis=1)
    data['log_consumption'] = np.log(data['consumption'])
    return data

def clean_ingresos(data):
    return data

def drop(data):
    data = (data.query('relationship_to_hhm == 1')
            .query('income > 0')
            .query('consumption > 0'))
    data = data.query('age >= 25')
    data = data.query('age <= 60')
    data = data[data['location_size'].apply(lambda x : x not in [4.0, 5.0])]

    consumption_to_income = ws.DescrStatsW(data['consumption'] / data['income'], weights=data['weight'])
    consumption_to_income_005 = consumption_to_income.quantile(0.005)
    consumption_to_income_995 = consumption_to_income.quantile(0.995)
    data = data[data['consumption'] / data['income'] > consumption_to_income_005.values[0]]
    data = data[data['consumption'] / data['income'] < consumption_to_income_995.values[0]]

    return data

def logit_residualize(df, y, Z, weight='weight'):
    X = patsy.dmatrix(Z, df, return_type='dataframe')

    model = sm.GLM(df[y], X, freq_weights=df[weight], family=sm.families.Binomial())
    fit = model.fit()
    resid = fit.resid_pearson
    return resid, model

from statsmodels.genmod.families.links import probit
def probit_residualize(df, y, Z, weight='weight'):
    X = patsy.dmatrix(Z, df, return_type='dataframe')

    model = sm.GLM(df[y], X, freq_weights=df[weight], family=sm.families.Binomial(probit()))
    fit = model.fit()
    resid = fit.resid_pearson
    return resid, model
