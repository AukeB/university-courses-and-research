# Imports.
import numpy as np
import matplotlib.pyplot as plt
import h5py,sys,os,errno

from lsreduce import io
from lsreduce import astrometry
from lsreduce import photometry
from astropy.io import fits
import imageio

import handy as hd

cat = io.read_catalogue('/data3/mascara/configuration/bringcat20180428.fits') # The catalogue.

# Global variables.
C_ARR = np.array(['C','E','N','S','W'])

def lightcurve_plotter_by_coordinates():
	# Input variables
	star_name = 'ProxCen'
	RA_input = '217.4289380144204'
	DEC_input = '-62.6794918941408'
	start_date = '20180302'
	end_date = '20180308'
	step_size_days = '6'
	C_ARR = ['S']

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
		datapoints = []
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

				counter = 0

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

					if flux.size == 0: 
						flux_arr.append(0)
					else: 
						flux_arr.append(flux[0][0])
						counter += 1
					time_arr.append(header['LST'])
					if time_arr[-1] < time_arr[0]: time_arr[-1] += 24

				datapoints.append(counter)
				plt.figure(figsize=(12.8,9.6))
				plt.rc('axes',labelsize=16)
				plt.rc('axes',titlesize=16)
				np.save('/home/bruinsma/Desktop/lsreduce-2017.6/time_arr_{0}'.format(O_ARR[j]),time_arr)
				np.save('/home/bruinsma/Desktop/lsreduce-2017.6/flux_arr_{0}'.format(O_ARR[j]),flux_arr)
				plt.plot(time_arr,flux_arr,'-o',markersize='2',c='b',lw=0.5,label='{0}'.format(star_name))
				plt.title('{0} {1}LS{2}'.format(star_name,O_ARR[j],C_ARR[i]))
				plt.xlabel('Time [LST]')
				plt.ylabel('Flux [counts]')
				plt.grid()
				plt.legend()

				PATH = '/data5/bruinsma/stars/{0}/lightcurves/LS{2}'.format(star_name,O_ARR[j],C_ARR[i])
				output_loc_png = PATH+'/{0}LS{1}'.format(O_ARR[j],C_ARR[i])
				try: os.makedirs(PATH)
				except OSError as sys.exit:
					if sys.exit.errno != errno.EEXIST: raise

				plt.savefig(output_loc_png)
				plt.close()
				print('\nFile saved as {0}.png'.format(output_loc_png))
		print(len(datapoints),datapoints)
		np.save(PATH+'/datapoints.npy',datapoints)

