# Imports.
import numpy as np
import matplotlib.pyplot as plt
import h5py,sys,os,errno

#from astropy.io import fits
#from time import sleep
#from pprint import pprint

from lsreduce import io
from astropy.io import fits
#from lsreduce import astrometry
#from lsreduce import photometry

import handy as hd

# Global variables.
C_ARR = np.array(['C','E','N','S','W'])
Q_ARR = np.array(['2015Q1','2015Q2','2015Q3','2015Q4',
                  '2016Q1','2016Q2','2016Q3','2016Q4',
                  '2017Q1','2017Q2','2017Q3','2017Q4',
                  '2018Q1','2018Q2','2018Q3','2018Q4'])

# Functions
def hdf5_checker():
	ascc = []
	while True:
		if len(ascc) == 0: entry = raw_input('ASCC number:                               ')
		else: entry = raw_input(''                                           '')
		if entry.lower() == '': break
		ascc.append(entry)

	for t in range(len(ascc)):
		output_loc_txt = '/data5/bruinsma/stars/{0}/{0}_lapalma_hdf5_files.txt'.format(ascc[t])
		try: os.makedirs('/data5/bruinsma/stars/{0}'.format(ascc[t])) # Make star directory if it does not exist.
		except OSError as sys.exit:
			if sys.exit.errno != errno.EEXIST: raise

		textfile = open(output_loc_txt,'w') # Open text file.
		hd.double_printer('\n       ### Star ASCC identifier: {0} ###\n\n'.format(ascc[t]),textfile) # Prints both in terminal and text file.

		for i in range(len(Q_ARR)):
			for j in range(len(C_ARR)):
				datafile = "/data3/mascara/reduced/{0}/LP{1}/red0_vmag_{0}LP{1}.hdf5".format(Q_ARR[i],C_ARR[j])
				if os.path.isfile(datafile): # Only go through if this file exists.
					with h5py.File(datafile,'r') as f:
						if ascc[t] in f['data']: hd.double_printer('{1}LP{2}: Star {0} is visible.\n'.format(ascc[t],Q_ARR[i],C_ARR[j]),textfile)
						else: hd.double_printer('{1}LP{2}: Star {0} is NOT visible.\n'.format(ascc[t],Q_ARR[i],C_ARR[j]),textfile)
				else: hd.double_printer('{0} does NOT exist.\n'.format(datafile),textfile)
			hd.double_printer('\n',textfile) # Some extra spaces for clarity.

def hdf5_info():
	# Input ascc numbers of stars you want x and y coordinates from at different times.
	ascc = []
	while True:
		if len(ascc) == 0: entry = raw_input('ASCC number:                               ')
		else: entry = raw_input(''                                           '')
		if entry.lower() == '': break
		ascc.append(entry)

	# Output a text document with x,y,lstseq
	for t in range(len(ascc)): # Loop through different stars.
		output_loc_txt = '/data5/bruinsma/stars/{0}/{0}_lapalma_hdf5_info.txt'.format(ascc[t])
		try: os.makedirs('/data5/bruinsma/stars/{0}'.format(ascc[t])) # Make star directory if it does not exist.
		except OSError as sys.exit: 
			if sys.exit.errno != errno.EEXIST: raise

		textfile = open(output_loc_txt,'w')
		hd.double_printer('Star ASCC identifier: {0}\n'.format(ascc[t]),textfile)
		for i in range(len(Q_ARR)): # Loop through all the quarters.
			for j in range(len(C_ARR)): # Loop through all different cameras.
				datafile = "/data3/mascara/reduced/{0}/LP{1}/red0_vmag_{0}LP{1}.hdf5".format(Q_ARR[i],C_ARR[j])
				if os.path.isfile(datafile): # Only go through if this file exists.
					hd.double_printer('\n      ### {0} - Camera: {1} ### \n\n'.format(Q_ARR[i],C_ARR[j]),textfile)
					with h5py.File(datafile,'r') as f:
						index = 'No index found'
						if ascc[t] in f['data']: # Find index number of ASCC[t] to obtain v-mag.
							hd.double_printer('Visibility:                   True\n',textfile)
							g = f['data'][ascc[t]]
							jdmid = g['jdmid']; lst = g['lst']; lstseq = g['lstseq']; mag0 = g['mag0']; nobs = g['nobs']; x = g['x']; y = g['y']; 
							hd.double_printer('Number of images:             {0}\n\n'.format(len(x)),textfile)
							for k in range(len(x)):
								if k == 0: hd.double_printer('K    JDMID         LST   LSTSEQ MAG0   NOBS  X       Y\n',textfile)
								hd.double_printer('{0:04.0f} {1:13.5f} {2:03.3f} {3:06.0f} {4:06.3f} {5:02.0f}    {6:07.2f} {7:07.2f}\n'.format(k,jdmid[k],lst[k],lstseq[k],mag0[k],nobs[k],x[k],y[k]),textfile)
						else:
							hd.double_printer('Visibility:                   False\n',textfile)
		
		textfile.close

