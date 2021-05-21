"""
Pre-processing WRF output

All you need to do in this function is specify those variables either
a) as they appear in the wrfout file, or
b) by the wrf-python diagnostic variable name, a list of which you can find here:
(https://wrf-python.readthedocs.io/en/latest/user_api/generated/wrf.getvar.html#wrf.getvar).

Adopted from the OPTWRF package written by Jeff Sward.

"""

import optwrf.postwrf as postwrf

# Identify which variables you want to extract from the wrfout file.
query_variables = [
    'height_agl',       # Height above ground level [m]
    'tk',               # Temperature [K]
    'theta',            # Potential Temperature [K]
    'pres',             # Pressure [Pa]
    'wspd',             # Wind speed [m s-1]
    'wdir',             # Wind direction [degrees]
    'UST',              # U* IN SIMILARITY THEORY (friction velocity) [m s-1]
    'HFX',              # Upward surface (sensible) heat flux [W m-2]
    'LH',               # Upward surface latent heat flux [W m-2]
    'T2',               # Two meter temperature [K]
    'slp',              # Sea level pressure [hPa]
    'uvmet10'           # 10 m U and V components of wind rotated to earth coordinates
    ]

# Specify which directory the wrfout file is located in
# Note that the processed file will automatically be saved to this directory.
# Also the directory MUST have a "/" at the end!!!!!

DIR_WRFOUT = 'D:/courses/F2020-S2021/EAS 5555/Code/numerical_weather/project/20210515.00Z/'

# Identify the WRF output file to be processed
wrfout_file = 'wrfout_d03_2021-05-15_00_00_00'

# Call the function that processes the data
postwrf.process_wrfout_flexible(DIR_WRFOUT, wrfout_file, query_variables,
                                outfile_prefix='proc_')
