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


ds_tmp = xr.open_dataset(DIR_CCI + '/' + '19820101' + FN_CCT_PF).isel(time=0)
sst_tmp = ds_tmp['sea_surface_temperature'] - 273.15

# only compare 1982 for now
for i_mon in range(1, 2):
  dofm = calendar.monthrange(YEAR, i_mon)[1]

  ds_tmp = xr.open_dataset('./data/avg_sst.nc')
  avg_sst = ds_tmp['__xarray_dataarray_variable__']
  ds_tmp.close()

  ds_tmp = xr.open_dataset('./data/avg_sst_sq.nc')
  avg_sst_sq = ds_tmp['__xarray_dataarray_variable__']
  ds_tmp.close()


  # plot
  print('Plotting ...')
  fig  = plt.figure(figsize=(8, 12))
  grid = gridspec.GridSpec(nrows=2, ncols=1, figure=fig)
  proj = ccrs.PlateCarree() 
  ax0 = fig.add_subplot(grid[0], projection=proj)
  ax1 = fig.add_subplot(grid[1], projection=proj)  

  for (ax, title, unit) in [(ax0, 'avg(cci_sst-oisst), 198201', 'Celsius'), (ax1, 'avg(cci_sst-oisst)^2, 198201', 'Celsius^2')]:
    gvutil.set_axes_limits_and_ticks(ax=ax, xlim=(-180, 180), ylim=(-90, 90)  \
      , xticks=np.linspace(-180, 180, 13), yticks=np.linspace(-90, 90, 7))
    gvutil.add_lat_lon_ticklabels(ax)
    ax.yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
    ax.xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))
    gvutil.add_major_minor_ticks(ax)
    ax.coastlines(linewidth=0.5)
    gvutil.set_titles_and_labels(ax, lefttitle=title, righttitle=unit, lefttitlefontsize=10, righttitlefontsize=10)
  # ax.set_title(title, loc='center', y=1.04, fontsize=10)

  cmap = gvcmaps.BlWhRe
  h0 = ax0.contourf(avg_sst['lon'], avg_sst['lat'], avg_sst.data, levels=np.arange(-2, 2, 0.2), cmap=cmap, extend='both')
# ax1.contourf(sst_mm_oisst['lon'], sst_mm_oisst['lat'], sst_mm_oisst.data, levels=np.arange(0, 30, 2), cmap=cmap, extend='both')
  h1 = ax1.contourf(avg_sst_sq['lon'], avg_sst_sq['lat'], avg_sst_sq.data, levels=np.arange(0, 8, 0.4), cmap=cmap, extend='both')

  # add colorbar
  cbar0 = plt.colorbar(h0, ax=ax0, ticks=np.arange(-2, 2, 0.2), extendrect=True, extendfrac='auto', shrink=0.85, aspect=13, drawedges=True)
  cbar1 = plt.colorbar(h1, ax=ax1, ticks=np.arange(0, 8, 0.4), extendrect=True, extendfrac='auto', shrink=0.85, aspect=13, drawedges=True)

  plt.show()
