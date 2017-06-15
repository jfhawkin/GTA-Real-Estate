# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 15:45:33 2017

@author: jason
"""
import matplotlib.pyplot as plt
import matplotlib.mlab as ml
from matplotlib.colors import BoundaryNorm
import pandas as pd
import numpy as np

# Read-in each of the input data files
# Own and rent data for relative price (wrt its class) and distance from CBD
f1 = pd.read_csv('./ExportData1.csv')
# Own data for binned prices
f2 = pd.read_csv('./ExportData2.csv')
# Own data for total price with distance from CBD
f3 = pd.read_csv('./ExportData3.csv')
# Own data for price/sqft price (wrt its class) for X,Y distance from CBD
f4 = pd.read_csv('./ExportData4.csv')
# Data for XY distance/SQFT price analysis
f4 = f4[(f4['Price']>0) & (f4['Price']<1000000)]
x6 = f4['X']
y6 = f4['Y']
z6 = f4['Price']

origin = 'lower'

deciles = []
i = 0.1

while i <=1:
    deciles.append(f4['Price'].quantile(i))
    i+=0.1

xmin, xmax = x6.min(), x6.max()
ymin, ymax = y6.min(), y6.max()

xi = np.linspace(xmin, xmax, 1000)
yi = np.linspace(ymin, ymax, 1000)
zi = ml.griddata(x6, y6, z6, xi, yi, interp='linear')
fig6, ax6 = plt.subplots()
cmap = plt.get_cmap('PiYG')
norm = BoundaryNorm(boundaries = deciles, ncolors=256)

cf = ax6.contourf(xi, yi, zi, norm=norm, cmap='RdBu_r')

plt.colorbar(cf, ax=ax6) 
plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax)
plt.savefig('contour_test.png')