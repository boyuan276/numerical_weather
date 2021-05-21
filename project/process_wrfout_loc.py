"""
Functions to aid in preprocessesing of various data inputs.

Adopted from the OPTWRF package written by Jeff Sward.
"""

import numpy as np
import pandas as pd
import xarray as xr
from datetime import timedelta
import optwrf.postwrf as postwrf
import optwrf.util as util
import optwrf.helper_functions as hf


def process_wrfout_nyserda_buoy(DIR_WRFOUT, wrfout_file, n_vertical=None,
                                outfile_prefix='processed_', save_file=True):

    # Identify which variables you want to extract from the wrfout file.
    query_variables = [
        'height_agl',  # Height above ground level [m]
        'tk',  # Temperature [K]
        'theta',  # Potential Temperature [K]
        'pres',  # Pressure [Pa]
        'wspd',  # Wind speed [m s-1]
        'wdir',  # Wind direction [degrees]
        'UST',  # U* IN SIMILARITY THEORY (friction velocity) [m s-1]
        'HFX',  # Upward surface (sensible) heat flux [W m-2]
        'LH',  # Upward surface latent heat flux [W m-2]
        # 'QKE',  # Twice TKE from PBL scheme [m2 s-2]
        'SST',  # Sea surface temperature [K]
        'SSTSK',  # Skin sea surface temperature [K]
    ]

    # Call the function that processes the data
    metdf = postwrf.process_wrfout_flexible(DIR_WRFOUT, wrfout_file, query_variables,
                                            outfile_prefix='ow_buoy_', save_file=False)

    if n_vertical is not None:
        # A faster method results from simply selecting the data only in the lowest x levels.
        # From above, we see that the lowest 15 levels capture all the data below 1000m
        metdf = metdf.isel(bottom_top=[x for x in range(n_vertical - 1)])
    else:
        # Reduce the dataset by selecting only data up to 1000m.
        # Unfortunately, this takes a while and you must specify the drop=True option
        # to reduce the size of the dataset.
        metdf = metdf.where(metdf.height_agl < 1000, drop=True)

    # Find the x, y indicies for the latitude, longitude pairs
    # correspoonding to the NYSERDA LiDAR buoys.
    # Hudson North -- LAT: 39° 58' 09.40"N, LONG: 72° 43' 00.09"W (39.969278, -72.716692)
    # Hudson South -- LAT: 39° 32' 48.38"N, LONG: 73° 25' 44.01"W (39.546772, -73.428892)
    loc_north_buoy = util.ll_to_xy(metdf, 39.969278, -72.716692)
    loc_south_buoy = util.ll_to_xy(metdf, 39.546772, -73.428892)

    # Now reduce the dataset futher by selecting data only at the two buoy locations
    # NOTE: Longitude/XLONG (west_east) ~ x (index 0); Latitude/XLAT (south_north) ~ y (index 1)
    metdf = metdf.isel(west_east=[loc_north_buoy[0], loc_south_buoy[0]],
                       south_north=[loc_north_buoy[1], loc_south_buoy[1]])

    # Finally, drop the unnecessary WRF XTIME coordinate variable.
    metdf = metdf.reset_coords(['XTIME'], drop=True)

    # Save the output file if specified.
    if save_file:
        # Write the processed data to a wrfout NetCDF file
        new_filename = DIR_WRFOUT + outfile_prefix + wrfout_file
        metdf.to_netcdf(path=new_filename)
    else:
        return metdf


def muliprocess_wrfout_nyserda_buoy(DIR_WRFOUT, start=None, end=None, n_vertical=15,
                                    outfile_prefix='ow_buoy_', save_file=True):
    # Format the input dates
    start_date = hf.format_date(start)
    end_date = hf.format_date(end)

    # Create a list of wrfout files
    time_delta = end_date - start_date
    date_list = [start_date + timedelta(days=i) for i in range(time_delta.days + 1)]
    wrfout_list = [f'wrfout_d03_{date.strftime("%Y-%m-%d")}_00:00:00' for date in date_list]

    # Loop over the list of wrfout files, process each one, and concatonate the resulting datasets
    first = True
    for wrfout_file in wrfout_list:
        # Call the function that processes the data
        metdf_day = process_wrfout_nyserda_buoy(DIR_WRFOUT, wrfout_file, n_vertical=15, save_file=False)
        if first is True:
            metdf = metdf_day
            first = False
        else:
            metdf = xr.concat([metdf, metdf_day], 'Time')

    # Save the output file if specified.
    if save_file:
        # Write the processed data to a wrfout NetCDF file
        new_filename = DIR_WRFOUT + outfile_prefix + \
                       f'wrfout_d03_{start_date.strftime("%Y-%m-%d")}-{end_date.strftime("%Y-%m-%d")}'
        metdf.to_netcdf(path=new_filename)
    else:
        return metdf