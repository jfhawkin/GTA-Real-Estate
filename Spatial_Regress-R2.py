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
X_LIST = ['DistCBD']

# Read-in each of the input data files
# All files are sorted in increasing alphabetic by TREB zone
regIn = pd.read_csv('./regressInputs.csv')
shp = ps.open('./TREB-Zones-Data.shp')

# Spatial weights using a Rook-based contiguity method
w = ps.weights.Rook.from_shapefile('./TREB-Zones-Data.shp')
w.transform = 'r'

ymList = regIn['YearMonth'].unique()

series1 = []

for k,v in TYPE_DICT.items():
    s1 = []
    s2 = []
    s3 = []
    for ym in ymList:
        data = regIn[(regIn['Type']==k)&(regIn['YearMonth']==ym)]
        y_name = "PRICE"
        x = data[X_LIST].as_matrix()
        y = data['RelAvePrice'].as_matrix()
        y = y[:,np.newaxis]
        mllag = ps.spreg.ml_lag.ML_Lag(y,x,w,name_y=y_name, name_x=X_LIST)
        s1.append(mllag.betas[1])
    series1.append(s1)
    
yrs = regIn['Year'].unique()
yrs = np.repeat(yrs,2)[:-1]

fix, ax = plt.subplots()        
ax.plot(yrs,series1[0],'ro',label='Condos')
ax.plot(yrs,series1[1],'bo',label='Houses')
ax.plot(yrs,series1[2],'go',label='Townhouses')
ax.legend(loc='upper right')
ax.set_xlabel('Year')
ax.set_ylabel('Relative Price wrt Distance from CBD (km)')
plt.savefig('Price_Distance.png')