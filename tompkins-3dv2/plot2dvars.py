#%% Import libraries

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

# Open the NetCDF file
cwd = "./"
domain = "d03"
date = "2021-04-10"
time = "12_00_00"
file_name = "wrfout_"+domain+"_"+date+"_"+time
ncfile = nc.Dataset(cwd+file_name)
# Create a list of wrf output
wrf_list = [nc.Dataset("wrfout_d03_2021-04-10_12_00_00"),
           nc.Dataset("wrfout_d03_2021-04-11_12_00_00"),
           nc.Dataset("wrfout_d03_2021-04-12_12_00_00"),
           nc.Dataset("wrfout_d03_2021-04-13_12_00_00"),
           nc.Dataset("wrfout_d03_2021-04-14_12_00_00"),
           nc.Dataset("wrfout_d03_2021-04-15_12_00_00")]

time = getvar(wrf_list, 'Times', timeidx=ALL_TIMES)
num_time = len(time)

#%%

# Get 2m temperature variable
var_name = "T2"
var_fullname = "2m temperature"
fig_dir = cwd + var_name + "/"

for i in range(num_time):
    var = getvar(wrf_list, var_name, timeidx=i)

    # Smooth data
    smooth_var = smooth2d(var, 3, cenweight=4)

    # Get the latitude and longitude points
    lats, lons = latlon_coords(var)

    # Get the cartopy mapping object
    cart_proj = get_cartopy(var)

    # Create a figure
    fig = plt.figure(figsize=(12,6))
    # Set the GeoAxes to the projection used by WRF
    ax = plt.axes(projection=cart_proj)

    # Download and add the states and coastlines
    states = NaturalEarthFeature(category="cultural", scale="50m",
                                 facecolor="none",
                                 name="admin_1_states_provinces_shp")
    ax.add_feature(states, linewidth=.5, edgecolor="black")
    ax.coastlines('50m', linewidth=0.8)

    # Make the contour outlines and filled contours for the smoothed sea level
    # pressure.
    plt.contour(to_np(lons), to_np(lats), to_np(smooth_var), 10, colors="black",
                transform=crs.PlateCarree())
    plt.contourf(to_np(lons), to_np(lats), to_np(smooth_var), 10,
                 transform=crs.PlateCarree(),
                 cmap=get_cmap("jet"))

    # Add a color bar
    plt.colorbar(ax=ax, shrink=.98)

    # Set the map bounds
    ax.set_xlim(cartopy_xlim(smooth_var))
    ax.set_ylim(cartopy_ylim(smooth_var))

    # Add the gridlines
    ax.gridlines(color="black", linestyle="dotted")

    # Add the tile
    time_str = np.datetime_as_string(to_np(var.Time), unit='s')
    title_name = var_name+"_"+domain+"_"+time_str
    plt.title(title_name)

    # Save and show figure
    fig_name = title_name.replace(':', '_') + '.png'
    fig.savefig(fig_dir + fig_name)
    plt.close()

#%% Create animation

# Read images
from pathlib import Path
image_path = Path(fig_dir)
images = list(image_path.glob('*.png'))
image_list = []
for file_name in images:
    image_list.append(imageio.imread(file_name))

print(len(image_list))

# Write animation
imageio.mimwrite(fig_dir + var_name + '.gif', image_list, fps=5)
