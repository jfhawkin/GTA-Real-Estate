# -*- coding: utf-8 -*-
"""
Created on Mon May 29 13:00:59 2017

Spatial Exploratory Analysis using Moran I for employment, income, and housing price in GTA

@author: jason
"""

import numpy as np
import pysal as ps
from pysal.contrib.viz import mapping as maps
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

# Read-in each of the input data files
# All files are sorted in increasing alphabetic by TREB zone
f = ps.open('./TREB-Zones-Data.dbf')
shp = ps.open('./TREB-Zones-Data.shp')

# Spatial weights using a Rook-based contiguity method
w = ps.weights.Rook.from_shapefile('./TREB-Zones-Data.shp')
w.transform = 'r'

# Initial LISA mapping setup
orig_crs = ccrs.PlateCarree()
projection = ccrs.LambertConformal()
p_thres = 0.05

YEAR_LIST = ['1996','2006','2016']
YEAR_CODE = ['96','06','16']
EMP_LIST = ['Establishments','Employees','Employment Density', 'EmpCode']
EMP_CODE = ['Estab','Emp','EmpD','EmpCode']


print("Explanatory Statistics for Condos:")
for i,yr in enumerate(YEAR_CODE):
    y = np.array(f.by_col['C{0}'.format(yr)])
    mi = ps.Moran(y,  w)
    lisa = ps.Moran_Local(y, w, permutations=9999)
    print("Global Moran I for {0}: {1:.5f}".format(YEAR_LIST[i], mi.I))
    print("Moran I p-Value for {0}: {1:.5f}".format(YEAR_LIST[i], mi.p_norm))
    polys = maps.map_poly_shp(shp)
    polys = maps.base_lisa_cluster(polys, lisa, p_thres=p_thres)
    polys.set_edgecolor('1')
    polys.set_linewidth(0.2)
    polys.set_transform(orig_crs)
    
    fig = plt.figure(figsize=(12, 8))
    
    ax = plt.axes(projection=projection)
    extent = [shp.bbox[0], shp.bbox[2], shp.bbox[1], shp.bbox[3]]
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_collection(polys)
    ax.outline_patch.set_visible(False)
    
    boxes, labels = maps.lisa_legend_components(lisa, p_thres=p_thres)
    plt.legend(boxes, labels, loc='lower left', fancybox=True)
    
    plt.title('Condos {0} | LISA clusters | P-value = {1}'.format(YEAR_LIST[i], p_thres))
    
    plt.show()

print("\nExplanatory Statistics for Houses:")
for i,yr in enumerate(YEAR_CODE):
    y = np.array(f.by_col['H{0}'.format(yr)])
    mi = ps.Moran(y,  w)
    lisa = ps.Moran_Local(y, w, permutations=9999)
    print("Global Moran I for {0}: {1:.5f}".format(YEAR_LIST[i], mi.I))
    print("Moran I p-Value for {0}: {1:.5f}".format(YEAR_LIST[i], mi.p_norm))
    polys = maps.map_poly_shp(shp)
    polys = maps.base_lisa_cluster(polys, lisa, p_thres=p_thres)
    polys.set_edgecolor('1')
    polys.set_linewidth(0.2)
    polys.set_transform(orig_crs)
    
    fig = plt.figure(figsize=(12, 8))
    
    ax = plt.axes(projection=projection)
    extent = [shp.bbox[0], shp.bbox[2], shp.bbox[1], shp.bbox[3]]
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_collection(polys)
    ax.outline_patch.set_visible(False)
    
    boxes, labels = maps.lisa_legend_components(lisa, p_thres=p_thres)
    plt.legend(boxes, labels, loc='lower left', fancybox=True)
    
    plt.title('Houses {0} | LISA clusters | P-value = {1}'.format(YEAR_LIST[i], p_thres))
    
    plt.show()


