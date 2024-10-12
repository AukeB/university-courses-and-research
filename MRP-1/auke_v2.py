###########################
# Author: Bruinsma        #
# Last edited: 10-10-2018 #
###########################

'''
Questions:
 1. The description of astrometry\pc is FITS WCS parameters PC. What kind of data is this? And where is it used for? Same for astrometry\crpix and astrometry/crvalue.
 2. What does "distortion coefficient" mean in the description of astometry/x_pix2wcs: "Distortion Coefficients from WCS to CCD". Is is just a matrix that is used for the conversion between the two systems?
'''
 ### Imports ###

import numpy as np
import h5py
from astropy.io import fits
import matplotlib.pyplot as plt
from lsreduce import io
from lsreduce import astrometry
from lsreduce import photometry

 ### Input ###

datafile = '/data5/mascara/LaSilla/20171116LSN/lightcurves/fast_20171116LSN.hdf5'
imagefile = '/data5/mascara/LaSilla/20171116LSN/binned/bin_24114825LSN.fits.gz'

# Read and plot the image.
image, header = fits.getdata(imagefile, header=True)

vmin = np.nanpercentile(image, 1)
vmax = np.nanpercentile(image, 99)

plt.imshow(image, interpolation='None', vmin=vmin, vmax=vmax, cmap=plt.cm.Greys)
#plt.show()

# Read astometric solutions from the lightcurve file.
with h5py.File(datafile,'r') as f: # Readonly, file must exist.

	grp = f['station']
	
	lst0 = grp['lst'].value # Local Siderial Time. Siderial time of the reference frame. Dimensions: [4872].
	lstseq0 = grp['lstseq'].value # Local Siderial Time Sequence. Exposure number of the reference frame. Dimensions: [4872].

	grp = f['astrometry']
	
	lstseq1 = grp['lstseq'].value # Names of .fits.gz files. Dimensions: [100].
	pc = grp['pc'].value # Dimensions: [100][2][2].
	crval = grp['crval'].value # Dimensions: [100][2].
	crpix = grp['crpix'].value # Dimensions: [100][2].

	x_wcs2pix = grp['x_wcs2pix'].value # Dimensions: [100][6][6].
	y_wcs2pix = grp['y_wcs2pix'].value # Dimensions: [100][6][6].
	x_pix2wcs = grp['x_pix2wcs'].value # Dimensions: [100][6][6].
	y_pix2wcs = grp['y_pix2wcs'].value # Dimensions: [100][6][6].

	# For inspecting one of the above elements.
	#for x in x_pix2wcs:
	#	print(x)
	#print(len(x_pix2wcs))

	for x in f:
		print x

# Look up the LST that belongs to each solution.
idx = np.searchsorted(lstseq0, lstseq1) # Finds the index number that corresponds to the binned image. Dimensions: [100].
lst1 = lst0[idx] # Local Siderial time of the binned images. Dimensions: [100].

# Look up the solution that belongs to the image.
arg, = np.where(lstseq1 == header['LSTSEQ']) # This look-up may not always work. If it doesn't work, ignore it.
arg = np.squeeze(arg)

# Set up the WCS dictionary (World Coordinate System).
wcspars = dict()
wcspars['lst'] = lst1[arg] # # Local Siderial time of the binned images. Dimensions [1].
wcspars['crval'] = crval[arg] # FITS WCS parameters CRVAL. Dimensions: [2].
wcspars['crpix'] = crpix[arg] # FITS WCS parameters CRPIX. Dimensions: [2].
wcspars['cdelt'] = np.array([header['CDELT1'], header['CDELT2']]) # Dimensions: [2].
wcspars['pc'] = pc[arg] # FITS WCS parameters PC. Dimensions: [2][2].

