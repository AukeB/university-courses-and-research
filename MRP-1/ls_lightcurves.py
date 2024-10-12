# Imports.
import numpy as np
import matplotlib.pyplot as plt
import h5py,sys,os,errno

from lsreduce import io
from lsreduce import astrometry
from lsreduce import photometry
from astropy.io import fits
#import glob
import imageio
#from time import sleep
#from pprint import pprint

import handy as hd

cat = io.read_catalogue('/data3/mascara/configuration/bringcat20180428.fits') # The catalogue.

# Global variables.
C_ARR = np.array(['C','E','N','S','W'])

def lightcurve_plotter():
	# Input variables
	ascc = []
	while True: 
		if len(ascc) == 0: entry = raw_input('ASCC number:                               ')
		else: entry = raw_input('                                           ')
		if entry.lower() == '': break
		ascc.append(entry)

	C_ARR = []
	while True:
		if len(C_ARR)==0:
			entry = raw_input("Enter camera's to check (<Enter> to quit): ")
		else: entry = raw_input('                                           ')
		if entry.lower () == '':
			break
		C_ARR.append(entry)

	start_date = raw_input('First night of observation (YYYYMMDD):     ')
	end_date = raw_input('Last night of observation:                 ')
	raw_ob_arr = hd.observation_dates(start_date,end_date,skip=True)
	step_size_days = raw_input('Day interval:                              ')
	O_ARR = []
	for i in range(len(raw_ob_arr)):
		if i % int(step_size_days) == 0:
			O_ARR.append(raw_ob_arr[i])

	for m in range(len(ascc)):
		for i in range(len(C_ARR)):
			for j in range(len(O_ARR)):
				datafile = '/data5/mascara/LaSilla/{0}LS{1}/lightcurves/fast_{0}LS{1}.hdf5'.format(O_ARR[j],C_ARR[i])

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

				# Select the star.
				star_index = 0
				for k in range(len(cat)):
					if cat[k][11] == ascc[m]:
						star_index = k

				# Create arrays so you can plot.
				flux_arr = []
				time_arr = []

				# Loop over all binned files.
				for k in range(len(lstseq1)):
					hd.progress(k,len(lstseq1),bar_length=40)
					imagefile = '/data5/mascara/LaSilla/{0}LS{1}/binned/bin_{2}LS{1}.fits.gz'.format ( O_ARR[j], C_ARR[i], lstseq1[k])

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
					xpix,ypix,mask = pos.world2pix(header['LST'],cat[star_index][6],cat[star_index][8],header['JD'])
					#new_cat = cat[mask]

					# Perform photometry at the computed positions.
					phot = photometry.Photometry([2.5,4.5],[6,21])
					flux,eflux,sky,esky,peak,flag = phot(image,xpix,ypix)

					if flux.size == 0: flux_arr.append(0)
					else: flux_arr.append(flux[0][0])
					time_arr.append(header['LST'])
					if time_arr[-1] > 14: time_arr[-1] -= 24

				plt.plot(time_arr,flux_arr,'-o',label='{0}'.format(ascc[m]))
				plt.title('{0} {1}LS{2}'.format(ascc[m],O_ARR[j],C_ARR[i]))
				plt.xlabel('Time [LST]')
				plt.ylabel('Flux [counts]')
				plt.legend()
				PATH = '/data5/bruinsma/stars/{0}/{1}LS{2}/lightcurves/individual'.format(ascc[m],O_ARR[j],C_ARR[i])
				output_loc_png = PATH+'/{0}LS{1}'.format(O_ARR[j],C_ARR[i])
				try: os.makedirs(PATH)
				except OSError as sys.exit:
					if sys.exit.errno != errno.EEXIST: raise
				plt.savefig(output_loc_png)
				plt.close()
				print('File saved as {0}.png'.format(output_loc_png))

