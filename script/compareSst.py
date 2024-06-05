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

# ds_tmp = xr.open_dataset(DIR_CCI + '/' + '19820101' + FN_CCT_PF).isel(time=0)
# avg_sst = ds_tmp['sea_surface_temperature'] - 273.15
# avg_sst.dropna()
# avg_sst = 0.0
# avg_sst = xr.DataArray(np.zeros(3600, 7200), dims=('lat', 'lon'), coords={'lat': sst_tmp.lat, 'lon', sst_tmp.lon})
  avg_sst = xr.DataArray(np.zeros((3600, 7200)), dims=('lat', 'lon'), coords={'lat': sst_tmp.lat, 'lon': sst_tmp.lon})

# avg_sst_sq = ds_tmp['sea_surface_temperature'] - 273.15
# avg_sst_sq.dropna()
# avg_sst_sq = 0.0
  avg_sst_sq = xr.DataArray(np.zeros((3600, 7200)), dims=('lat', 'lon'), coords={'lat': sst_tmp.lat, 'lon': sst_tmp.lon})

  num_valid = xr.DataArray(np.zeros((3600, 7200)), dims=('lat', 'lon'), coords={'lat': sst_tmp.lat, 'lon': sst_tmp.lon})

  for i_day in range(1, dofm+1):
    str_ymd = str(YEAR) + str(i_mon).zfill(2) + str(i_day).zfill(2)
    print('Currently processing day: ' + str_ymd)

    ds_cci = xr.open_dataset(DIR_CCI + '/' + str_ymd + FN_CCT_PF).isel(time=0)
    sst_cci = ds_cci['sea_surface_temperature'] - 273.15
    ds_cci.close()

    ds_oisst = xr.open_dataset(DIR_OISST + '/' + FN_OISST_PF + str_ymd + '.nc')
    ds_oisst.coords['lon'] = (ds_oisst.coords['lon'] + 180)%360 -180  # convert (0~360) to (-180~180)!
    ds_oisst = ds_oisst.sortby(ds_oisst.lon)
    sst_oisst = ds_oisst['sst'].isel(time=0, zlev=0)
  # interpolate to CCI finer grid
    oisst2cci = sst_oisst.interp_like(sst_cci)
    ds_oisst.close()

    sst_diff = sst_cci - oisst2cci
    avg_sst = avg_sst + xr.where(sst_diff.isnull(), 0.0, sst_diff)
    avg_sst_sq = avg_sst_sq + xr.where(sst_diff.isnull(), 0.0, xr.ufuncs.square(sst_diff))
    num_valid = num_valid + xr.where(sst_diff.isnull(), 0, 1)

  # for i_lat in range(0, 3600):
  #   print('i_lat = ', i_lat)
  #   for i_lon in range(0, 7200):
  #   # if sst_cci[i_lat, i_lon] != None and oisst2cci[i_lat, i_lon] != None:
  #     if not np.isnan(sst_cci[i_lat, i_lon]) and not np.isnan(oisst2cci[i_lat, i_lon]):
  #       avg_sst[i_lat, i_lon] = avg_sst[i_lat, i_lon] + sst_cci[i_lat, i_lon] - oisst2cci[i_lat, i_lon]
  #       avg_sst_sq[i_lat, i_lon] = avg_sst_sq[i_lat, i_lon] + xr.ufuncs.square(sst_cci[i_lat, i_lon] - oisst2cci[i_lat, i_lon])
  #       num_valid[i_lat, i_lon] = num_valid[i_lat, i_lon] + 1

#   avg_sst    = avg_sst + (sst_cci-oisst2cci)
#   avg_sst_sq = avg_sst_sq + xr.ufuncs.square(sst_cci-oisst2cci)  

  avg_sst    = xr.where(oisst2cci.isnull(), np.nan, avg_sst)
  avg_sst_sq = xr.where(oisst2cci.isnull(), np.nan, avg_sst_sq)

# avg_sst = xr.where(num_valid == 0, np.nan, avg_sst/num_valid)

# avg_sst    = avg_sst/(1.0*dofm)
# avg_sst_sq = avg_sst_sq/(1.0*dofm)

  for i_lat in range(0, 3600):
    print('i_lat = ', i_lat)
    for i_lon in range(0, 7200):
      if num_valid[i_lat, i_lon] != 0:
        avg_sst[i_lat, i_lon] = avg_sst[i_lat, i_lon] / num_valid[i_lat, i_lon]
        avg_sst_sq[i_lat, i_lon] = avg_sst_sq[i_lat, i_lon] / num_valid[i_lat, i_lon]

  print('avg_sst[1800, :]: ')
  print(avg_sst[1800, :])
  print('avg_sst_sq[1700, :]: ')
  print(avg_sst_sq[1700, :])
 
  avg_sst.to_netcdf('./avg_sst.nc') 
  avg_sst_sq.to_netcdf('./avg_sst_sq.nc') 

# print('Computing average ...')
# for i_lat in range(0, 3600):
#   for i_lon in range(0, 7200):
#     if num_valid[i_lat, i_lon] > 0:
#       avg_sst[i_lat, i_lon] = avg_sst[i_lat, i_lon] / num_valid[i_lat, i_lon] 
#       avg_sst_sq[i_lat, i_lon] = avg_sst_sq[i_lat, i_lon] / num_valid[i_lat, i_lon]


  # plot
  print('Plotting ...')
  fig  = plt.figure(figsize=(8, 12))
  grid = gridspec.GridSpec(nrows=2, ncols=1, figure=fig)
  proj = ccrs.PlateCarree() 
  ax0 = fig.add_subplot(grid[0], projection=proj)
  ax1 = fig.add_subplot(grid[1], projection=proj)  

  for (ax, title) in [(ax0, 'avg(cci_sst-oisst), 198201'), (ax1, 'avg(cci_sst-oisst)^2, 198201')]:
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
  h0 = ax0.contourf(sst_cci['lon'], sst_cci['lat'], avg_sst.data, levels=np.arange(-2, 2, 0.2), cmap=cmap, extend='both')
# ax1.contourf(sst_mm_oisst['lon'], sst_mm_oisst['lat'], sst_mm_oisst.data, levels=np.arange(0, 30, 2), cmap=cmap, extend='both')
  h1 = ax1.contourf(sst_cci['lon'], sst_cci['lat'], avg_sst_sq.data, levels=np.arange(0, 4, 0.2), cmap=cmap, extend='both')

  # add colorbar
  cbar0 = plt.colorbar(h0, ax=ax0, ticks=np.arange(-2, 2, 0.2), extendrect=True, extendfrac='auto', shrink=0.85, aspect=13, drawedges=True)
  cbar1 = plt.colorbar(h1, ax=ax1, ticks=np.arange(0, 4, 0.2), extendrect=True, extendfrac='auto', shrink=0.85, aspect=13, drawedges=True)

  plt.show()
