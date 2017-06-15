# -*- coding: utf-8 -*-
"""
Created on Mon May 22 09:14:44 2017
Markov Chain Process for Toronto Real Estate Data
@author: jason
"""
import pysal as ps
import numpy as np

# Read-in each of the input data files
fd = ps.open('./DetachedMarkov.csv')
fs = ps.open('./SemiMarkov.csv')
ft = ps.open('./TownMarkov.csv')
fc = ps.open('./CondoMarkov.csv')

# Define the year month categories for the data array
yr_month = [str(yr)+str(month) for yr in range(1996,2018) for month in [4,9]]
yr_month = yr_month[:-1]

rpiD = np.array([fd.by_col[str(y)] for y in yr_month])
rpiS = np.array([fs.by_col[str(y)] for y in yr_month])
rpiT = np.array([ft.by_col[str(y)] for y in yr_month])
rpiC = np.array([fc.by_col[str(y)] for y in yr_month])
rpiD = rpiD.transpose()
rpiS = rpiS.transpose()
rpiT = rpiT.transpose()
rpiC = rpiC.transpose()


# Spatial weights using a Rook-based contiguity method
w = ps.weights.Rook.from_shapefile('../TREB-Zones-Dissolve.shp')
w.transform = 'r'

# Spatial Markov with 5 classes for housing price (Detached, Semi-Detached, Townhouse, Condo)
smD = ps.Spatial_Markov(rpiD, w, fixed = True, k=5)
smS = ps.Spatial_Markov(rpiS, w, fixed = True, k=5)
smT = ps.Spatial_Markov(rpiT, w, fixed = True, k=5)
smC = ps.Spatial_Markov(rpiC, w, fixed = True, k=5)

# Print results for each structure class
# Results for Detached Homes
print("Results for Detached Home Analysis:")
# Pooled over space and time global transition probabilities
print("Global Transition Probablilities:")
print(smD.p)
# Transition probabilities given condition of neighbours
print("Conditioned Transition Probablilities:")
for p in smD.P:
    print(p)
print("Steady State Long Run Probabilities:")
print(smD.S)
# Time in year/months to enter a quintile, conditioned on neighbours quintiles
# Ex. One in the 1st quintile to return to 1st quintile or to enter 4th quintile
# Each array is referenced to the neighbour number, each column is the time to enter that quintile,
# and each row of that array is the origin quintile
print("First Mean Passage Time:")
for f in smD.F:
    print(f)

# Results for Semi-Detached Homes
print("\n")
print("Results for Semi-Detached Home Analysis:")
print("Global Transition Probablilities:")
print(smS.p)
print("Conditioned Transition Probablilities:")
for p in smS.P:
    print(p)
print("Steady State Long Run Probabilities:")
print(smS.S)
print("First Mean Passage Time:")
for f in smS.F:
    print(f)
    
# Results for Townhouses
print("\n")
print("Results for Townhouse Analysis:")
print("Global Transition Probablilities:")
print(smT.p)
print("Conditioned Transition Probablilities:")
for p in smT.P:
    print(p)
print("Steady State Long Run Probabilities:")
print(smT.S)
print("First Mean Passage Time:")
for f in smT.F:
    print(f)
    
# Results for Condos
print("\n")
print("Results for Condo Analysis:")
print("Global Transition Probablilities:")
print(smC.p)
print("Conditioned Transition Probablilities:")
for p in smC.P:
    print(p)
print("Steady State Long Run Probabilities:")
print(smC.S)
print("First Mean Passage Time:")
for f in smC.F:
    print(f)