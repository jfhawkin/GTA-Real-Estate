# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 22:18:30 2017

@author: jason
"""

import numpy as np
import pysal as ps
import pandas as pd
from pysal.contrib.viz import mapping as maps
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

TYPE_DICT = {'C':'Condo', 'H':'House', 'T':'Townhouse'}
X_LIST = ['AveIncome','PTransit','PActive','SQFT','EmpCode','DistCBD', 'Month']

# Read-in each of the input data files
# All files are sorted in increasing alphabetic by TREB zone
regIn = pd.read_csv('./regressInputs.csv')

for k,v in TYPE_DICT.items():
    s1 = []
    s2 = []
    data = regIn[(regIn['Type']==k)]
    y_name = "PRICE"
    x = data[X_LIST].as_matrix()
    x[:,0] = x[:,0]/10**5
    x[:,3] = x[:,3]/10**2
    y = data['RelAvePrice'].as_matrix()
    y = y[:,np.newaxis]
    ols = ps.spreg.ols.OLS(y, x, name_y=y_name, name_x=X_LIST)
    
summary = ols.summary
print(summary)

        