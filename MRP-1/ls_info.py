# Imports.
import numpy as np
import matplotlib.pyplot as plt
import h5py,sys,os,errno
import glob # <-- Maybe possible to delete.

from lsreduce import io
from lsreduce import astrometry
from lsreduce import photometry
from astropy.io import fits
#from time import sleep
#from pprint import pprint

import handy as hd

cat = io.read_catalogue('/data3/mascara/configuration/bringcat20180428.fits') # The catalogue.

# Global variables.
C_ARR = np.array(['C','E','N','S','W'])

# With the ASCC number, gives the RA, DEC, B-mag, V-mag and Spectral type of the star, if it is in the catalogue.
def info_star():
	ascc = raw_input('ASCC number:                  ')

	output_loc_txt = '/data5/bruinsma/stars/{0}/{0}_info_star.txt'.format(ascc)
	try: os.makedirs('/data5/bruinsma/stars/{0}'.format(ascc)) # Make star directory if it does not exist.
	except OSError as sys.exit:
		if sys.exit.errno != errno.EEXIST: raise

	textfile = open(output_loc_txt,'w') # Open text file.

	in_cat = False

	hd.double_printer('\n  ####################\n  ### Star {0} ###\n  ####################\n\n'.format(ascc),textfile)

	for i in range(len(cat)):
		if ascc == cat[i][11]: # Column 11 of the 'ascc' column.
			in_cat = True			
			hd.double_printer('Is star {0} in the catalogue? Yes.\n'.format(ascc),textfile)
			hd.double_printer('Star coordinates:\n',textfile)
			hd.double_printer('RA:            {0}\n'.format(cat[i][6]),textfile)
			hd.double_printer('DEC:           {0}\n'.format(cat[i][8]),textfile)
			hd.double_printer('B-mag:         {0}\n'.format(cat[i][0]),textfile)
			hd.double_printer('V-mag:         {0}\n'.format(cat[i][3]),textfile)
			hd.double_printer('Spectral type: {0}\n'.format(cat[i][2]),textfile)

	if in_cat == False:
		hd.double_printer('Is star {0} in the catalogue? No.\n'.format(ascc),textfile)

def star_visibility():
	#Input ASCC number, observation range and stepsize binned images.
	ascc = []
	while True:
		if len(ascc) == 0: entry = raw_input('ASCC number:                               ')
		else: entry = raw_input('                                           ')
		if entry.lower() == '': break
		ascc.append(entry)
	
	start_date = raw_input('First night of observation (YYYYMMDD):     ')
	end_date = raw_input('Last night of observation:                 ')
	raw_ob_arr = hd.observation_dates(start_date,end_date,skip=True)
	step_size_days = raw_input('Day interval:                              ')
	O_ARR = []

	for i in range(len(raw_ob_arr)):
		if i % int(step_size_days) == 0:
			O_ARR.append(raw_ob_arr[i])

	C_ARR = []
	while True:
		if len(C_ARR)==0:
			entry = raw_input("Enter camera's to check (<Enter> to quit): ")
		else: entry = raw_input('                                           ')
		if entry.lower () == '':
			break
		C_ARR.append(entry)
	
	step_size_binned = raw_input('Step size binned images:                   ')
	
	for m in range(len(ascc)):
		output_loc_txt = '/data5/bruinsma/stars/{0}/visibility/{0}_start={1}_end={2}_stepsizedays={3}_stepsizebinned={4}.txt'.format(ascc[m],start_date,end_date,step_size_days,step_size_binned)
		try: os.makedirs('/data5/bruinsma/stars/{0}/visibility'.format(ascc[m])) # Make star directory if it does not exist.
		except OSError as sys.exit:
			if sys.exit.errno != errno.EEXIST: raise

		textfile = open(output_loc_txt,'w') # Open text file.
		hd.double_printer('Star:                    {0}\n'.format(ascc[m]),textfile)
		hd.double_printer('Start date:              {0}\n'.format(start_date),textfile)
		hd.double_printer('End date:                {0}\n'.format(end_date),textfile)
		hd.double_printer('Step size days:          {0}\n'.format(step_size_days),textfile)
		hd.double_printer('Step size binned images: {0}\n'.format(step_size_binned),textfile)

		for i in range(len(O_ARR)):
			for j in range(len(C_ARR)):
				hd.double_printer('\n   ### {0}LS{1} ###\n\n'.format(O_ARR[i],C_ARR[j]),textfile)
				datafile = '/data4/snellen/products/{0}LS{1}/lightcurves/fast_{0}LS{1}.hdf5'.format(O_ARR[i],C_ARR[j])

				# Read astometric solutions from the lightcurve file.
				with h5py.File(datafile,'r') as f:
					grp = f['station']
					lst0 = grp['lst'].value 
					lstseq0 = grp['lstseq'].value
					grp = f['astrometry']
					lstseq1 = grp['lstseq'].value
					pc = grp['pc'].value
					crval = grp['crval'].value
					crpix = grp['crpix'].value
					x_wcs2pix = grp['x_wcs2pix'].value
					y_wcs2pix = grp['y_wcs2pix'].value
					x_pix2wcs = grp['x_pix2wcs'].value
					y_pix2wcs = grp['y_pix2wcs'].value

				# Look up the LST that belongs to each solution.
				idx = np.searchsorted(lstseq0, lstseq1)
				lst1 = lst0[idx]

				for k in range(len(lstseq1)):
					if k % int(step_size_binned) == 0:
						imagefile = '/data4/snellen/products/{0}LS{1}/binned/bin_{2}LS{1}.fits.gz'.format ( O_ARR[i], C_ARR[j], lstseq1[k])

						# Read and plot the image.
						image,header = fits.getdata(imagefile,header=True)

						# Look up the solution that belongs to the image.
						arg, = np.where(lstseq1 == header['LSTSEQ'])
						arg = np.squeeze(arg)

						# Set up the WCS dictionary (World Coordinate System).
						wcspars = dict()
						wcspars['lst'] = lst1[arg]
						wcspars['crval'] = crval[arg]
						wcspars['crpix'] = crpix[arg]
						wcspars['cdelt'] = np.array([header['CDELT1'], header['CDELT2']])
						wcspars['pc'] = pc[arg]

						# Set up the polynomial dictionary.
						polpars = dict()
						polpars['nx'] = 4008
						polpars['ny'] = 2672
						polpars['order'] = 5
						polpars['x_wcs2pix'] = x_wcs2pix[arg]
						polpars['y_wcs2pix'] = y_wcs2pix[arg]
						polpars['x_pix2wcs'] = x_pix2wcs[arg]
						polpars['y_pix2wcs'] = y_pix2wcs[arg]

						# Compute the x, y positions of visible stars.
						pos = astrometry.Astrometry(wcspars,polpars)
						xpix,ypix,mask = pos.world2pix(header['LST'],cat['ra'],cat['dec'],header['JD']) 
						newcat = cat[mask]

						if k == 0: hd.double_printer('k    LSTSEQ1   LST1     VISIBILITY\n',textfile)
						hd.double_printer('{0:03.0f}  {1}  {2} '.format(k,lstseq1[k],hd.h2hm(lst1[k])),textfile)

						if ascc[m] in newcat['ascc']: hd.double_printer(' True\n',textfile)
						else: hd.double_printer(' False\n',textfile)

		textfile.close()
