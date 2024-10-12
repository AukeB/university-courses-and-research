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

def lapalma_images_by_hdf5_coordinates():
	# Input ascc numbers of all the stars you want lightcurves of.
	#ascc = []
	#while True:
	#	if len(ascc) == 0: entry = raw_input('ASCC number:                               ')
	#	else: entry = raw_input('                                           ')
	#	if entry.lower() == '': break
	#	ascc.append(entry)
	ascc = ['982823'] # 

	pr = 20

	# Output a text document with all magnitude values for each binned image in the 4 years.
	for t in range(len(ascc)): # Loop through different stars.
		for i in range(len(Q_ARR)): # Loop through all the quarters.
			for j in range(len(C_ARR)): # Loop through all different cameras.
				PATH = '/data5/bruinsma/stars/{0}/{1}LP{2}/images'.format(ascc[t],Q_ARR[i],C_ARR[j])
				try: os.makedirs(PATH) # Make star dir if it does not exist.
				except OSError as sys.exit: 
					if sys.exit.errno != errno.EEXIST: raise

				datafile = "/data3/mascara/reduced/{0}/LP{1}/red0_vmag_{0}LP{1}.hdf5".format(Q_ARR[i],C_ARR[j])
				if os.path.isfile(datafile): # Only go through if this file exists.
					with h5py.File(datafile,'r') as f:
						index = 'No index found'
						if ascc[t] in f['data']: # Find index number of ASCC[t] to obtain v-mag.
							for n in range(len(f['header']['ascc'])):
								if f['header']['ascc'][n] == ascc[t]:
									index = n

							g = f['data'][ascc[t]]
							lst_shifted = g['lst'] # Local siderial time. Shifted is for computing and plotting.
							lst_not_shifted = g['lst'] # Used for printing.
							jd = g['jdmid']
							x = g['x']
							y = g['y']

							# Shift coordinates.
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

							julian_dates = open('/data5/bruinsma/general_documents/julian_dates/{0}_lapalma_fits_julian_date.txt'.format(C_ARR[j]))
							fits_file_array = []
							fits_jd_array = []

							for lines in julian_dates:
								fits_file_array.append(lines[0:23])
								fits_jd_array.append(lines[24:-1])

							for k in range(number_nights):
								previous_sum = sum(number_images[0:k])

								jd_night = []
								x_night = []
								y_night = []

								for l in range(number_images[k]):
									total_sum = previous_sum+l
									jd_night.append(jd[previous_sum+l])
									x_night.append(x[previous_sum+l])
									y_night.append(y[previous_sum+l])

								smallest_difference = 10e10
								smallest_element = -1

								for m in range(len(fits_jd_array)-len(jd_night)):
									difference = 0
									for n in range(len(jd_night)):
										difference += np.abs(jd_night[n]-float(fits_jd_array[m+n]))
									if difference < smallest_difference:
										smallest_difference = difference
										smallest_element = m

								for n in range(len(jd_night)):
									directory = 'Directory not yet determined.'
									list_directories = sorted(os.listdir('/data5/mascara/LaPalma'))
									for o in range(len(list_directories)):
										path = '/data5/mascara/LaPalma/{0}/binned'.format(list_directories[o])
										if os.path.isdir(path):
											image_list = os.listdir(path)
											for p in range(len(image_list)):
												#print image_list[p]
												if image_list[p] == fits_file_array[smallest_element]:
													directory = list_directories[o]

									imagefile = '/data5/mascara/LaPalma/{0}/binned/{1}'.format(directory,fits_file_array[smallest_element+n])
									image,header = fits.getdata(imagefile,header=True)

									vmin = np.nanpercentile(image, 1)
									vmax = np.nanpercentile(image, 99)

									plt.imshow(image,interpolation='None',vmin=vmin,vmax=vmax,cmap=plt.cm.Greys)
									plt.plot(x_night[n],y_night[n],'r.')
									plt.xlim(x_night[n]-pr,x_night[n]+pr)
									plt.ylim(y_night[n]-pr,y_night[n]+pr)
									plt.title('Star: {0}. {1}LP{2}: Night {3}, image {4}'.format(ascc[t],Q_ARR[i],C_ARR[j],k,n))
									plt.xlabel('Pixels'); plt.ylabel('Pixels')
									output_loc_png = '/data5/bruinsma/stars/{4}/{0}LP{1}/images_hdf5/night{2}image{3}'.format(Q_ARR[i],C_ARR[j],k,n,ascc[t])
									try: os.makedirs('/data5/bruinsma/stars/{2}/{0}LP{1}/images_hdf5/'.format(Q_ARR[i],C_ARR[j],ascc[t]))
									except OSError as sys.exit:
										if sys.exit.errno != errno.EEXIST: raise
									plt.savefig(output_loc_png)
									sys.stdout.write('File saved as {0}.png\n'.format(output_loc_png))
									plt.close()

									




						else: print '{0}LP{1}: Not in catalogue.'.format(Q_ARR[i],C_ARR[j])
			print ''

lapalma_images_by_hdf5_coordinates()