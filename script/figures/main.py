'''
Description: python code to plot SST with xarray, numpy, matplotlib, Basemap, and probably netCDF4 etc.
Author: Ligang Chen
Date created: 06/22/2020
Date last modified: 06/22/2020 
'''

# import Nio
# import netCDF4
import xarray as xr
import numpy as np
# import pandas as pd

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

import os
# import calendar




DIR_DATA = '/glade/scratch/lgchen/data/SST_ML/ESA_SST_CCI/AVHRR_L3C_CDRv2.1/AVHRR19_G_Done'
os.chdir(DIR_DATA)

fn = '20161230120000-ESACCI-L3C_GHRSST-SSTskin-AVHRR19_G-CDR2.1_day-v02.0-fv01.0.nc'
# fn = '20161230120000-ESACCI-L3C_GHRSST-SSTskin-AVHRR19_G-CDR2.1_night-v02.0-fv01.0.nc'
ds = xr.open_dataset(fn)
# print(ds)

lat = ds.lat
lon = ds.lon
time = ds.time
# sst = fl.variables['sea_surface_temperature'][:].astype('float32')
# sst_var = fl.variables['sea_surface_temperature'][:]
sst = ds.sea_surface_temperature

ds.close()
# print('lat: ')
# print(lat)
# print('lon: ')
# print(lon)
# 
# print('sst shape: ', sst.shape)
# print('sst type: ', type(sst))
# print('sst[0][2000][:]: ')
# print(sst[0][2000][2000:2100])




# sst[0].plot()
# plt.show()

exit()


map = Basemap(projection='mill', lat_ts=10, llcrnrlon=lon.min(), llcrnrlat=lat.min(), urcrnrlon=lon.max(), urcrnrlat=lat.max(), resolution='c')
# map = Basemap(projection='merc',llcrnrlon=-180.,llcrnrlat=-90.,urcrnrlon=180.,urcrnrlat=90.,resolution='i')
# map = Basemap(projection='stere',llcrnrlon=-180.,llcrnrlat=-90.,urcrnrlon=180.,urcrnrlat=90.,resolution='i')
(Lon, Lat) = np.meshgrid(lon, lat)
(x, y) = map(Lon, Lat)

cs = map.pcolormesh(x, y, sst[0, :, :], shading='flat', cmap=plt.cm.jet)

# cs = map.contourf(x, y, sst[0, :, :])
# cb  = map.colorbar(sst, 'bottom', size='5%', pad='2%')
# plt.title('sst')
# cb.set_label('K')

map.drawcoastlines()
map.fillcontinents()
map.drawmapboundary()

map.colorbar(cs)
plt.title('SST 20161230 night')


plt.show()
plt.savefig('./sst_20161230_day.png')
