'''
Description: python code to compute valid ESACCI obs SST percentage.
Author: Ligang Chen
Date created: 05/18/2021
Date last modified: 05/18/2021 
'''

import numpy as np
import xarray as xr

import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as colors

# import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil

import os
import calendar




DIR_CCI     = '/glade/scratch/lgchen/data/SST_ML/ESA_SST_CCI/AVHRR_L3C_CDRv2.1'
# FN_CCT_PF   = ''
lst_yr_sat = [(1985, 'AVHRR09_G'), (1995, 'AVHRR12_G'), (2005, 'AVHRR17_G'), (2012, 'AVHRRMTA_G')]
dic_yr_avg = {1985:[], 1995:[], 2005:[], 2012:[]}


# for (yr, sat) in lst_yr_sat:
#     dire = sat + '_Done'
#     ds = xr.open_mfdataset(paths=DIR_CCI + '/' + dire + '/' + str(yr) + '100*.nc', compat='override', data_vars='minimal',  \
#         coords='minimal', combine='by_coords')
#   # print(type(ds))
#   # print(ds)
#     da_sst = ds['sea_surface_temperature']
#   # print(da_sst.shape)
#   # print(ds.dims)
#   # print(ds.sizes)
#   # print(ds.coords)
#   # print(da_sst.dims)
#   # print(da_sst.sizes)
#   # print(da_sst.coords)
# 
#   # exit()
#     
#     for i_tm in range(da_sst.sizes['time']):
#         da_tmp = xr.where(da_sst[i_tm, :, :].isnull(), 0.0, 1.0)
#       # print(da_tmp[1800, :])
#         n_valid = da_tmp.sum().values
#       # print(type(n_valid))
#         if i_tm == 0:
#             pass
#           # print(da_tmp.shape)
#           # print("n_valid = ", n_valid)
#           # print(n_valid.shape)
#           # print(n_valid)
#           # print(n_valid[0])  # error: too many indices
#         dic_yr_avg[yr].append(1.0*n_valid/(3600*7200))
#       # print(dic_yr_avg[yr])
#     
#     print("year = ", yr, ", avg = ", sum(dic_yr_avg[yr])/da_sst.sizes['time'])
#     print("Daily percentage of valid observations: ")
#     print(dic_yr_avg[yr])


# for plotting
ds = xr.open_mfdataset(paths=DIR_CCI + '/tmp/*.nc', compat='override', data_vars='minimal',  \
    coords='minimal', combine='by_coords')
da_sst = ds['sea_surface_temperature'] - 273.15
print(da_sst.shape)

fig  = plt.figure(figsize=(8, 12))
# grid = gridspec.GridSpec(nrows=2, ncols=2, figure=fig)
grid = fig.add_gridspec(nrows=2, ncols=2, height_ratios=[0.55, 0.45], hspace=0.1)
proj = ccrs.PlateCarree()

ax0 = fig.add_subplot(grid[0, 0])
ax1 = fig.add_subplot(grid[0, 1])
ax2 = fig.add_subplot(grid[1, 0], projection=proj)
ax3 = fig.add_subplot(grid[1, 1], projection=proj)
#ax0.coastlines(linewidth=0.5)
#ax1.coastlines(linewidth=0.5)
ax2.coastlines(linewidth=0.5)
ax3.coastlines(linewidth=0.5)

gvutil.set_titles_and_labels(ax0, maintitle='1985', maintitlefontsize=14)
gvutil.set_titles_and_labels(ax1, maintitle='1995', maintitlefontsize=14)
gvutil.set_titles_and_labels(ax2, maintitle='2005', maintitlefontsize=14)
gvutil.set_titles_and_labels(ax3, maintitle='2012', maintitlefontsize=14)

gvutil.set_axes_limits_and_ticks(ax=ax0, xlim=(-180, 180), ylim=(-90, 90),  \
    xticks=np.arange(-180, 181, 30), yticks=np.arange(-90, 91, 30))
gvutil.set_axes_limits_and_ticks(ax=ax1, xlim=(-180, 180), ylim=(-90, 90),  \
    xticks=np.arange(-180, 181, 30), yticks=np.arange(-90, 91, 30))
gvutil.set_axes_limits_and_ticks(ax=ax2, xlim=(-180, 180), ylim=(-90, 90),  \
    xticks=np.arange(-180, 181, 30), yticks=np.arange(-90, 91, 30))
gvutil.set_axes_limits_and_ticks(ax=ax3, xlim=(-180, 180), ylim=(-90, 90),  \
    xticks=np.arange(-180, 181, 30), yticks=np.arange(-90, 91, 30))

gvutil.add_lat_lon_ticklabels(ax0)
gvutil.add_lat_lon_ticklabels(ax1)
gvutil.add_lat_lon_ticklabels(ax2)
gvutil.add_lat_lon_ticklabels(ax3)

divnorm = colors.TwoSlopeNorm(vmin=-15, vcenter=0, vmax=40)
cmap = gvcmaps.BlueRed
levels = np.arange(-10, 36, 5)  # Specify levels for contours

ct0 = ax0.contourf(da_sst['lon'], da_sst['lat'], da_sst[0, :, :].data, cmap=cmap, norm=divnorm,  \
     levels=levels, extend='both')
ct1 = ax1.contourf(da_sst['lon'], da_sst['lat'], da_sst[1, :, :].data, cmap=cmap, norm=divnorm,  \
     levels=levels, extend='both')
ct2 = ax2.contourf(da_sst['lon'], da_sst['lat'], da_sst[2, :, :].data, cmap=cmap, norm=divnorm,  \
     levels=levels, extend='both')
ct3 = ax3.contourf(da_sst['lon'], da_sst['lat'], da_sst[3, :, :].data, cmap=cmap, norm=divnorm,  \
     levels=levels, extend='both')

cbar3 = plt.colorbar(ct3, ax=ax3, orientation='horizontal', extendrect=True, extendfrac='auto',  \
    shrink=0.75, aspect=13, drawedges=True, pad=0.1)  # Create colorbars
cbar3.ax.tick_params(labelsize=8)

plt.show()

 