def multiple_sources(gen_flux,plot_flux,fit,mag,avg):
	# Input stars
	stars = np.array([
		[0,'ProxCen','217.4289380144204','-62.6794918941408',11.13],
		[1,'HD126793',hd.ra_conversion(14,30,12.65665),hd.dec_conversion(-62,-51,-44.4635),8.24],
		[2,'HD127145',hd.ra_conversion(14,32,19.00776),hd.dec_conversion(-63,-0,-53.1418),8.43],
		[3,'HD126549',hd.ra_conversion(14,28,35.55607),hd.dec_conversion(-62,-12,-32.4185),8.57],
		[4,'HD126097',hd.ra_conversion(14,25,53.29504),hd.dec_conversion(-62,-47,-53.0302),9.01],
		[5,'HD126762',hd.ra_conversion(14,29,58.11294),hd.dec_conversion(-62,-57,-34.9651),9.43]
		])

	#[,'',hd.ra_conversion(),hd.dec_conversion(),]

	star_index = stars[:,0]
	star_name = stars[:,1]
	RA_input = stars[:,2]
	DEC_input = stars[:,3]
	V_mag = stars[:,4]

	start_date = '20180301'
	end_date = '20180310'
	step_size_days = '1'
	C_ARR = ['S']

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
				try: os.makedirs(PATH)
				except OSError as sys.exit:
					if sys.exit.errno != errno.EEXIST: raise

				def generate_flux():
					# Create arrays so you can plot.
					flux_arr = []
					time_arr = []
					c1 = 0; c2 = 0; c3 = 0

					# Loop over all binned files.
					for k in range(len(lstseq1)):
						hd.progress(k,len(lstseq1)-1,bar_length=40)
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
							c1 += 1
							flux_arr.append(np.zeros((len(stars),2)))
						elif len(flux) < len(stars): # Only save fluxes if all stars are visible.
							c2 += 1
							flux_arr.append(np.zeros((len(stars),2)))
						if len(flux) == len(stars):
							c3 += 1
							flux_arr.append(flux)
						time_arr.append(header['lst'])
						if time_arr[-1] < time_arr[0]: time_arr[-1] += 24

					np.save(PATH+'/flux_arr_{0}.npy'.format(O_ARR[j]),flux_arr)
					np.save(PATH+'/time_arr_{0}.npy'.format(O_ARR[j]),time_arr)

				def magnitude(y_fit):
					flux_arr = np.load(PATH+'/flux_arr_{0}.npy'.format(O_ARR[j]))
					time_arr = np.load(PATH+'/time_arr_{0}.npy'.format(O_ARR[j]))

					np.save(PATH+'/y_fit_{0}.npy'.format(O_ARR[j]),y_fit)
					y_fit = np.load(PATH+'/y_fit_{0}.npy'.format(O_ARR[j]))
					
					magnitude = []
					magnitude_fit = []
					for k in range(len(flux_arr[0])-1):
						magnitude.append(float(V_mag[k+1])-2.5*np.log10(flux_arr[:,0,0]/flux_arr[:,k+1,0]))
						magnitude_fit.append(float(V_mag[k+1])-2.5*np.log10(flux_arr[:,0,0]/y_fit[k]))
					
					np.save(PATH+'/mag_arr_{0}.npy'.format(O_ARR[j]),magnitude)
					mag_arr = np.load(PATH+'/mag_arr_{0}.npy'.format(O_ARR[j]))
					np.save(PATH+'/mag_arr_fit_{0}.npy'.format(O_ARR[j]),magnitude_fit)
					mag_arr_fit = np.load(PATH+'/mag_arr_fit_{0}.npy'.format(O_ARR[j]))

					plt.figure(figsize=(12.8,9.6))
					for k in range(len(mag_arr)):
						plt.plot(time_arr,mag_arr[k],'-o',markersize='2',lw=0.5,label='{0}'.format(star_name[k+1]))
					plt.ylim(13,7); plt.xlim(6,16)
					plt.legend(); plt.grid()
					output_loc_png = PATH+'/{0}LS{1}_mag'.format(O_ARR[j],C_ARR[i])
					plt.savefig(output_loc_png); plt.close()
					print('File saved as {0}.png'.format(output_loc_png))

					plt.figure(figsize=(12.8,9.6))
					for k in range(len(mag_arr)):
						plt.plot(time_arr,mag_arr_fit[k],'-o',markersize='2',lw=0.5,label='Fitted {0}'.format(star_name[k+1]))
					plt.ylim(13,7); plt.xlim(6,16)
					plt.legend(); plt.grid()
					output_loc_png = PATH+'/{0}LS{1}_mag_fit'.format(O_ARR[j],C_ARR[i])
					plt.savefig(output_loc_png); plt.close()
					print('File saved as {0}.png'.format(output_loc_png))

					return mag_arr
					
				def fit_curve(): # Uses np.polyfit to fit a second degree curve to datapoints, without the zero values.
					flux_arr = np.load(PATH+'/flux_arr_{0}.npy'.format(O_ARR[j]))
					time_arr = np.load(PATH+'/time_arr_{0}.npy'.format(O_ARR[j]))

					t = []
					flux_nozeros = []

					for l in range(len(flux_arr)):
						if flux_arr[l,1,0] != 0:
							flux_nozeros.append(flux_arr[l])
							t.append(time_arr[l])

					np.save(PATH+'/flux_nozeros_{0}.npy'.format(O_ARR[j]),flux_nozeros)
					flux_nozeros_arr = np.load(PATH+'/flux_nozeros_{0}.npy'.format(O_ARR[j]))

					p = []

					for l in range(len(stars)-1):
						p.append(np.polyfit(x=t,y=flux_nozeros_arr[:,l+1,0],deg=2))

					return p

				def plot_fluxes(p):
					flux_arr = np.load(PATH+'/flux_arr_{0}.npy'.format(O_ARR[j]))
					time_arr = np.load(PATH+'/time_arr_{0}.npy'.format(O_ARR[j]))

					try: os.makedirs(PATH)
					except OSError as sys.exit:
						if sys.exit.errno != errno.EEXIST: raise

					y_fit = []
					for k in range(len(stars)-1):
						y_fit.append(p[k][0]*time_arr**2+p[k][1]*time_arr+p[k][2])

					for k in range(len(stars)):
						plt.figure(figsize=(12.8,9.6))
						plt.plot(time_arr,flux_arr[:,k,0],'-o',markersize='2',lw=0.5,label='{0}, V = {1}'.format(star_name[k],V_mag[k]))
						plt.title('Nearby star {0} {1}LS{2}'.format(star_name[k],O_ARR[j],C_ARR[i]))
						plt.xlabel('Time [LST]'); plt.ylabel('Flux [counts]')
						plt.grid(); plt.legend()
						output_loc_png = PATH+'/{0}LS{1}_star_{2}'.format(O_ARR[j],C_ARR[i],star_name[k])
						plt.savefig(output_loc_png); plt.close()
						print('File saved as {0}.png'.format(output_loc_png))

					plt.figure(figsize=(12.8,9.6))
					for k in range(len(stars)):
						plt.plot(time_arr,flux_arr[:,k,0],'-o',markersize='2',lw=0.5,label='{0}, V = {1}'.format(star_name[k],V_mag[k]))
					plt.title('{0} {1}LS{2} and nearby stars.'.format(star_name[0],O_ARR[j],C_ARR[i]))
					plt.xlabel('Time [LST]'); plt.ylabel('Flux [counts]')
					plt.grid(); plt.legend()
					output_loc_png = PATH+'/{0}LS{1}_nearby_stars'.format(O_ARR[j],C_ARR[i])
					plt.savefig(output_loc_png); plt.close()
					print('File saved as {0}.png'.format(output_loc_png))

					for k in range(len(stars)-1):
						plt.figure(figsize=(12.8,9.6))
						plt.plot(time_arr,flux_arr[:,k+1,0],'-o',markersize='2',lw=0.5,label='{0}, V = {1}'.format(star_name[k+1],V_mag[k+1]))
						plt.plot(time_arr,y_fit[k],'-o',markersize='2',lw=0.3)
						plt.title('Nearby star {0} and their fitted curve'.format(star_name[k+1]))
						plt.xlabel('Time [LST]'); plt.ylabel('Flux [counts]')
						plt.grid(); plt.legend()
						output_loc_png = PATH+'/{0}LS{1}_fit_{2}'.format(O_ARR[j],C_ARR[i],star_name[k+1])
						plt.savefig(output_loc_png); plt.close()
						print('File saved as {0}.png'.format(output_loc_png))					

					plt.figure(figsize=(12.8,9.6))
					for k in range(len(stars)-1):
						plt.plot(time_arr,flux_arr[:,k+1,0],'-o',markersize='2',lw=0.5,label='{0}, V = {1}'.format(star_name[k+1],V_mag[k+1]))
						plt.plot(time_arr,y_fit[k],'-o',markersize='2',lw=0.5,)
					plt.title('Nearby stars and their fitted curve')
					plt.xlabel('Time [LST]'); plt.ylabel('Flux [counts]')
					plt.grid(); plt.legend()
					output_loc_png = PATH+'/{0}LS{1}_fitted_curves'.format(O_ARR[j],C_ARR[i])
					plt.savefig(output_loc_png); plt.close()
					print('File saved as {0}.png'.format(output_loc_png))

					return y_fit

				def avgmag():
					time_arr = np.load(PATH+'/time_arr_{0}.npy'.format(O_ARR[j]))
					mag_arr = np.load(PATH+'/mag_arr_{0}.npy'.format(O_ARR[j]))

					average = 0
					for k in range(len(mag_arr)):
						average += mag_arr[k]
					average /= len(mag_arr)

					np.save('/home/bruinsma/Desktop/lsreduce-2017.6/mag_arr_{0}.npy'.format(O_ARR[j]),average)

					plt.figure(figsize=(12.8,9.6))
					plt.rc('axes',labelsize=14)
					plt.rc('axes',titlesize=14)
					plt.title('Brightness of Proxima Centauri')
					plt.xlabel('Time [LST]')
					plt.ylabel('Flux [magnitudes]')
					plt.plot(time_arr,average,'-o',markersize='2',lw=0.5,label='Average of nearby stars')
					plt.ylim(11,8); plt.xlim(6,16)
					plt.legend(); plt.grid()
					output_loc_png = PATH+'/{0}LS{1}_mag_average'.format(O_ARR[j],C_ARR[i])
					plt.savefig(output_loc_png); plt.close()
					print('File saved as {0}.png'.format(output_loc_png))

				if gen_flux == True: generate_flux()
				if fit == True: p = fit_curve()
				if plot_flux == True: y_fit = plot_fluxes(p)
				if mag == True: magnitude(y_fit)
				if avg == True: avgmag()			