def lightcurve_plotter_by_coordinates():
	# Input variables
	star_name = 'ProxCen2'#raw_input('Enter star name:                           ')
	RA_input = '217.4289380144204'#raw_input('Enter right-ascension:                     ')
	DEC_input = '-62.6794918941408'#raw_input('Enter declination:                         ')
	start_date = '20171117'#raw_input('First night of observation (YYYYMMDD):     ')
	end_date = '20171130'#raw_input('Last night of observation:                 ')
	step_size_days = '1'#raw_input('Day interval:                              ')
	C_ARR = ['S']; #C_ARR = hd.add_to_array(C_ARR,"Enter camera's to check (<Enter> to quite): ")

	raw_ob_arr = hd.observation_dates(start_date,end_date,skip=True)
	O_ARR = []
	for i in range(len(raw_ob_arr)):
		if i % int(step_size_days) == 0:
			O_ARR.append(raw_ob_arr[i])

	main_path = '/data5/bruinsma/stars/{0}'.format(star_name)
	hd.mk_dir(main_path)
	text_file = open(main_path+'/{0}_coordinates.txt'.format(star_name),'w')
	hd.double_printer('Star: {0}\nRA:   {1}\nDEC:  {2}\n'.format(star_name,RA_input,DEC_input),text_file)
	text_file.close()

	for i in range(len(C_ARR)):
		for j in range(len(O_ARR)):
			if os.path.isdir('/data5/mascara/LaSilla/{0}LS{1}/lightcurves'.format(O_ARR[j],C_ARR[i])):
				datafile = '/data5/mascara/LaSilla/{0}LS{1}/lightcurves/fast_{0}LS{1}.hdf5'.format(O_ARR[j],C_ARR[i])

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

				# Create arrays so you can plot.
				flux_arr = []
				time_arr = []

				# Loop over all binned files.
				for k in range(len(lstseq1)):
					hd.progress(k,len(lstseq1),bar_length=40)
					imagefile = '/data5/mascara/LaSilla/{0}LS{1}/binned/bin_{2}LS{1}.fits'.format(O_ARR[j],C_ARR[i],lstseq1[k])

					#For 2017 data:
					if O_ARR[j][3] == '7': # The '7' in '2017'
						imagefile += '.gz'

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
					xpix,ypix,mask = pos.world2pix(header['LST'],RA_input,DEC_input,header['JD'])
					#new_cat = cat[mask]

					# Perform photometry at the computed positions.
					phot = photometry.Photometry([2.5,4.5],[6,21])
					flux,eflux,sky,esky,peak,flag = phot(image,xpix,ypix)

					if flux.size == 0: flux_arr.append(0)
					else: flux_arr.append(flux[0][0])
					time_arr.append(header['LST'])
					if time_arr[-1] < time_arr[0]: time_arr[-1] += 24

				plt.figure(figsize=(12.8,9.6))
				plt.plot(time_arr,flux_arr,'-o',markersize='2',c='b',lw=0.5,label='{0}'.format(star_name))
				plt.title('{0} {1}LS{2}'.format(star_name,O_ARR[j],C_ARR[i]))
				plt.xlabel('Time [LST]')
				plt.ylabel('Flux [counts]')
				plt.grid()
				plt.legend()
				#plt.show()
				PATH = '/data5/bruinsma/stars/{0}/lightcurves/LS{2}'.format(star_name,O_ARR[j],C_ARR[i])
				output_loc_png = PATH+'/{0}LS{1}'.format(O_ARR[j],C_ARR[i])
				try: os.makedirs(PATH)
				except OSError as sys.exit:
					if sys.exit.errno != errno.EEXIST: raise

				plt.savefig(output_loc_png)
				plt.close()
				print('\nFile saved as {0}.png'.format(output_loc_png))

#lightcurve_plotter_by_coordinates()