def hdf5_jd_and_coordinates():
	# Input ascc numbers of stars you want x and y coordinates from at different times.
	ascc = []
	while True:
		if len(ascc) == 0: entry = raw_input('ASCC number:                               ')
		else: entry = raw_input(''                                           '')
		if entry.lower() == '': break
		ascc.append(entry)

	# Output a text document with x,y,lstseq
	for t in range(len(ascc)): # Loop through different stars.
		for j in range(len(C_ARR)): # Loop through all different cameras.
			output_loc_txt = '/data5/bruinsma/stars/{0}/julian_dates/{1}_{0}_lapalma_jd_and_coordinates.txt'.format(ascc[t],C_ARR[j])
			try: os.makedirs('/data5/bruinsma/stars/{0}/julian_dates'.format(ascc[t])) # Make star directory if it does not exist.
			except OSError as sys.exit: 
				if sys.exit.errno != errno.EEXIST: raise

			textfile = open(output_loc_txt,'w')
			
			for i in range(len(Q_ARR)): # Loop through all the quarters.
				datafile = "/data3/mascara/reduced/{0}/LP{1}/red0_vmag_{0}LP{1}.hdf5".format(Q_ARR[i],C_ARR[j])
				if os.path.isfile(datafile): # Only go through if this file exists.
					with h5py.File(datafile,'r') as f:
						index = 'No index found'
						if ascc[t] in f['data']: # Find index number of ASCC[t] to obtain v-mag.
							g = f['data'][ascc[t]]

							jd_mid = g['jdmid'] 
							x = g['x'] 
							y = g['y'];

							lst_shifted = g['lst'] # Local siderial time. Shifted is for computing and plotting.
							lst_not_shifted = g['lst'] # Used for printing.

							for k in range(len(lst_shifted)):
								if lst_shifted[k] > 14: lst_shifted[k] -= 24 # Continuity.

							# Initialise variables for dividing the quarter into nights.
							number_nights = 0
							number_images = []
							image_counter = 0

							for k in range(len(lst_shifted)):
								image_counter += 1
								if lst_shifted[k] < lst_shifted[k-1]:
									number_nights += 1
								if k != len(lst_shifted)-1 and lst_shifted[k] > lst_shifted[k+1]:
									number_images.append(image_counter)
									image_counter = 0
								if k == len(lst_shifted)-1:
									number_images.append(image_counter)

							for k in range(number_nights):
								previous_sum = sum(number_images[0:k])

								jd_night = []
								x_night = []
								y_night = []                                

								for l in range(number_images[k]):
									total_sum = previous_sum+l
									jd_night.append(jd_mid[previous_sum+l])
									x_night.append(x[previous_sum+l])
									y_night.append(y[previous_sum+l])
									hd.double_printer('{0} {1} {2}\n'.format(jd_night[-1],x_night[-1],y_night[-1]),textfile)

								hd.double_printer('\n',textfile)

			textfile.close
