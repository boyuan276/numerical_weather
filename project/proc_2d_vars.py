'''
Process selected 2d variables

'''
import os
import netCDF4 as nc
import numpy as np
import datetime
import matplotlib.pyplot as plt
import imageio
# from matplotlib import animation
from matplotlib.cm import get_cmap
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature
from wrf import (getvar, to_np, ALL_TIMES, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords)
import optwrf.util as util


#%% Import data

# Set up working directory
wrfout_headdir = 'D:/courses/F2020-S2021/EAS 5555/Code/numerical_weather/project/'
# Sub directories of different initial data sources
time_dir = ['20210515.00Z/',
            '20210515.12Z/',
            '20210516.00Z/',
            '20210516.12Z/',
            '20210517.00Z/']
# Identify the WRF output file to be processed
wrfout_file = ['wrfout_d03_2021-05-15_00_00_00',
               'wrfout_d03_2021-05-15_12_00_00',
               'wrfout_d03_2021-05-16_00_00_00',
               'wrfout_d03_2021-05-16_12_00_00',
               'wrfout_d03_2021-05-17_00_00_00',]

var_names = ['T2', 'slp']
var_fullnames = ["2m temperature", "Sea level pressure"]

#%%
# # Set start and end time stamps
# start =
# end =

# Set variable
n = 0
var_name = var_names[n]
var_fullname = var_fullnames[n]

# Read WRF out file
i = 3
if i == 0:
    ncfile = [nc.Dataset(wrfout_headdir + time_dir[i] + 'wrfout_d03_2021-05-15_00_00_00'),
              nc.Dataset(wrfout_headdir + time_dir[i] + 'wrfout_d03_2021-05-16_00_00_00')]
elif i== 1:
    ncfile = [nc.Dataset(wrfout_headdir + time_dir[i] + 'wrfout_d03_2021-05-15_00_00_00'),
              nc.Dataset(wrfout_headdir + time_dir[i] + 'wrfout_d03_2021-05-16_00_00_00')]
else:
    ncfile = nc.Dataset(wrfout_headdir + time_dir[i] + wrfout_file[i])

# Create an xarray.Dataset from the wrf qurery_variables.
met_data = util._wrf2xarray(ncfile, var_names)

# Slice the wrfout data if start and end times ares specified
met_data = met_data.sel(Time=slice(start, end))

# metdf = met_data.isel(west_east=loc_ithaca[0],south_north=loc_ithaca[1])

# metdf = metdf.reset_coords(['XTIME'], drop=True)





# time = getvar(wrf_list, 'Times', timeidx=ALL_TIMES)
time = getvar(ncfile, 'Times', timeidx=ALL_TIMES)
num_time = len(time)

# Choose timestamps: original file is 10-min
timestamps = np.arange(0, num_time, 1)




t = 1
var = getvar(ncfile, var_name, timeidx=t)
lats, lons = latlon_coords(var)


#%%
















#%%
for t in timestamps:
    # Read variable at time i
    # var = getvar(ncfile, var_name, timeidx=i)
    var = getvar(ncfile, var_name, timeidx=t)
    # Smooth data
    smooth_var = smooth2d(var, 3, cenweight=4)

    # Get the latitude and longitude points
    lats, lons = latlon_coords(var)