#lightcurve_plotter_by_coordinates()				
#multiple_sources(gen_flux=True,fit=True,plot_flux=True,mag=True,avg=True)

def visible_over_year():
	PATH = '/data5/bruinsma/stars/ProxCen/lightcurves/LSS'
	datapoints = np.load(PATH+'/datapoints.npy')
	#print(len(datapoints))
	#print(datapoints)
	time_arr = np.linspace(1,len(datapoints),len(datapoints))
	print(len(time_arr))
	plt.plot(time_arr,datapoints,'.',c='k',markersize=2)
	plt.xlabel('Observation night number'); plt.ylabel('Number of binned images')
	plt.title('Number of binned images per night of Proxima Centauri')
	#plt.savefig(PATH+'/datapoints')
	plt.show()
	plt.close()

def standard_deviation():
	PATH = '/data5/bruinsma/stars/ProxCen/lightcurves/LSS/nearby'

	data_arr = ['1','2','3','4','5','6','7','8','9']

	for p in range(len(data_arr)):
		mag_arr = np.load(PATH+'/mag_arr_2018030{0}.npy'.format(data_arr[p]))

		average = 0
		for k in range(len(mag_arr)):
			average += mag_arr[k]
		average /= len(mag_arr)

		#print(average[23:-1])
		std = np.std(average[23:-1])
		print(std)

#visible_over_year()
standard_deviation()


#time = np.load('/home/bruinsma/Desktop/lsreduce-2017.6/time_arr_20180302.npy')
#flux = np.load('/home/bruinsma/Desktop/lsreduce-2017.6/flux_arr_20180302.npy')
#mag = np.load('/home/bruinsma/Desktop/lsreduce-2017.6/mag_arr_20180302.npy')
#time1 = np.load('/home/bruinsma/Desktop/lsreduce-2017.6/time_arr_20180308.npy')
#flux1 = np.load('/home/bruinsma/Desktop/lsreduce-2017.6/flux_arr_20180308.npy')
#mag1 = np.load('/home/bruinsma/Desktop/lsreduce-2017.6/mag_arr_20180308.npy')

#plt.plot(time,flux)
#plt.show(); plt.close()

#plt.plot(time,mag)
#plt.show(); plt.close()

#plt.plot(time1,flux1)
#plt.show(); plt.close()

#plt.plot(time1,mag1)
#plt.show(); plt.close()