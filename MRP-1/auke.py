#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 11:51:42 2018

@author: talens
"""

import numpy as np

import h5py
from astropy.io import fits

# Install lsreduce using: python setup.py install --user
from lsreduce import io
from lsreduce import astrometry
from lsreduce import photometry

import matplotlib.pyplot as plt

datafile = '/data5/mascara/LaSilla/20180904LSS/lightcurves/fast_20180904LSS.hdf5'
imagefile = '/data5/mascara/LaSilla/20180904LSS/binned/bin_28064794LSS.fits'

# Read and plot the image.
image, header = fits.getdata(imagefile, header=True)

#vmin = np.nanpercentile(image, 1)
#vmax = np.nanpercentile(image, 99)

#plt.imshow(image, interpolation='None', vmin=vmin, vmax=vmax, cmap=plt.cm.Greys)
#plt.show()

# Read astrometric solutions from the lightcurve file.
with h5py.File(datafile, 'r') as f:
    
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
    
# Look up the solution that belongs to the image.
arg, = np.where(lstseq1 == header['LSTSEQ']) # This look-up may not always work.
arg = np.squeeze(arg)

# Set up the WCS dictionary.
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
polpars['order'] = 5 # Different for older files?
polpars['x_wcs2pix'] = x_wcs2pix[arg]
polpars['y_wcs2pix'] = y_wcs2pix[arg]
polpars['x_pix2wcs'] = x_pix2wcs[arg]
polpars['y_pix2wcs'] = y_pix2wcs[arg]

# Read the catalogue of stars.
cat = io.read_catalogue('/data3/mascara/configuration/bringcat20180428.fits')
#print len(cat['ra'])
for i in range(len(cat['ra'])):
    print(cat['ra'][i],cat['dec'][i])

# Compute the x, y positions of visible stars.
pos = astrometry.Astrometry(wcspars, polpars)
xpix, ypix, mask = pos.world2pix(header['LST'], cat['ra'], cat['dec'], header['JD']) # May not always need Julian date.

# Plot the image and positions.
vmin = np.nanpercentile(image, 1)
vmax = np.nanpercentile(image, 99)

plt.imshow(image, interpolation='None', vmin=vmin, vmax=vmax, origin = (xpix, ypix), cmap=plt.cm.Greys)
plt.plot(xpix, ypix, 'r.')
pixel_rang = 20
#plt.xlim ( xpix - pixel_rang, xpix + pixel_rang )
#plt.ylim ( ypix - pixel_rang, ypix + pixel_rang )
plt.show()

# Perform photometry at the computes positions.
#phot = photometry.Photometry([2.5, 4.5], [6, 21])
#flux, eflux, sky, esky, peak, flag = phot(image, xpix, ypix)
