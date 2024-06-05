'''
Description: python code to compute and plot valid ESACCI obs SST percentage.
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
#         # Ligang: has to use values to make it a number, or it's a DataArray and you can't use it for calculation directly!
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

# fig  = plt.figure(figsize=(8, 12))
fig  = plt.figure(figsize=(12, 12))
# grid = gridspec.GridSpec(nrows=2, ncols=2, figure=fig)
grid = fig.add_gridspec(nrows=2, ncols=2, height_ratios=[0.55, 0.45], hspace=-0.05, wspace=0.125)
proj = ccrs.PlateCarree()

divnorm = colors.TwoSlopeNorm(vmin=-15, vcenter=0, vmax=40)
cmap = gvcmaps.BlueRed
# levels = np.arange(-2, 28, 2)  # Specify levels for contours
levels = np.arange(0, 36, 6)  # Specify levels for contours

fig.suptitle('ESACCI-L3C SST OBS Distribution Comparison', fontsize=18, y=0.80)

ax = []
ct = []
for i in range(4):
    ax.append(fig.add_subplot(grid[i], projection=proj))
    ax[i].coastlines(linewidth=0.5)
  # gvutil.set_titles_and_labels(ax[i], maintitle=str(lst_yr_sat[i][0])+'-10-01', maintitlefontsize=10,  \
  #     lefttitle='SST', lefttitlefontsize=10, righttitle='Celsius', righttitlefontsize=10, ylabel='', xlabel='')
    ax[i].set_title(label=str(lst_yr_sat[i][0])+'-10-01', loc='center', fontsize=10, y=1.0, pad=6.0)
    ax[i].set_title(label='SST', loc='left', fontsize=10, y=1.0, pad=6.0)
    ax[i].set_title(label='Celsius', loc='right', fontsize=10, y=1.0, pad=6.0)
    gvutil.set_axes_limits_and_ticks(ax=ax[i], xlim=(-180, 180), ylim=(-90, 90),  \
        xticks=np.arange(-120, 121, 60), yticks=np.arange(-60, 61, 30))
    gvutil.add_lat_lon_ticklabels(ax[i])
    ax[i].yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
    ax[i].xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))
    ct_tmp = ax[i].contourf(da_sst['lon'], da_sst['lat'], da_sst[i, :, :].data, cmap=cmap, norm=divnorm,  \
        levels=levels, extend='both')
    ct.append(ct_tmp)

# cbar3 = plt.colorbar(ct[3], ax=ax, orientation='horizontal', extendrect=True, extendfrac='auto',  \
#     shrink=0.75, aspect=13, drawedges=True, pad=0.1)  # Create colorbars
# cbar3.ax.tick_params(labelsize=8)
cbar = fig.colorbar(ct[3], ax=ax, ticks=np.linspace(0, 36, 7), orientation='horizontal', drawedges=True, 
    extendrect=False, extendfrac='auto', shrink=0.6, aspect=20,  pad=0.05)
cbar.ax.tick_params(labelsize=8)

plt.show()
