# -*- coding: utf-8 -*-
"""
Created on Tue May 30 14:16:21 2017

Regressions of price of housing in GTA

@author: jason
"""

import numpy as np
import pysal as ps
import pandas as pd
from pysal.contrib.viz import mapping as maps
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import csv

TYPE_DICT = {'C':'Condo', 'H':'House', 'T':'Townhouse'}
X_LISTS = [['AveIncome','PTransit','PActive','SQFT','EmpCode','DistCBD'],
           ['MedIncome','PTransit','PActive','SQFT','EmpCode','DistCBD']
            ,['AveIncomeC','PTransit','PActive','SQFT','EmpCode','DistCBD']
            ,['MedIncomeC','PTransit','PActive','SQFT','EmpCode','DistCBD']]

# Read-in each of the input data files
# All files are sorted in increasing alphabetic by TREB zone
regIn = pd.read_csv('./regressInputs.csv')
shp = ps.open('./TREB-Zones-Data.shp')

# Spatial weights using a Rook-based contiguity method
w = ps.weights.Rook.from_shapefile('./TREB-Zones-Data.shp')
w.transform = 'r'

ymList = regIn['YearMonth'].unique()

with open('regressBest1.csv', 'w') as file:
    myWriter = csv.writer(file, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    myWriter.writerow(['Type','YearMonth','yVal','xModel','pseudoR2'])
    for k,v in TYPE_DICT.items():   
        for ym in ymList:
            for i, yVal in enumerate(['RelAvePrice','RelMedPrice']):
                for j, xList in enumerate(X_LISTS):
                    data = regIn[(regIn['Type']==k)&(regIn['YearMonth']==ym)]
                    y_name = "PRICE"+"_"+v+"_"+str(ym)+"_"+str(i)+"_"+str(j)
                    x = data[xList].as_matrix()
                    y = data[yVal].as_matrix()
                    y = y[:,np.newaxis]
                    mllag = ps.spreg.ml_lag.ML_Lag(y,x,w,name_y=y_name)
                    pseduoR = mllag.pr2
                    mllag.rho
                    myWriter.writerow([v,ym,yVal,j,pseduoR])
            