# Set up the polynomial dictionary.
polpars = dict()
polpars['nx'] = 4008 # Number of pixels in x-direction. Dimensions: [1].
polpars['ny'] = 2672 # Number of pixels in y-direction. Dimensions: [1].
polpars['order'] = 5 # Different for older files?. Dimensions: [1].
polpars['x_wcs2pix'] = x_wcs2pix[arg] # Distortion Coefficients from WCS to CCD. Dimensions: [6][6].
polpars['y_wcs2pix'] = y_wcs2pix[arg] # Distortion Coefficients from WCS to CCD. Dimensions: [6][6].
polpars['x_pix2wcs'] = x_pix2wcs[arg] # Distortion Coefficients from CCD to WCS. Dimensions: [6][6].
polpars['y_pix2wcs'] = y_pix2wcs[arg] # Distortion Coefficients from CCD to WCS. Dimensions: [6][6].

# Read the catalogue of stars.
cat = io.read_catalogue('/data3/mascara/configuration/bringcat20180428.fits') # Dimensions: [349236][12].

''' # For inspecting cat.
hdulist = fits.open('/data3/mascara/configuration/bringcat20180428.fits')
hdulist.info()
#hdu = hdulist[0]
#hdu = hdulist[1]
#print(hdu.header) # 1804355, 1804409, 1804359, 1804415
print ( hdulist[0].header )
print ( hdulist[1].header )
hdulist.close()
print ( cat[0] )
print cat.dtype.names
'''

# Compute the x, y positions of visible stars.
pos = astrometry.Astrometry(wcspars, polpars)
xpix, ypix, mask = pos.world2pix(header['LST'], cat['ra'], cat['dec'], header['JD']) # May not always need Julian date. In the case of '24114824', the array has length 19107, which means there are 19107 stars visible and in the catalogue. Length of 'mask'-array is equal to the amount of stars in the catalogue: 349236.

new_cat = cat[mask] # Filter out all the stars that are not in the image, so it contains only the stars in the image.

print ""


ascc_num = "469584"

#print cat.shape
#print new_cat.shape

#print ""
#print cat[0]
#print ""
#print new_cat[0]
#print ""

#print type ( new_cat[0][11] )

#for i in range ( len ( new_cat ) ):
#	if ascc_num == new_cat[i][11]:
#		print i

e = 10000
distance = np.zeros ( len ( xpix ) )
close_distance = []
close_pixel_range = 50
j = 0
for i in range ( len ( xpix ) ):
	distance[i] = np.sqrt ( ( xpix[e] - xpix[i] ) ** 2 + ( ypix[e] - ypix[i] ) ** 2 )
	if distance[i] <= close_pixel_range:
		close_distance.append ( distance[i] )
		#print i, close_distance[j], new_cat[i][11]
		j += 1

#ascc_num = "914452"
#for i in range ( len ( new_cat ) ):
	#if ( ascc_num == new_cat[i][11] ):
		#print i

#print new_cat[18740][11]




print ""

#print len ( mask ), len ( newcat ), len ( xpix ), len ( ypix ), len ( distance )
#print len ( close_distance )
#print new_cat

#for i in range ( len ( close_distance ) ): print close_distance[i]

'''
# Inspecting selected catalogue.
for i in range ( len ( newcat ) ):
	if ( i % 50 == 0 ):
		print i, newcat[i]['ascc'], newcat[i]['ra'], newcat[i]['dec'], newcat[i]['bmag']
'''
'''
if '914452' not in new_cat['ascc']:
	print 'Star not in image'
if '914452' in new_cat['ascc']:
	print 'Star in image'
'''

# Star 1906572 is in the image.
	# LSC: Star in image.
	# LCE: Star not in image.
	# LSN: Star not in image.
	# LSS: Star in image.
	# LSW: Star in image.

# Plot the image and positions.
vmin = np.nanpercentile(image, 1)
vmax = np.nanpercentile(image, 99)

plt.imshow(image, interpolation='None', vmin=vmin, vmax=vmax, cmap=plt.cm.Greys)
plt.plot(xpix, ypix, 'r.')
#plt.show()

# Perform photometry at the computes positions.
#phot = photometry.Photometry([2.5, 4.5], [6, 21])
#flux, eflux, sky, esky, peak, flag = phot(image, xpix, ypix)
