#%% Import libraries
import os
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import imageio
# from matplotlib import animation
from matplotlib.cm import get_cmap
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature
from wrf import (getvar, to_np, ALL_TIMES, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords)

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
               'wrfout_d03_2021-05-17_00_00_00']
outfile_prefix='proc_'
# List of queried variables
query_variables = [
    'height_agl',       # Height above ground level [m]
    'tk',               # Temperature [K]
    'pres',             # Pressure [Pa]
    'wspd',             # Wind speed [m s-1]
    'wdir',             # Wind direction [degrees]
    'UST',              # U* IN SIMILARITY THEORY (friction velocity) [m s-1]
    'T2',               # Two meter temperature [K]
    'slp',              # Sea level pressure [hPa]
    'uvmet10'           # 10 m U and V components of wind rotated to earth coordinates [m s-1]
    ]

# Program control settings
write_gif = 1

#%% Read netCDF data
i = 1
ncfile = [nc.Dataset(wrfout_headdir + time_dir[i]+'wrfout_d03_2021-05-15_12_00_00'),
           nc.Dataset(wrfout_headdir + time_dir[i]+'wrfout_d03_2021-05-16_12_00_00')]

# ncfile = nc.Dataset(wrfout_headdir + time_dir[i] + wrfout_file[i])
# time = getvar(wrf_list, 'Times', timeidx=ALL_TIMES)
time = getvar(ncfile, 'Times', timeidx=ALL_TIMES)
num_time = len(time)

#%%

# Get 2m temperature variable
# var_name = "T2"
# var_fullname = "2m temperature"

var_name = "slp"
var_fullname = "Sea level pressure"

if var_name == "T2":
    var_levels = np.linspace(270, 300, 20)
elif var_name == "slp":
    var_levels = np.linspace(1020, 1028, 20)

var_dir = wrfout_headdir + time_dir[i] + var_name + "/"
if os.path.isdir(var_dir):
    pass
else:
    os.makedirs(var_dir)
    print("Create dir ", var_dir)


# Half-hourly output
timestamps = np.arange(0, num_time, 1)

for t in timestamps:
    # Read variable at time i
    # var = getvar(ncfile, var_name, timeidx=i)
    var = getvar(ncfile, var_name, timeidx=t)
    # Smooth data
    smooth_var = smooth2d(var, 3, cenweight=4)

    # Get the latitude and longitude points
    lats, lons = latlon_coords(var)

    # Get the cartopy mapping object
    cart_proj = get_cartopy(var)

    # Create a figure
    fig = plt.figure(figsize=(8,6))
    # Set the GeoAxes to the projection used by WRF
    ax = plt.axes(projection=cart_proj)

    # Download and add the states and coastlines
    states = NaturalEarthFeature(category="cultural", scale="50m",
                                 facecolor="none",
                                 name="admin_1_states_provinces_shp")
    ax.add_feature(states, linewidth=.5, edgecolor="black")
    ax.coastlines('50m', linewidth=0.8)

    # Make the contour outlines and filled contours for the smoothed 2d variable
    plt.contour(to_np(lons), to_np(lats), to_np(smooth_var), 10, colors="black",
                transform=crs.PlateCarree(),
                levels=var_levels)
    plt.contourf(to_np(lons), to_np(lats), to_np(smooth_var), 10,
                 transform=crs.PlateCarree(),
                 cmap=get_cmap("jet"),
                 levels=var_levels)

    # Add a color bar
    plt.colorbar(ax=ax, shrink=.98)

    # Set the map bounds
    ax.set_xlim(cartopy_xlim(smooth_var))
    ax.set_ylim(cartopy_ylim(smooth_var))

    # Add the gridlines
    ax.gridlines(color="black", linestyle="dotted")

    # Add the tile
    time_str = np.datetime_as_string(to_np(var.Time), unit='s')
    title_name = var_name+"_"+time_str
    title_fullname = var_fullname+" "+ time_str
    plt.title(title_fullname)

    # Save and show figure
    fig_name = title_name.replace(':', '_') + '.png'
    fig.savefig(var_dir + fig_name)
    plt.close()

# Create animation

# Read images
from pathlib import Path
image_path = Path(var_dir)
images = list(image_path.glob('*.png'))
image_list = []
for file_name in images:
    image_list.append(imageio.imread(file_name))

print(len(image_list))

# Write animation
imageio.mimwrite(var_dir + var_name + '.gif', image_list, fps=4)
