'''
Description: 
Author: Ligang Chen
Date created: 01/28/2021
Date last modified: 01/28/2021 
'''

import numpy as np
import xarray as xr


# FN_SST = '/glade/work/lgchen/project/OISST_JEDI/UMD-SST/UMD-SST/test/Data/19850101_regridded_sst.nc'
FN_SST = '/glade/work/lgchen/project/OISST_JEDI/UMD-SST/UMD-SST/test/Data/20100101_regridded_sst.nc'

ds_sst = xr.open_dataset(FN_SST)
# da_mask = xr.DataArray(np.ones((180, 360), dtype=np.int32), name='landmask', dims=('lat', 'lon'), \
#     coords={'lat': ds_sst.coords['lat'].data, 'lon': ds_sst.coords['lon'].data})
da_mask = xr.DataArray(np.ones((720, 1440), dtype=np.int32), name='landmask', dims=('lat', 'lon'), \
    coords={'lat': ds_sst.coords['lat'].data, 'lon': ds_sst.coords['lon'].data})

# da_mask = xr.where(ds_sst['sst'].isel(time=0).drop('time').isnull(), 1, da_mask)
da_mask = xr.where(ds_sst['sst'].isel(time=0, drop=True).isnull(), 0, da_mask)
# print(da_mask)
da_mask.to_dataset(name='landmask').to_netcdf('./landmask.nc')
