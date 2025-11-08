# Imports
import numpy as np
import os
import argparse

from astropy.io import fits
from astropy.modeling import models
from astropy.wcs import WCS
from astropy.nddata.utils import Cutout2D
from astropy import units as u

from spython.main import Client

import handy

def remove_sources(pointing,pointing_dir,catalog_filename,box_center,box_size):
	# Setup filenames.
	image_filename = '{0}{1}.fits'.format(pointing_dir,pointing)
	table_filename = catalog_filename

	# Open the .fits catalog table.
	with fits.open(table_filename) as hdul:
		table_header = hdul[1].header
		table_data = hdul[1].data

	# Load the .fits image.
	with fits.open(image_filename,memmap=True) as hdul:
		image_header = hdul[0].header
		image_data = hdul[0].data
		wcs = WCS(image_header)

	# Only remove point sources.	
	beam_size = image_header['BMAJ'] # Beam size
	axis_ratio = table_data['DC_Maj']/table_data['DC_Min']
	
	axis_ratio_threshold = 1.4 # Set a (arbitrary) threshold.
	maj_beam_threshold = 1.4
	is_point_source = np.where((axis_ratio < axis_ratio_threshold) * (table_data['S_code'] == 'S') * (table_data['DC_Maj'] < beam_size * maj_beam_threshold))[0]

	# Ouput number of point sources.
	# Output some statistics.
	print('\nRemoving point sources.')
	print(' Number of sources detected by PyBDSF: {0}'.format(table_header['NAXIS2']))
	print(' Number of point/removed sources:      {0}'.format(len(is_point_source)))

	# Conversion in case the file is a mosaic and not a pointing.
	if len(image_data.shape) == 4:
		image_data = image_data[0,0]
		wcs = handy.wcsTakeFirstTwo(image_header)

	# Make a cutout.
	cutout = Cutout2D(image_data,tuple(box_center),box_size,wcs=wcs,mode='partial')
	cutout_data = cutout.data
	cutout_wcs = cutout.wcs

	pixel_size = abs(image_header['CDELT1'])

	yi,xi = np.indices(cutout_data.shape)

	subtracted_data = np.copy(cutout_data)

	# Loop over the sources.
	for i in is_point_source:
		amp,x0,y0,Majsigma,Minsigma,theta = handy.getGaussianParams(table_data,pixel_size,i)

		# Make a gaussian model using the parameters from the catalog.
		w = models.Gaussian2D(amp,x0,y0,Majsigma,Minsigma,theta)

		# Calculate the gaussian itself on the extent of the data.
		g_data = w(xi,yi)

		# Remove from the cutout data
		subtracted_data -= g_data

	return cutout_data,subtracted_data,table_data,pixel_size,is_point_source
























