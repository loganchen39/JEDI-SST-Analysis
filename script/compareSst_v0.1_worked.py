'''
Description: python code to compare SST between CCI and OISSTv2.1 with xarray, numpy, matplotlib etc.
Author: Ligang Chen
Date created: 11/13/2020
Date last modified: 11/13/2020 
'''

import numpy as np
import xarray as xr

import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

import os
import calendar




DIR_CCI     = '/glade/scratch/lgchen/data/SST_ML/ESA_SST_CCI/AVHRR_L3C_CDRv2.1/AVHRR07_G_Done/night'
DIR_OISST   = '/glade/scratch/lgchen/data/SST_ML/OISSTv2.1'
FN_CCT_PF   = '120000-ESACCI-L3C_GHRSST-SSTskin-AVHRR07_G-CDR2.1_night-v02.0-fv01.0.nc'
FN_OISST_PF = 'oisst-avhrr-v02r01.'
YEAR        = 1982

# only compare 1982 for now
for i_mon in range(1, 2):
  dofm = calendar.monthrange(YEAR, i_mon)[1]
  str_ym = str(YEAR) + str(i_mon).zfill(2)
  print('Currently processing month: ' + str_ym)

  print('Reading CCI SST data ...')
# ds_cci = xr.open_mfdataset(paths=DIR_CCI + '/' + str_ym + '??' + FN_CCT_PF  \
#   , compat='override', data_vars='minimal', coords='minimal', combine='by_coords')
# sst_mm_cci = ds_cci.sea_surface_temperature.mean(dim='time')
# sst_mm_cci = sst_mm_cci - 273.15  # Kelvin to Celsius

  ds_cci = xr.open_dataset(DIR_CCI + '/' + str_ym + '01' + FN_CCT_PF).isel(time=0)
  sst_cci = ds_cci['sea_surface_temperature'] - 273.15
# print('sst_cci[1800, :]:  ')
# print(sst_cci[1800, :])
  ds_cci.close()


  print('Reading OISSTv2.1 data ...')
# ds_oisst = xr.open_mfdataset(paths=DIR_OISST + '/' + FN_OISST_PF + str_ym + '??.nc'  \
#   , compat='override', data_vars='minimal', coords='minimal', combine='by_coords')
# sst_mm_oisst = ds_oisst.sst.mean(dim='time')

  ds_oisst = xr.open_dataset(DIR_OISST + '/' + FN_OISST_PF + str_ym + '01.nc')
  ds_oisst.coords['lon'] = (ds_oisst.coords['lon'] + 180)%360 -180  # convert (0~360) to (-180~180)!
  ds_oisst = ds_oisst.sortby(ds_oisst.lon)
# print('new ds_oisst.lon: ')
# print(ds_oisst.lon)
  sst_oisst = ds_oisst['sst'].isel(time=0, zlev=0)
# print('sst_mm_oisst shape: ', sst_mm_oisst.shape)

  # interpolate to CCI finer grid
  oisst2cci = sst_oisst.interp_like(sst_cci)
  print('oisst2cci.shape: ', oisst2cci.shape)
  print('oisst2cci.lon: ')
  print(oisst2cci.lon)
  print('oisst2cci.lat: ')
  print(oisst2cci.lat) 

  ds_oisst.close() 
  

  # plot
  print('Plotting ...')
  fig  = plt.figure(figsize=(8, 12))
  grid = gridspec.GridSpec(nrows=2, ncols=1, figure=fig)
  proj = ccrs.PlateCarree() 
  ax0 = fig.add_subplot(grid[0], projection=proj)
  ax1 = fig.add_subplot(grid[1], projection=proj)  

# for (ax, title) in [(ax0, 'CCI_SST'), (ax1, 'OISSTv2.1')]:
  for (ax, title) in [(ax0, 'CCI_SST 19820101'), (ax1, 'OISSTv2.1 interpolated 19820101')]:
    gvutil.set_axes_limits_and_ticks(ax=ax, xlim=(-180, 180), ylim=(-90, 90)  \
      , xticks=np.linspace(-180, 180, 13), yticks=np.linspace(-90, 90, 7))
    gvutil.add_lat_lon_ticklabels(ax)
    ax.yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
    ax.xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))
    gvutil.add_major_minor_ticks(ax)
    ax.coastlines(linewidth=0.5)
    gvutil.set_titles_and_labels(ax, lefttitle=title, righttitle='Celsius', lefttitlefontsize=10, righttitlefontsize=10)
  # ax.set_title(title, loc='center', y=1.04, fontsize=10)

  cmap = gvcmaps.BlWhRe
  handle = ax0.contourf(sst_cci['lon'], sst_cci['lat'], sst_cci.data, levels=np.arange(0, 30, 2), cmap=cmap, extend='both')
# ax1.contourf(sst_mm_oisst['lon'], sst_mm_oisst['lat'], sst_mm_oisst.data, levels=np.arange(0, 30, 2), cmap=cmap, extend='both')
  ax1.contourf(oisst2cci['lon'], oisst2cci['lat'], oisst2cci.data, levels=np.arange(0, 30, 2), cmap=cmap, extend='both')

  # add colorbar
  cbar = plt.colorbar(handle, ax=[ax0, ax1], ticks=range(0, 30, 2), extendrect=True, extendfrac='auto', shrink=0.85, aspect=13, drawedges=True)

  plt.show()
