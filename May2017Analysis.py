# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 13:09:16 2017

Analysis of May, 2017 Real Estate Data for houses, condos, and townhouses

@author: jason
"""

import matplotlib.pyplot as plt
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

# Data for ownership analysis
dataOwn = f1[(f1['Tenure']=='O')&(f1['RelPrice']>=0.25)&(f1['RelPrice']<=4.00)]
dataOwnS = f1[(f1['Tenure']=='O')&(f1['RelPriceSQFT']>=0.25)&(f1['RelPriceSQFT']<=4.00)]
dataOwnR = f1[(f1['Tenure']=='O')&(f1['RelPriceRoom']>=0.25)&(f1['RelPriceRoom']<=4.00)]

x1Own = dataOwn['AbsDistRoundkm']
y1Own = dataOwn['RelPrice']
x1OwnS = dataOwnS['AbsDistRoundkm']
y1OwnS = dataOwnS['RelPriceSQFT']
x1OwnR = dataOwnR['AbsDistRoundkm']
y1OwnR = dataOwnR['RelPriceRoom']

# Fit linear plots to data
fit1 = np.polyfit(x1Own, y1Own, 1)
fit2 = np.polyfit(x1OwnS, y1OwnS, 1)
fit3 = np.polyfit(x1OwnR, y1OwnR, 1)
fit_f1 = np.poly1d(fit1)
fit_f2 = np.poly1d(fit2)
fit_f3 = np.poly1d(fit3)

fig1, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
ax1.plot(x1Own, y1Own, 'bo', x1Own, fit_f1(x1Own), '--k')
ax2.plot(x1OwnS, y1OwnS, 'go', x1OwnS, fit_f1(x1OwnS), '--k')
ax3.plot(x1OwnR, y1OwnR,'ro', x1OwnR, fit_f1(x1OwnR), '--k')
# Fine-tune figure; make subplots close to each other and hide x ticks for
# all but bottom plot.
fig1.subplots_adjust(hspace=0.2)
plt.setp([a.get_xticklabels() for a in fig1.axes[:-1]], visible=False)
plt.xlabel('Distance from CBD (km)')
ax1.set_ylabel('Total')
ax2.set_ylabel('SQFT')
ax3.set_ylabel('Rooms')
fig1.savefig('Price_Dist_Own.png')

# Data for rental analysis
dataRent = f1[(f1['Tenure']=='R')&(f1['RelPrice']>=0.25)&(f1['RelPrice']<=4.00)]
dataRentS = f1[(f1['Tenure']=='R')&(f1['RelPriceSQFT']>=0.25)&(f1['RelPriceSQFT']<=4.00)]
dataRentR = f1[(f1['Tenure']=='R')&(f1['RelPriceRoom']>=0.25)&(f1['RelPriceRoom']<=4.00)]

x1Rent = dataRent['AbsDistRoundkm']
y1Rent = dataRent['RelPrice']
x1RentS = dataRentS['AbsDistRoundkm']
y1RentS = dataRentS['RelPriceSQFT']
x1RentR = dataRentR['AbsDistRoundkm']
y1RentR = dataRentR['RelPriceRoom']

# Fit linear plots to data
fit1 = np.polyfit(x1Rent, y1Rent, 1)
fit2 = np.polyfit(x1RentS, y1RentS, 1)
fit3 = np.polyfit(x1RentR, y1RentR, 1)
fit_f1 = np.poly1d(fit1)
fit_f2 = np.poly1d(fit2)
fit_f3 = np.poly1d(fit3)

fig3, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
ax1.plot(x1Rent, y1Rent, 'bo', x1Rent, fit_f1(x1Rent), '--k')
ax2.plot(x1RentS, y1RentS, 'go', x1RentS, fit_f1(x1RentS), '--k')
ax3.plot(x1RentR, y1RentR,'ro', x1RentR, fit_f1(x1RentR), '--k')
# Fine-tune figure; make subplots close to each other and hide x ticks for
# all but bottom plot.
fig3.subplots_adjust(hspace=0.2)
plt.setp([a.get_xticklabels() for a in fig3.axes[:-1]], visible=False)
plt.xlabel('Distance from CBD (km)')
ax1.set_ylabel('Total')
ax2.set_ylabel('SQFT')
ax3.set_ylabel('Rooms')

fig3.savefig('Price_Dist_Rent.png')

# Data for Housing Price Category Analysis
xBin = f2.index.values.tolist()
xLabels = f2['CustomBins']
yBin = f2['Count']

fig4, ax4 = plt.subplots()
rects1 = ax4.bar(xBin, yBin)
ax4.set_xticks(xBin)
ax4.set_xticklabels(xLabels)
ax4.set_ylabel('Count of Listings')
fig4.savefig('Price_Bins.png')

#def autolabel(rects):
#    """
#    Attach a text label above each bar displaying its height
#    """
#    for rect in rects:
#        height = rect.get_height()
#        ax4.text(rect.get_x() + rect.get_width()/2., 1.05*height,
#                '%d' % int(height),
#                ha='center', va='bottom')
#
#autolabel(rects1)

# Data for distance/price analysis
x5 = f3['AbsDistRound5km']
y5 = f3['Price']

minVals = f3.groupby(['AbsDistRound5km'])['Price'].min()
maxVals = f3.groupby(['AbsDistRound5km'])['Price'].max()
meanVals = f3.groupby(['AbsDistRound5km'])['Price'].mean()

fig5, ax5 = plt.subplots()
ax5.semilogy(x5, y5, 'ko', label = 'Prices at Distances')
ax5.semilogy(minVals.index, minVals, '--r', label = 'Minimum Price')
ax5.semilogy(maxVals.index, maxVals, '--b', label = 'Maximum Price')
ax5.semilogy(meanVals.index, meanVals, '--g', label = 'Mean Price')
ax5.set_xlabel('Distance from CBD (5km Bins)')
ax5.set_ylabel('Housing Price ($)')
ax5.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
fig5.savefig('Price_Dist.png',bbox_inches='tight')