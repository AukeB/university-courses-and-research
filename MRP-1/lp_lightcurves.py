# Imports.
import numpy as np
import matplotlib.pyplot as plt
import h5py,sys,os,errno

#from astropy.io import fits
#from time import sleep
#from pprint import pprint

from lsreduce import io
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
def lapalma_lightcurve():
    # Input ascc numbers of all the stars you want lightcurves of.
    ascc = []
    while True:
        if len(ascc) == 0: entry = raw_input('ASCC number:                               ')
        else: entry = raw_input(''                                           '')
        if entry.lower() == '': break
        ascc.append(entry)

    # Output a text document with all magnitude values for each binned image in the 4 years.
    for t in range(len(ascc)): # Loop through different stars.
        output_loc_txt = '/data5/bruinsma/stars/{0}/{0}_lapalma_night_magnitudes.txt'.format(ascc[t])
        try: os.makedirs('/data5/bruinsma/stars/{0}'.format(ascc[t])) # Make star dir if it does not exist.
        except OSError as sys.exit: 
            if sys.exit.errno != errno.EEXIST: raise

        text_file = open(output_loc_txt,'w')
        hd.double_printer('Star ASCC identifier: {0}\n'.format(ascc[t]),text_file)
        for i in range(len(Q_ARR)): # Loop through all the quarters.
            for j in range(len(C_ARR)): # Loop through all different cameras.
                datafile = "/data3/mascara/reduced/{0}/LP{1}/red0_vmag_{0}LP{1}.hdf5".format(Q_ARR[i],C_ARR[j])
                if os.path.isfile(datafile): # Only go through if this file exists.
                    hd.double_printer('\n      ### {0} - Camera: {1} ### \n\n'.format(Q_ARR[i],C_ARR[j]),text_file)
                    with h5py.File(datafile,'r') as f:
                        index = 'No index found'
                        if ascc[t] in f['data']: # Find index number of ASCC[t] to obtain v-mag.
                            for n in range(len(f['header']['ascc'])):
                                if f['header']['ascc'][n] == ascc[t]:
                                    index = n

                            vmag = f['header']['vmag'][index] # Obtain V-magnitude.
                            hd.double_printer('Visibility:                   True\n',text_file)

                            x = f['data'][ascc[t]]
                            lst_shifted = x['lst'] # Local siderial time. Shifted is for computing and plotting.
                            lst_not_shifted = x['lst'] # Used for printing.

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

                            lstseq = x['lstseq']
                            jd = x['jdmid']
                            mag = x['mag0'] + vmag

                            hd.double_printer('Number of binned images:      {0}\n'.format(len(lst_shifted)),text_file)
                            hd.double_printer('Number of observation nights: {0}\n'.format(number_nights),text_file)

                            for k in range(number_nights):
                                hd.double_printer('\n{0}, camera {1}, night {2}, number of images: {3}\n\n'.format(Q_ARR[i],C_ARR[j],k,number_images[k]),text_file)
                                previous_sum = sum(number_images[0:k])
                                lst_night = []
                                mag_night = []

                                for l in range(number_images[k]):
                                    total_sum = previous_sum+l
                                    hd.double_printer('{0}'.format(previous_sum+l),text_file) # Change this to total_sum?
                                    s = 5
                                    while total_sum >= 10: total_sum /= 10; s -= 1
                                    for r in range(s): hd.double_printer(' ',text_file)
                                    hd.double_printer('{0}   {1}\n'.format(hd.h2hm(lst_not_shifted[previous_sum+l]),mag[previous_sum+l]),text_file)
                                    lst_night.append(lst_shifted[previous_sum+l]); mag_night.append(mag[previous_sum+l])

                                # Plotting.
                                plt.plot(lst_night,mag_night,label='{0}, {1}LP{2}, night {3}: {4} images.'.format(ascc[t],Q_ARR[i],C_ARR[j],k,number_images[k]))
                                plt.ylim(vmag-0.5,vmag+1) # To make sure peaks would be quickly recognized as perturbations.
                                plt.legend()
                                output_loc_image = '/data5/bruinsma/stars/{0}/day_lightcurves/{0}_{1}_LP{2}_night{3}.png'.format(ascc[t],Q_ARR[i],C_ARR[j],k)
                                try: os.makedirs('/data5/bruinsma/stars/{0}/day_lightcurves'.format(ascc[t]))
                                except OSError as e:
                                        if e.errno != errno.EEXIST: raise
                                plt.savefig(output_loc_image)
                                sys.stdout.write('File saved as {0}\n'.format(output_loc_image))
                                plt.close()
                        else:
                            hd.double_printer('Visibility:                   False\n',text_file)
        text_file.close()

# Functions
def lapalma_quarter_lightcurve(): # For inspecting the whole plot of a quarter.
    # Input ASCC numbers, quarters and cameras.
    ascc = []
    while True:
        if len(ascc) == 0: entry = raw_input('ASCC number:                               ')
        else: entry = raw_input('                                           ')
        if entry.lower() == '': break
        ascc.append(entry)

    Q_ARR = []
    while True:
        if len(Q_ARR) == 0: entry = raw_input('Quarters:                                  ')
        else: entry = raw_input('                                           ')
        if entry.lower() == '': break
        Q_ARR.append(entry)

    C_ARR = []
    while True:
        if len(C_ARR) == 0: entry = raw_input('Cameras:                                   ')
        else: entry = raw_input('                                           ')
        if entry.lower() == '': break
        C_ARR.append(entry)

    for t in range(len(ascc)): # Loop through different stars.
        for i in range(len(Q_ARR)): # Loop through all the quarters.
            for j in range(len(C_ARR)): # Loop through all different cameras.
                datafile = "/data3/mascara/reduced/{0}/LP{1}/red0_vmag_{0}LP{1}.hdf5".format(Q_ARR[i],C_ARR[j])
                if os.path.isfile(datafile): # Only go through if this file exists.
                    with h5py.File(datafile,'r') as f:
                        index = 'No index found'
                        if ascc[t] in f['data']: # Find index number of ASCC[t] to obtain v-mag.
                            for n in range(len(f['header']['ascc'])):
                                if f['header']['ascc'][n] == ascc[t]:
                                    index = n

                            vmag = f['header']['vmag'][index] # Obtain V-magnitude.

                            x = f['data'][ascc[t]]
                            jd = x['jdmid']
                            mag = x['mag0'] + vmag

                            # Plotting.
                            plt.plot(jd,mag,'.',label='{0}, {1}LP{2}'.format(ascc[t],Q_ARR[i],C_ARR[j]))
                            plt.ylim(vmag-0.5,vmag+1) # To make sure peaks would be quickly recognized as perturbations.
                            plt.legend()
                            output_loc_image = '/data5/bruinsma/stars/{0}/quarters/lightcurves/{0}_{1}LP{2}.png'.format(ascc[t],Q_ARR[i],C_ARR[j])
                            try: os.makedirs('/data5/bruinsma/stars/{0}/quarters/lightcurves'.format(ascc[t]))
                            except OSError as e:
                                    if e.errno != errno.EEXIST: raise
                            plt.show()
                            plt.close()