# Stellar Structure & Evolution 2020: Practical Assignment.
# Auke Bruinsma (s1594443).

 ### Import packages ###

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

 ### Global constants ###

n1 = 76 # Number of .data files which is the same as the number of time instances of the star.
n2 = 125 # For M_1

 ### Set up paths and directories ###

# General data directory.
#data_dir = '/data2/bruinsma/SSE/data'
data_dir = '/home/auke/Desktop/temp/data'

# Two different paths for the two different simulations.
sim_1 = '/1m_sun/LOGS/'
sim_2 = '/2m_sun/LOGS/'
numpy_arrays = '/numpy_arrays/'

# Make a list of all the .data files for both the simulations
data_files_1_unfiltered = os.listdir(data_dir+sim_1)
data_files_2_unfiltered = os.listdir(data_dir+sim_2)

data_files_1 = []
data_files_2 = []

# Remove the two unwanted files.
for i in range(len(data_files_1_unfiltered)):
    if data_files_1_unfiltered[i].endswith('.data') and data_files_1_unfiltered[i].startswith('profile'):
        data_files_1.append(data_files_1_unfiltered[i])
for i in range(len(data_files_2_unfiltered)):
    if data_files_2_unfiltered[i].endswith('.data') and data_files_2_unfiltered[i].startswith('profile'):
        data_files_2.append(data_files_2_unfiltered[i])
 
# Function to make sure strings are ordered as 1,2,3,... and not 1,10,100,101,...
def natural_string_sort(arr):
    arr_sort = []
    l = 0
    for i in range(len(arr)):
        for j in range(len(arr)):
            if int(arr[j][7:-5]) == l+1:
                arr_sort.append(arr[j])
        l += 1
    return arr_sort

# Sort the arrays correctly.
data_files_1 = natural_string_sort(data_files_1)
data_files_2 = natural_string_sort(data_files_2)

# Add everything together with a loop
data_paths_1 = []
data_paths_2 = []

for i in range(n1):
    data_paths_1.append(data_dir+sim_1+data_files_1[i])
for i in range(n2):
    data_paths_2.append(data_dir+sim_2+data_files_2[i])

 ### Function that reads in MESA log files from a data path ###

def read_in_data_file(path):
    # First import the first part of the .data file, which is the global data.
    global_data = pd.read_csv(path, delim_whitespace=True, engine='python', nrows=3) # Read in first 3 rows.
    global_data.columns = global_data.iloc[0] # Use the second row as header.
    global_data = global_data.drop(global_data.index[0]) # Delete first row that only contains row numbers.

    # Secondly, import the zone data, which is done less devious.
    zone_data = pd.read_csv(path, delim_whitespace=True, engine='python', skiprows=5, header=0)

    # Return data.
    return global_data, zone_data

 ### Read in all relevant parameters for both simulations and save them to numpy arrays ###

def save_relevant_parameters():
	# Global parameters.
	star_age_1 = []
	star_age_2 = []
	num_zones_1 = []
	num_zones_2 = []
	Teff_1 = []
	Teff_2 = []
	photosphere_L_1 = []
	photosphere_L_2 = []

	# Zone parameters.
	logT_1 = [] 
	logT_2 = []
	logRho_1 = []
	logRho_2 = []
	logR_1 = []
	logR_2 = []
	grada_1 = []
	grada_2 = []
	gradr_1 = []
	gradr_2 = []

	# Loop through all files
	for i in range(n1):
		# Read in all data for both simulations.
		global_data_1, zone_data_1 = read_in_data_file(data_paths_1[i])
		
		# Global parameters.
		star_age_1.append(float(global_data_1['star_age'].iloc[0]))
		num_zones_1.append(float(global_data_1['num_zones'].iloc[0]))
		Teff_1.append(float(global_data_1['Teff'].iloc[0]))
		photosphere_L_1.append(float(global_data_1['photosphere_L'].iloc[0]))

		# Zone parameters.
		logT_1.append(float(zone_data_1['logT'].iloc[-1])) # Last row for the core.
		logRho_1.append(float(zone_data_1['logRho'].iloc[-1])) # Last row for the core.
		logR_1.append(zone_data_1['logR'])
		grada_1.append(zone_data_1['grada'])
		gradr_1.append(zone_data_1['gradr'])

		print(i,data_files_1[i],star_age_1[-1],num_zones_1[-1],Teff_1[-1],photosphere_L_1[-1],logT_1[-1],logRho_1[-1],)
		#print(i,data_files_1[i],logR_1[-1])

	for i in range(n2):
		# Read in all data for both simulations.
		global_data_2, zone_data_2 = read_in_data_file(data_paths_2[i])

		# Global parameters.
		star_age_2.append(float(global_data_2['star_age'].iloc[0]))
		num_zones_2.append(float(global_data_2['num_zones'].iloc[0]))
		Teff_2.append(float(global_data_2['Teff'].iloc[0]))
		photosphere_L_2.append(float(global_data_2['photosphere_L'].iloc[0]))

		# Zone parameters.
		logT_2.append(float(zone_data_2['logT'].iloc[-1]))
		logRho_2.append(float(zone_data_2['logRho'].iloc[-1]))
		logR_2.append(zone_data_2['logR'])
		grada_2.append(zone_data_2['grada'])
		gradr_2.append(zone_data_2['gradr'])

		print(i,data_files_2[i],star_age_2[-1],num_zones_2[-1],Teff_2[-1],photosphere_L_2[-1],logT_2[-1],logRho_2[-1])
		#print(i,data_files_2[i],logR_2[-1])

	np.save(data_dir+numpy_arrays+'star_age_1',star_age_1)
	np.save(data_dir+numpy_arrays+'star_age_2',star_age_2)
	np.save(data_dir+numpy_arrays+'num_zones_1',num_zones_1)
	np.save(data_dir+numpy_arrays+'num_zones_2',num_zones_2)
	np.save(data_dir+numpy_arrays+'Teff_1',Teff_1)
	np.save(data_dir+numpy_arrays+'Teff_2',Teff_2)
	np.save(data_dir+numpy_arrays+'photosphere_L_1',photosphere_L_1)
	np.save(data_dir+numpy_arrays+'photosphere_L_2',photosphere_L_2)
	np.save(data_dir+numpy_arrays+'logT_1',logT_1)
	np.save(data_dir+numpy_arrays+'logT_2',logT_2)
	np.save(data_dir+numpy_arrays+'logRho_1',logRho_1)
	np.save(data_dir+numpy_arrays+'logRho_2',logRho_2)
	np.save(data_dir+numpy_arrays+'logR_1',logR_1)
	np.save(data_dir+numpy_arrays+'logR_2',logR_2)
	np.save(data_dir+numpy_arrays+'grada_1',grada_1)
	np.save(data_dir+numpy_arrays+'grada_2',grada_2)
	np.save(data_dir+numpy_arrays+'gradr_1',gradr_1)
	np.save(data_dir+numpy_arrays+'gradr_2',gradr_2)

	print(f'Succesfully saved all relevant parameters in {data_dir}{numpy_arrays}')

save_relevant_parameters()










