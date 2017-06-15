# -*- coding: utf-8 -*-
"""
Created on Tue May 30 14:16:21 2017

Regressions of price of housing in GTA

@author: jason
"""

import numpy as np
import pysal as ps
import pandas as pd
import matplotlib.pyplot as plt
import csv

TYPE_DICT = {'C':'Condo', 'H':'House', 'T':'Townhouse'}
X_LISTS = [['AveIncome','PTransit','PActive','SQFT','EmpCode','DistCBD', 'Month']
           ,['MedIncome','PTransit','PActive','SQFT','EmpCode','DistCBD', 'Month']
            ,['AveIncomeC','PTransit','PActive','SQFT','EmpCode','DistCBD', 'Month']
            ,['MedIncomeC','PTransit','PActive','SQFT','EmpCode','DistCBD', 'Month']]

# Read-in each of the input data files
# All files are sorted in increasing alphabetic by TREB zone
regIn = pd.read_csv('./regressInputs.csv')
shp = ps.open('./TREB-Zones-Data.shp')

lag = len(regIn['TREBID'].unique())*len(regIn['Month'].unique())
per = len(regIn['YearMonth'].unique())

# Spatial weights using a Rook-based contiguity method
w = ps.weights.Rook.from_shapefile('./TREB-Zones-Data.shp', None, False, repeat = per)
w.transform = 'r'

#with open('regressBest1.csv', 'w') as file:
#    myWriter = csv.writer(file, delimiter=',',
#                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    myWriter.writerow(['Type','YearMonth','yVal','xModel','pseudoR2'])
for k,v in TYPE_DICT.items():   
    for i, yVal in enumerate(['RelAvePrice','RelMedPrice']):
        for j, xList in enumerate(X_LISTS):
            data = regIn[(regIn['Type']==k)]
            y_name = "PRICE"+"_"+v+"_"+"_"+str(i)+"_"+str(j)
            x = data[xList].as_matrix()
            y = data[yVal].as_matrix()
            y = y[:,np.newaxis]
            mllag = ps.spreg.ml_lag_sdpd.ML_Lag_SDPD(y,lag,x,w,name_y=y_name)