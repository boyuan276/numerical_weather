import imageio
from pathlib import Path

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
var_dir = ['T2/', 'slp']

#%%
# Read images
i = 0
j = 0

input_dir = wrfout_headdir + time_dir[i] + var_dir[j]
image_path = Path(input_dir)

images = list(image_path.glob('*.png'))
image_list = []
for file_name in images:
    image_list.append(imageio.imread(file_name))

print(len(image_list))

# Write animation
imageio.mimwrite(var_dir + var_name + '.gif', image_list, fps=4)