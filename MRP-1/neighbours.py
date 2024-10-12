 ### Imports ###

import numpy as np
import h5py
from astropy.io import fits
import matplotlib.pyplot as plt
from lsreduce import io
from lsreduce import astrometry
from lsreduce import photometry
import progressbar
from time import sleep
import sys, os, errno
import glob
import imageio
from pprint import pprint
e=sys.exit
cat = io.read_catalogue('/data3/mascara/configuration/bringcat20180428.fits')
import handy as hd

 ### Global constants ###

cam_arr = ['C',  'E',  'N',  'S',  'W' ]

 ### Functions ###

def closest_stars (): # Creates lightcurves of multiple nights.
	print ""
	ascc = []
	while True:
		if len ( ascc ) == 0:
			entry = raw_input ( "ASCC number:                               " )
		else: entry = raw_input ( "                                           " )
		if entry.lower () == "":
			break
		ascc.append ( entry )
	pixel_distance = int ( raw_input ( "Pixel range:                               " ) )
	num_bin_image = int ( raw_input ( "Number of binned image:                    " ) )
	start_date = raw_input ( "Night of observation (YYYYMMDD):           " )
	end_date = start_date
	ob_arr = hd.observation_dates ( start_date, end_date, skip=True )
	
	cam_to_check = []
	while True:
		if len ( cam_to_check ) == 0:
			entry = raw_input ( "Enter camera's to check                    " )
		else: entry = raw_input ( "                                           " )
		if entry.lower () == "":
			break
		cam_to_check.append ( entry )

	#ascc = ["1804355"]; pixel_distance = 30; start_date="20171116"; end_date="20171116"; cam_to_check=["W"]

	for n in range ( len ( ascc ) ):
		for i in range ( len ( cam_to_check ) ):
			for m in range ( len ( ob_arr ) ):
				datafile = '/data5/mascara/LaSilla/{0}LS{1}/lightcurves/fast_{0}LS{1}.hdf5'.format ( ob_arr[m], cam_to_check[i] )

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

				# Define arrays that are needed for the lightcurve graph.
				flux_star = np.zeros ( ( len ( ob_arr ), len ( lstseq1 ) ) )
				time_array = np.zeros ( ( len ( ob_arr ), len ( lstseq1 ) ) )

				output_loc = "/data5/bruinsma/stars/{0}/LS{4}/{0}_LS{4}_neighbours_{1}_#bin={3}_pixelrange={5}.txt".format ( ascc[n], start_date, end_date, num_bin_image, cam_to_check[i], pixel_distance )
				try: os.makedirs ( '/data5/bruinsma/stars/{0}/LS{1}'.format ( ascc[n], cam_to_check[i] ) ) 
				except OSError as e:
					if e.errno != errno.EEXIST:
						raise

				text_file = open ( output_loc, "w" )

				# Loop over all binned files.
				for j in range ( len ( lstseq1 ) ):
					if j == num_bin_image:
						imagefile = '/data5/mascara/LaSilla/{0}LS{1}/binned/bin_{2}LS{1}.fits.gz'.format ( ob_arr[m], cam_to_check[i], lstseq1[j] )
						image, header = fits.getdata(imagefile, header=True)

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

						# Compute the x, y positions of the corresponding star.
						pos = astrometry.Astrometry(wcspars, polpars)
						xpix, ypix, mask = pos.world2pix(header['LST'], cat['ra'], cat['dec'], header['JD'])
						new_cat = cat[mask]

						# Computation of nearby stars.
						element = 0
						for l in range ( len ( new_cat ) ):
							if ( str ( new_cat[l][11] ) == ascc[n] ):
								element = l

						distance = np.zeros ( len ( xpix ) )
						close_stars = []
						p = 0
						for l in range ( len ( xpix ) ):
							distance[l] = np.sqrt ( ( xpix[element] - xpix[l] ) ** 2 + ( ypix[element] - ypix[l] ) ** 2 )
							if distance[l] <= pixel_distance:
								close_stars.append ( distance[l] )
								if p == 0: 
									print " ### ASCC = {0}, Pixel range = {1}, #bin image = {2}, Camera = {3}, Date = {4} ### ".format ( ascc[n], pixel_distance, num_bin_image, cam_to_check[i], ob_arr[m] )
									print "\nASCC     Distance (pix)  B-mag"
									text_file.write ( "\n ### ASCC = {0}, Pixel range = {1}, #bin image = {2}, Camera = {3}, Date = {4} ### \n\n".format ( ascc[n], pixel_distance, num_bin_image, cam_to_check[i], ob_arr[m] ) )
									text_file.write ( "ASCC     Distance (pix)  B-mag\n" )
								if close_stars[p] == 0:
									print new_cat[l][11], "", "{0:.2f}".format ( close_stars[p] ), "          ", round ( new_cat[l][0], 2 )
									text_file.write ( str ( new_cat[l][11] ) ); text_file.write ( "  " ); text_file.write ( "{0:.2f}".format ( close_stars[p] ) ); text_file.write ( "           " ); text_file.write ( str ( round ( new_cat[l][0], 2 ) ) ); text_file.write ( "\n" )
								else:
									print new_cat[l][11], "", "{0:.2f}".format ( close_stars[p] ), "         ", round ( new_cat[l][0], 2 )
									text_file.write ( str ( new_cat[l][11] ) ); text_file.write ( "  " ); text_file.write ( "{0:.2f}".format ( close_stars[p] ) ); text_file.write ( "           " ); text_file.write ( str ( round ( new_cat[l][0], 2 ) ) ); text_file.write ( "\n" )
								p += 1
				
				print ""
				text_file.close ()