def multiple_sources(gen_flux,plot_flux,fit,avg):
	# Input variables
	stars = np.array([
		[0,'ProxCen2','217.4289380144204','-62.6794918941408',11.13],
		[1,'HD 127200','218.1512715020132','-62.7021086363366',10.03],
		[2,'HD 126321','216.7916371470576','-62.5444825406462',10.10]
		])

	star_index = stars[:,0]
	star_name = stars[:,1]
	RA_input = stars[:,2]
	DEC_input = stars[:,3]
	V_mag = stars[:,4]

	start_date = '20180302'#raw_input('First night of observation (YYYYMMDD):     ')
	end_date = '20180302'#raw_input('Last night of observation:                 ')
	step_size_days = '1'#raw_input('Day interval:                              ')
	C_ARR = ['S']; #C_ARR = hd.add_to_array(C_ARR,"Enter camera's to check (<Enter> to quite): ")

	raw_ob_arr = hd.observation_dates(start_date,end_date,skip=True)
	O_ARR = []
	for i in range(len(raw_ob_arr)):
		if i % int(step_size_days) == 0:
			O_ARR.append(raw_ob_arr[i])

	main_path = '/data5/bruinsma/stars/{0}'.format(star_name[0])
	hd.mk_dir(main_path)
	text_file = open(main_path+'/{0}_coordinates.txt'.format(star_name[0]),'w')
	hd.double_printer('Star: {0}\nRA:   {1}\nDEC:  {2}\n'.format(star_name[0],RA_input[0],DEC_input[0]),text_file)
	text_file.close()

	for i in range(len(C_ARR)):
		for j in range(len(O_ARR)):
			if os.path.isdir('/data5/mascara/LaSilla/{0}LS{1}/lightcurves'.format(O_ARR[j],C_ARR[i])):
				datafile = '/data5/mascara/LaSilla/{0}LS{1}/lightcurves/fast_{0}LS{1}.hdf5'.format(O_ARR[j],C_ARR[i])

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

				PATH = '/data5/bruinsma/stars/{0}/lightcurves/LS{2}/nearby'.format(star_name[0],O_ARR[j],C_ARR[i])

				def generate_flux():
					# Create arrays so you can plot.
					flux_arr = []
					time_arr = []

					# Loop over all binned files.
					for k in range(len(lstseq1)):
						hd.progress(k+1,len(lstseq1),bar_length=40)
						imagefile = '/data5/mascara/LaSilla/{0}LS{1}/binned/bin_{2}LS{1}.fits'.format(O_ARR[j],C_ARR[i],lstseq1[k])

						#For 2017 data:
						if O_ARR[j][3] == '7': # The '7' in '2017'
							imagefile += '.gz'

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
						xpix,ypix,mask = pos.world2pix(header['LST'],RA_input,DEC_input,header['JD'])
						#new_cat = cat[mask]

						# Perform photometry at the computed positions.
						phot = photometry.Photometry([2.5,4.5],[6,21])
						flux,eflux,sky,esky,peak,flag = phot(image,xpix,ypix)
						
						if flux.size == 0:
							flux_arr.append(np.zeros((len(stars),2)))
						elif len(flux) < len(stars):
							flux_arr.append(np.zeros((len(stars),2)))
						if len(flux) == len(stars):
							flux_arr.append(flux)
						time_arr.append(header['lst'])
						if time_arr[-1] < time_arr[0]: time_arr[-1] += 24

					np.save(PATH+'/flux_arr',flux_arr)
					np.save(PATH+'/time_arr',time_arr)

				def average():
					flux_arr = np.load(PATH+'/flux_arr.npy')
					time_arr = np.load(PATH+'/time_arr.npy')
					return (flux_arr[:,1,0]+flux_arr[:,2,0])/2

				def fit_curve(avg):
					time_arr = np.load(PATH+'/time_arr.npy')

					t = []
					avg_nozeros = []

					for l in range(len(avg)):
						if avg[l] != 0:
							avg_nozeros.append(avg[l])
							t.append(time_arr[l])

					p = np.polyfit(x=t,y=avg_nozeros,deg=2)
					y = p[0]*time_arr**2+p[1]*time_arr+p[2]
					
					plt.figure(figsize=(12.8,9.6))
					plt.plot(time_arr,y,'-o',markersize='2',lw=0.5,label='Fitted 2nd degree curve')
					plt.plot(time_arr,avg,'-o',markersize='2',lw=0.5,label='Average')
					plt.xlabel('Time [LST]')
					plt.ylabel('Flux [counts]')
					plt.grid()
					plt.legend()
					#plt.show()
					plt.close()

					return p

				def plot_fluxes(avg,p):
					flux_arr = np.load(PATH+'/flux_arr.npy')
					time_arr = np.load(PATH+'/time_arr.npy')

					try: os.makedirs(PATH)
					except OSError as sys.exit:
						if sys.exit.errno != errno.EEXIST: raise

					y_fit = p[0]*time_arr**2+p[1]*time_arr+p[2]

					dif = flux_arr[:,0,0]-y_fit

					plt.figure(figsize=(12.8,9.6))
					#for k in range(len(stars)):
					#	plt.plot(time_arr,flux_arr[:,k,0],'-o',markersize='2',lw=0.5,label='{0}'.format(star_name[k]))
					plt.plot(time_arr,flux_arr[:,0,0],'-o',markersize='2',lw=0.5,label='{0}'.format(star_name[0]))
					plt.plot(time_arr,avg,'-o',markersize='2',lw=0.5,label='Average of two nearby stars')
					plt.plot(time_arr,y_fit,'-o',markersize='2',lw=0.5,label='Fitted curve to average')
					plt.plot(time_arr,dif,'-o',markersize='2',lw=0.5,label='Difference ProxCen and fitted curve')

					plt.title('{0} {1}LS{2} and nearby stars.'.format(star_name[0],O_ARR[j],C_ARR[i]))
					plt.xlabel('Time [LST]')
					plt.ylabel('Flux [counts]')
					plt.grid()
					plt.legend()
					
					output_loc_png = PATH+'/{0}LS{1}'.format(O_ARR[j],C_ARR[i])
					

					plt.savefig(output_loc_png)
					plt.close()
					print('\nFile saved as {0}.png'.format(output_loc_png))



				if gen_flux == True: generate_flux()
				if avg == True: average_stars = average()
				if fit == True: p = fit_curve(average_stars)
				if plot_flux == True: plot_fluxes(average_stars,p)

				
multiple_sources(gen_flux=False,avg=True,fit=True,plot_flux=True)