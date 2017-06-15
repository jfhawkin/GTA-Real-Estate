# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 22:18:30 2017

@author: jason
"""

import numpy as np
import pysal as ps
import pandas as pd
import matplotlib.pyplot as plt
import collections

TYPE_TUPLE = [('C','Condo'), ('H','House'), ('T','Townhouse')]
TYPE_DICT = collections.OrderedDict(TYPE_TUPLE)
# Prices measured in $10,000, price per sqft measured in $/sqft, and income measured in $10,000
# Population density measured in persons per sqkm
X_LISTS = [['AveIncomeC','PActive','SQFT','EmpCode','DistCBD', 'PopDens', 'SubwayAdj','StreetCarAdj','GoTrainAdj','SW','NW','NE']]
Y_LIST = ['RelAvePrice']

# Read-in each of the input data files
# All files are sorted in increasing alphabetic by TREB zone
regIn = pd.read_csv('./regressInputs.csv')
shp = ps.open('./TREB-Zones-Data.shp')

# Spatial weights using a Rook-based contiguity method
w = ps.weights.Rook.from_shapefile('./TREB-Zones-Data.shp')
w.transform = 'r'

ymList = regIn['YearMonth'].unique()

with open("Model_Results3.txt", "w") as rst_file, open("Beta_Results3.txt", "w") as beta_file:
    for i, yVar in enumerate(Y_LIST):
        for j, xList in enumerate(X_LISTS):
            seriesT = [('C',[]),('H',[]),('T',[])]
            seriesT = collections.OrderedDict(seriesT)
            seriesD = []
            for k,v in TYPE_DICT.items():
                series = {}
                sD = []
                R2 = []
                SC = []
                for ym in ymList:
                    yrTxt = str(ym)[:4]
                    data = regIn[(regIn['Type']==k)&(regIn['YearMonth']==ym)]
                    y_name = "PRICE"
                    x = data[xList].as_matrix()
                    y = data[yVar].as_matrix()
                    y = y[:,np.newaxis]
                    mllag = ps.spreg.ml_lag.ML_Lag(y,x,w,name_y=y_name, name_x=xList)
                    sD.append(mllag.betas[5])
                    for b in range(0,len(xList)):
                        if mllag.z_stat[b+1][1]<=0.05:
                            tmp = series.get(b,[[],[]])
                            tmp[0].append(yrTxt)
                            tmp[1].extend(mllag.betas[b+1])
                            series[b] = tmp
                    # Write the results of the regression to a text file for each
                    # pair of dependent and independent variables, for each structure
                    # type and year/month pair
                    rst_file.write("{0}_{1}_{2}_{3}".format(str(i),str(j),k,str(ym)))
                    rst_file.write(mllag.summary)
                    rst_file.write("\n")
                    R2.append(mllag.pr2)
                    SC.append(mllag.schwarz)
                    print(mllag.rho)
                #print(np.mean(R2))
                #print(np.mean(SC))
                seriesT[k] = series
                seriesD.append(sD)
            
            for b,xVar in enumerate(xList):
                fig, ax = plt.subplots()
                plt.tight_layout()
                numC = 0
                numH = 0
                numT = 0
                if b in seriesT['C'].keys():
                    numC = str(len(seriesT['C'][b][0]))
                    ax.plot(seriesT['C'][b][0],seriesT['C'][b][1],'ro',label='Condos N={0}'.format(numC))
                    ax.set_xlim([1995,2020])
                    beta_file.write("{0}_{1}_C_{2}".format(str(i),str(j),str(b)))
                    x = np.array(seriesT['C'][b][1])
                    x = x[:,np.newaxis]
                    y = np.array([int(w) for w in seriesT['C'][b][0]])
                    y = y[:,np.newaxis]
                    if x.shape[0]==x.shape[1] or y[0]==y[1]:
                        beta_file.write("Nothing")
                    else:
                        ols = ps.spreg.OLS(x, y)
                        beta_file.write(ols.summary)
                        
                    beta_file.write("\n")
                if b in seriesT['H'].keys():
                    numH = str(len(seriesT['H'][b][0]))
                    ax.plot(seriesT['H'][b][0],seriesT['H'][b][1],'bo',label='Houses N={0}'.format(numH))
                    ax.set_xlim([1995,2020])
                    beta_file.write("{0}_{1}_H_{2}".format(str(i),str(j),str(b)))
                    x = np.array(seriesT['H'][b][1])
                    x = x[:,np.newaxis]
                    y = np.array([int(w) for w in seriesT['H'][b][0]])
                    y = y[:,np.newaxis]
                    if x.shape[0]==x.shape[1] or y[0]==y[1]:
                        beta_file.write("Nothing")
                    else:
                        ols = ps.spreg.OLS(x, y)
                        beta_file.write(ols.summary)
                    beta_file.write("\n")
                if b in seriesT['T'].keys():
                    numT = str(len(seriesT['T'][b][0]))
                    ax.plot(seriesT['T'][b][0],seriesT['T'][b][1],'go',label='Townhouses N={0}'.format(numT))
                    ax.set_xlim([1995,2020])
                    beta_file.write("{0}_{1}_T_{2}".format(str(i),str(j),str(b)))
                    x = np.array(seriesT['T'][b][1])
                    x = x[:,np.newaxis]
                    y = np.array([int(w) for w in seriesT['T'][b][0]])
                    y = y[:,np.newaxis]
                    # If there is only one entry then kluge it!
                    if x.shape[0]==x.shape[1] or y[0]==y[1]:
                        beta_file.write("Nothing")
                    else:
                        ols = ps.spreg.OLS(x, y)
                        beta_file.write(ols.summary)
                    beta_file.write("\n")
                ax.legend(loc='upper right')
                ax.set_xlabel('Year')
                ax.set_ylabel('{0} vs {1}'.format(yVar,xVar))
                plt.savefig('{0}_{1}.png'.format(yVar,xVar),bbox_inches='tight')
                
            fig, ax = plt.subplots()
            plt.tight_layout()
            yrs = regIn['Year'].unique()
            yrs = np.repeat(yrs,2)[:-1]
            N = str(len(yrs))
            ax.plot(yrs,seriesD[0],'ro',label='Condos N={0}'.format(N))
            ax.set_xlim([1995,2020])
            ax.plot(yrs,seriesD[1],'bo',label='Houses N={0}'.format(N))
            ax.set_xlim([1995,2020])
            ax.plot(yrs,seriesD[2],'go',label='Townhouses N={0}'.format(N))
            ax.set_xlim([1995,2020])
            ax.legend(loc='upper right')
            ax.set_xlabel('Year')
            ax.set_ylabel('{0} vs Dist'.format(yVar))
            plt.savefig('{0}_DIST_Years.png'.format(yVar),bbox_inches='tight')
rst_file.close()
beta_file.close()            