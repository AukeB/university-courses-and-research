#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 11:34:36 2019

@author: talens-irex
"""

import numpy as np 

from astropy.io import fits

import matplotlib.pyplot as plt

import mascara

def binned_positions(header, cat):
    
    # Extract the 0th order pointing.
    alt0 = header['ALT0']
    az0 = header['AZ0']
    th0 = header['TH0']
    x0 = header['X0']
    y0 = header['Y0']
    
    # Initialize Site and Camera classes.
    site = mascara.observer.Site(28.76025, -17.8792, 2364.)
    cam = mascara.observer.Camera(altitude=alt0, azimuth=az0, orientation=th0, Xo=x0, Yo=y0, nx=4008., ny=2672.)

    # Set the rest of the astrometric solution.  
    cam.tnx['xorder'] = header['XORDER']
    cam.tnx['yorder'] = header['YORDER']
    cam.tnx['xterm'] = header['XTERM']
    crpix = np.zeros((2,))
    crpix[0] = header['CRPIX1']
    crpix[1] = header['CRPIX2']
    cam.tnx['crpix'] = crpix
    cd = np.zeros((2,2))
    cd[0,0] = header['CD1_1']
    cd[0,1] = header['CD1_2']
    cd[1,0] = header['CD2_1']
    cd[1,1] = header['CD2_2']
    cam.tnx['cd'] = cd
    cam.tnx['coefx'] = np.array([float(i) for i in header['XCOEFS'].rsplit(' ')])
    cam.tnx['coefy'] = np.array([float(i) for i in header['YCOEFS'].rsplit(' ')])
    cam.tnx['xfit'] = np.array([float(i) for i in header['XCOR'].rsplit(' ')])
    cam.tnx['yfit'] = np.array([float(i) for i in header['YCOR'].rsplit(' ')])
    
    # Compute the coordinates.
    jd = np.float64(header['JDMID'])
    ra, dec = cat['_RAJ2000'], cat['_DEJ2000']

    alt, az, vis = site.apparent_stars(ra, dec, jd, nutation=True, precession=True, refraction=True)
    cam.solve_corrections(image, alt, az)
    x, y, inCCD = cam.visible_stars(alt, az, margin=-50)
    cam.correct_positions(x, y)
    
    return x, y

catfile = '/data3/mascara/configuration/bringcat20180428.fits'
imagefile = '/data5/mascara/LaPalma/20170915LPC/binned/20170916T033024LPC.fits'  

# Read the La Palma catalogue.
cat = fits.getdata(catfile)
cat = cat[cat['Vmag'] < 8.4]


# Read a binned image.
image, header = fits.getdata(imagefile, header=True)

# Compute the positions of stars in the image.
x, y = binned_positions(header, cat)

vmin = np.nanpercentile(image, 1)
vmax = np.nanpercentile(image, 99)

plt.imshow(image, vmin=vmin, vmax=vmax, cmap=plt.cm.Greys)
plt.plot(x, y, '.')
plt.xlim(0, 4008)
plt.ylim(0, 2672)
plt.show()