print("\nExplanatory Statistics for Townhouses:")
for i,yr in enumerate(YEAR_CODE):
    y = np.array(f.by_col['T{0}'.format(yr)])
    mi = ps.Moran(y,  w)
    lisa = ps.Moran_Local(y, w, permutations=9999)
    print("Global Moran I for {0}: {1:.5f}".format(YEAR_LIST[i], mi.I))
    print("Moran I p-Value for {0}: {1:.5f}".format(YEAR_LIST[i], mi.p_norm))
    polys = maps.map_poly_shp(shp)
    polys = maps.base_lisa_cluster(polys, lisa, p_thres=p_thres)
    polys.set_edgecolor('1')
    polys.set_linewidth(0.2)
    polys.set_transform(orig_crs)
    
    fig = plt.figure(figsize=(12, 8))
    
    ax = plt.axes(projection=projection)
    extent = [shp.bbox[0], shp.bbox[2], shp.bbox[1], shp.bbox[3]]
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_collection(polys)
    ax.outline_patch.set_visible(False)
    
    boxes, labels = maps.lisa_legend_components(lisa, p_thres=p_thres)
    plt.legend(boxes, labels, loc='lower left', fancybox=True)
    
    plt.title('Townhouses {0} | LISA clusters | P-value = {1}'.format(YEAR_LIST[i], p_thres))
    
    plt.show()


print("\nExplanatory Statistics for Employment:")
for i,cd in enumerate(EMP_CODE):
    y = np.array(f.by_col['{0}'.format(cd)])
    mi = ps.Moran(y,  w)
    lisa = ps.Moran_Local(y, w, permutations=9999)
    print("Global Moran I for {0}: {1:.5f}".format(EMP_LIST[i], mi.I))
    print("Moran I p-Value for {0}: {1:.5f}".format(EMP_LIST[i], mi.p_norm))
    polys = maps.map_poly_shp(shp)
    polys = maps.base_lisa_cluster(polys, lisa, p_thres=p_thres)
    polys.set_edgecolor('1')
    polys.set_linewidth(0.2)
    polys.set_transform(orig_crs)
    
    fig = plt.figure(figsize=(12, 8))
    
    ax = plt.axes(projection=projection)
    extent = [shp.bbox[0], shp.bbox[2], shp.bbox[1], shp.bbox[3]]
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_collection(polys)
    ax.outline_patch.set_visible(False)
    
    boxes, labels = maps.lisa_legend_components(lisa, p_thres=p_thres)
    plt.legend(boxes, labels, loc='lower left', fancybox=True)
    
    plt.title('{0} | LISA clusters | P-value = {1}'.format(EMP_LIST[i], p_thres))
    
    plt.show()


print("\nExplanatory Statistics for Average Income:")
for i,yr in enumerate(YEAR_CODE):
    y = np.array(f.by_col['I{0}'.format(yr)])
    mi = ps.Moran(y,  w)
    lisa = ps.Moran_Local(y, w, permutations=9999)
    print("Global Moran I for {0}: {1:.5f}".format(YEAR_LIST[i], mi.I))
    print("Moran I p-Value for {0}: {1:.5f}".format(YEAR_LIST[i], mi.p_norm))
    polys = maps.map_poly_shp(shp)
    polys = maps.base_lisa_cluster(polys, lisa, p_thres=p_thres)
    polys.set_edgecolor('1')
    polys.set_linewidth(0.2)
    polys.set_transform(orig_crs)
    
    fig = plt.figure(figsize=(12, 8))
    
    ax = plt.axes(projection=projection)
    extent = [shp.bbox[0], shp.bbox[2], shp.bbox[1], shp.bbox[3]]
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_collection(polys)
    ax.outline_patch.set_visible(False)
    
    boxes, labels = maps.lisa_legend_components(lisa, p_thres=p_thres)
    plt.legend(boxes, labels, loc='lower left', fancybox=True)
    
    plt.title('Income {0} | LISA clusters | P-value = {1}'.format(YEAR_LIST[i], p_thres))
    
    plt.show()