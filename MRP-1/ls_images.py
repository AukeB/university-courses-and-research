# Imports.
import numpy as np
import matplotlib.pyplot as plt
import h5py,sys,os,errno

from lsreduce import io
from lsreduce import astrometry
from lsreduce import photometry
from astropy.io import fits
import glob
import imageio
from time import sleep
from pprint import pprint

import handy as hd

cat = io.read_catalogue('/data3/mascara/configuration/bringcat20180428.fits') # The catalogue.

# Global variables.
C_ARR = np.array(['C','E','N','S','W'])

def image_maker():
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
	step_size_binned = raw_input('Step size binned images:                   ')

	pixel_range_arr = []
	while True:
		if len ( pixel_range_arr ) == 0:
			print "Pixel range(s) ('0' is no zoom)            "
			entry = raw_input ( " From center to border:                    " )
		else: entry = raw_input ( "                                           " )
		if entry.lower () == "":
			break
		pixel_range_arr.append ( entry )

	duration = 0
	make_gif = raw_input('Make gif? (Y/N):                           ')
	if make_gif == 'Y':
		duration = raw_input('Enter duration of each image in gif file:  ')
	duration = float(duration)

	for m in range(len(ascc)):
		for i in range(len(C_ARR)):
			for j in range(len(O_ARR)):
				for l in range(len(pixel_range_arr)):
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

					# Loop over all binned files.
					for k in range(len(lstseq1)):
						if k % int(step_size_binned) == 0: # Skip files if you want to.
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
							
							print cat[star_index][6],cat[star_index][8]

							# Plot the image and positions.
							vmin = np.nanpercentile(image, 1)
							vmax = np.nanpercentile(image, 99)

							plt.imshow(image,interpolation='None',vmin=vmin,vmax=vmax,cmap=plt.cm.Greys)
							plt.title('{0} {2}LS{1} {3}'.format(ascc[m],C_ARR[i],O_ARR[j],lstseq1[k]))
							plt.plot(xpix,ypix,'r.',label='{0}'.format(hd.h2hm(lst1[k])))
							plt.legend()
							if pixel_range_arr[l] != '0':
								plt.xlim(xpix-int(pixel_range_arr[l]),xpix+int(pixel_range_arr[l]))
								plt.ylim(ypix-int(pixel_range_arr[l]),ypix+int(pixel_range_arr[l]))
							plt.xlabel('Pixels'); plt.ylabel('Pixels')

							output_loc_png = '/data5/bruinsma/stars/{0}/{1}LS{2}/binned/pr{3}/{4}LS{2}'.format(ascc[m],O_ARR[j],C_ARR[i],pixel_range_arr[l],lstseq1[k])
							try: os.makedirs('/data5/bruinsma/stars/{0}/{1}LS{2}/binned/pr{3}'.format(ascc[m],O_ARR[j],C_ARR[i],pixel_range_arr[l]))
							except OSError as sys.exit:
								if sys.exit.errno != errno.EEXIST: raise

							plt.savefig(output_loc_png)
							plt.close()
							sys.stdout.write('File saved as {0}.png\n'.format(output_loc_png))

					def create_gif(filenames,duration):
						images = []
						for filename in filenames:
							images.append(imageio.imread(filename))
						PATH = '/data5/bruinsma/stars/{0}/{1}LS{2}/gifs/pr{3}'.format(ascc[m],O_ARR[j],C_ARR[i],pixel_range_arr[l])
						output_loc_gif = PATH+'/{0}_{1}LS{2}_{3}.gif'.format(ascc[m],O_ARR[j],C_ARR[i],pixel_range_arr[l])
						try: os.makedirs(PATH)
						except OSError as sys.exit:
							if sys.exit.errno != errno.EEXIST: raise
						imageio.mimsave(output_loc_gif,images,duration=duration)
						sys.stdout.write('File saved as {0}.\n\n'.format(output_loc_gif))

					PATH = '/data5/bruinsma/stars/{0}/{1}LS{2}/binned/pr{3}'.format(ascc[m],O_ARR[j],C_ARR[i],pixel_range_arr[l])
					items = sorted(os.listdir(PATH))
					filenames = []
					for names in items:
						filenames.append(PATH+'/'+names)
					# Make .gif files if you want to.
					if make_gif == 'Y': 
						create_gif(filenames,duration)

def image_maker_by_coordinates():
	# Input variables
	star_names = 'ProxCen'#raw_input('Enter star name:                           ')
	RA_input = '217.4289380144204'#raw_input('Enter right-ascension:                     ')
	DEC_input = '-62.6794918941408'#raw_input('Enter declination:                         ')

	#C_ARR = []
	C_ARR = np.array(['S'])
	'''
	while True: 
		if len(C_ARR)==0:
			entry = raw_input("Enter camera's to check (<Enter> to quit): ")
		else: entry = raw_input('                                           ')
		if entry.lower () == '':
			break
		C_ARR.append(entry)
	'''

	start_date = '20180302'#raw_input('First night of observation (YYYYMMDD):     ')
	end_date = '20180308'#raw_input('Last night of observation:                 ')
	raw_ob_arr = hd.observation_dates(start_date,end_date,skip=True)
	step_size_days = '6'#raw_input('Day interval:                              ')
	O_ARR = []
	for i in range(len(raw_ob_arr)):
		if i % int(step_size_days) == 0:
			O_ARR.append(raw_ob_arr[i])
	step_size_binned = '1'#raw_input('Step size binned images:                   ')

	pixel_range_arr = ['0','5','10','20','50','100']
	#while True:,
	#	if len ( pixel_range_arr ) == 0:
	#		print "Pixel range(s) ('0' is no zoom)            "
	#		entry = raw_input ( " From center to border:                    " )
	#	else: entry = raw_input ( "                                           " )
	#	if entry.lower () == "":
	#		break
	#	pixel_range_arr.append ( entry )

	duration = '0.04'
	make_gif = 'Y'#raw_input('Make gif? (Y/N):                           ')
	#if make_gif == 'Y':
	#	duration = raw_input('Enter duration of each image in gif file:  ')
	duration = float(duration)

	for i in range(len(C_ARR)):
		for j in range(len(O_ARR)):
			for l in range(len(pixel_range_arr)):
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

					# Loop over all binned files.
					for k in range(len(lstseq1)):
						if k % int(step_size_binned) == 0: # Skip files if you want to.
							imagefile = '/data5/mascara/LaSilla/{0}LS{1}/binned/bin_{2}LS{1}.fits'.format ( O_ARR[j], C_ARR[i], lstseq1[k])

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
							
							# Plot the image and positions.
							vmin = np.nanpercentile(image, 1)
							vmax = np.nanpercentile(image, 99)

							plt.imshow(image,interpolation='None',vmin=vmin,vmax=vmax,cmap=plt.cm.Greys)
							plt.rc('axes',labelsize=12)
							#plt.rc('axes',titlesize=14)
							plt.title('Proxima Centauri {1}LS{0} {2}'.format(C_ARR[i],O_ARR[j],lstseq1[k],star_names))
							plt.plot(xpix,ypix,'r.',label='{0}'.format(hd.h2hm(lst1[k])))
							plt.legend()
							if pixel_range_arr[l] != '0':
								plt.xlim(xpix-int(pixel_range_arr[l]),xpix+int(pixel_range_arr[l]))
								plt.ylim(ypix-int(pixel_range_arr[l]),ypix+int(pixel_range_arr[l]))
							plt.xlabel('Pixels'); plt.ylabel('Pixels')

							output_loc_png = '/data5/bruinsma/stars/{0}/{1}LS{2}/binned/pr{3}/{4}LS{2}'.format(star_names,O_ARR[j],C_ARR[i],pixel_range_arr[l],lstseq1[k])
							try: os.makedirs('/data5/bruinsma/stars/{0}/{1}LS{2}/binned/pr{3}'.format(star_names,O_ARR[j],C_ARR[i],pixel_range_arr[l]))
							except OSError as sys.exit:
								if sys.exit.errno != errno.EEXIST: raise

							plt.savefig(output_loc_png)
							plt.close()
							sys.stdout.write('File saved as {0}.png\n'.format(output_loc_png))

					def create_gif(filenames,duration):
						images = []
						for filename in filenames:
							images.append(imageio.imread(filename))
						PATH = '/data5/bruinsma/stars/{0}/{1}LS{2}/gifs/pr{3}'.format(star_names,O_ARR[j],C_ARR[i],pixel_range_arr[l])
						output_loc_gif = PATH+'/{0}_{1}LS{2}_{3}.gif'.format(star_names,O_ARR[j],C_ARR[i],pixel_range_arr[l])
						try: os.makedirs(PATH)
						except OSError as sys.exit:
							if sys.exit.errno != errno.EEXIST: raise
						imageio.mimsave(output_loc_gif,images,duration=duration)
						sys.stdout.write('File saved as {0}.\n\n'.format(output_loc_gif))

					PATH = '/data5/bruinsma/stars/{0}/{1}LS{2}/binned/pr{3}'.format(star_names,O_ARR[j],C_ARR[i],pixel_range_arr[l])
					items = sorted(os.listdir(PATH))
					filenames = []
					for names in items:
						filenames.append(PATH+'/'+names)
					# Make .gif files if you want to.
					if make_gif == 'Y': 
						create_gif(filenames,duration)
				else:
					print '{0}LS{1} - Lightcurve folder does not exist.'.format(O_ARR[j],C_ARR[i])

def show_red_dots():
	# Stars array. Format is [index,name,RA,DEC,V-mag]
	stars = np.array([
		[0,'ProxCen','217.4289380144204','-62.6794918941408',11.13],
		[1,'HD 126793',hd.ra_conversion(14,30,12.65665),hd.dec_conversion(-62,-51,-44.4635),8.24],
		[2,'HD 127145',hd.ra_conversion(14,32,19.00776),hd.dec_conversion(-63,-0,-53.1418),8.43],
		[3,'HD 126549',hd.ra_conversion(14,28,35.55607),hd.dec_conversion(-62,-12,-32.4185),8.57],
		[4,'HD 126097',hd.ra_conversion(14,25,53.29504),hd.dec_conversion(-62,-47,-53.0302),9.01],
		[5,'HD 126762',hd.ra_conversion(14,29,58.11294),hd.dec_conversion(-62,-57,-34.9651),9.43]
		])

	#[,'',hd.ra_conversion(),hd.dec_conversion(),]


	star_index = stars[:,0]
	star_names = stars[:,1]
	RA_input = stars[:,2]
	DEC_input = stars[:,3]
	V_mag = stars[:,4]

	print('\n')

	#C_ARR = []
	C_ARR = np.array(['S'])
	'''
	while True:
		if len(C_ARR)==0:
			entry = raw_input("Enter camera's to check (<Enter> to quit): ")
		else: entry = raw_input('                                           ')
		if entry.lower () == '':
			break
		C_ARR.append(entry)
	'''

	start_date = '20180308'#raw_input('First night of observation (YYYYMMDD):     ')
	end_date = '20180308'#raw_input('Last night of observation:                 ')
	raw_ob_arr = hd.observation_dates(start_date,end_date,skip=True)
	step_size_days = '1'#raw_input('Day interval:                              ')
	O_ARR = []
	for i in range(len(raw_ob_arr)):
		if i % int(step_size_days) == 0:
			O_ARR.append(raw_ob_arr[i])
	step_size_binned = '1'#raw_input('Step size binned images:                   ')

	pixel_range_arr = ['30']
	#while True:,
	#	if len ( pixel_range_arr ) == 0:
	#		print "Pixel range(s) ('0' is no zoom)            "
	#		entry = raw_input ( " From center to border:                    " )
	#	else: entry = raw_input ( "                                           " )
	#	if entry.lower () == "":
	#		break
	#	pixel_range_arr.append ( entry )

	duration = '0.04'
	make_gif = 'N'#raw_input('Make gif? (Y/N):                           ')
	#if make_gif == 'Y':
	#	duration = raw_input('Enter duration of each image in gif file:  ')
	duration = float(duration)

	for i in range(len(C_ARR)):
		for j in range(len(O_ARR)):
			for l in range(len(pixel_range_arr)):
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

					# Loop over all binned files.
					for k in range(len(lstseq1)):
						if k % int(step_size_binned) == 0: # Skip files if you want to.
							if k == 100:
								imagefile = '/data5/mascara/LaSilla/{0}LS{1}/binned/bin_{2}LS{1}.fits'.format(O_ARR[j],C_ARR[i],lstseq1[k])

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
								
								# Plot the image and positions.
								vmin = np.nanpercentile(image,1)
								vmax = np.nanpercentile(image,99)

								plt.imshow(image,interpolation='None',vmin=vmin,vmax=vmax,cmap=plt.cm.Greys)
								#plt.title('{3} {1}LS{0} {2}'.format(C_ARR[i],O_ARR[j],lstseq1[k],star_names))
								for m in range(len(stars)):
									plt.plot(xpix[m],ypix[m],'.',label='{0}'.format(star_names[m]))
								plt.legend()
								if pixel_range_arr[l] != '0':
									plt.xlim(xpix[0]-int(pixel_range_arr[l]),xpix[0]+int(pixel_range_arr[l]))
									plt.ylim(ypix[0]-int(pixel_range_arr[l]),ypix[0]+int(pixel_range_arr[l]))
								plt.xlabel('Pixels'); plt.ylabel('Pixels')

								PATH = '/data5/bruinsma/stars/{0}/lightcurves/LS{2}/nearby'.format(star_names[0],O_ARR[j],C_ARR[i])
								try: os.makedirs(PATH)
								except OSError as sys.exit:
									if sys.exit.errno != errno.EEXIST: raise
								output_loc_png = PATH+'/{0}LS{1}_image_nearby_stars'.format(O_ARR[j],C_ARR[i])

								plt.savefig(output_loc_png)
								#plt.show()
								plt.close()
								sys.stdout.write('File saved as {0}.png\n'.format(output_loc_png))

					'''
					def create_gif(filenames,duration):
						images = []
						for filename in filenames:
							images.append(imageio.imread(filename))
						PATH = '/data5/bruinsma/stars/{0}/{1}LS{2}/gifs/pr{3}'.format(star_names,O_ARR[j],C_ARR[i],pixel_range_arr[l])
						output_loc_gif = PATH+'/{0}_{1}LS{2}_{3}.gif'.format(star_names,O_ARR[j],C_ARR[i],pixel_range_arr[l])
						try: os.makedirs(PATH)
						except OSError as sys.exit:
							if sys.exit.errno != errno.EEXIST: raise
						imageio.mimsave(output_loc_gif,images,duration=duration)
						sys.stdout.write('File saved as {0}.\n\n'.format(output_loc_gif))

					PATH = '/data5/bruinsma/stars/{0}/{1}LS{2}/binned/pr{3}'.format(star_names,O_ARR[j],C_ARR[i],pixel_range_arr[l])
					items = sorted(os.listdir(PATH))
					filenames = []
					for names in items:
						filenames.append(PATH+'/'+names)
					# Make .gif files if you want to.
					if make_gif == 'Y': 
						create_gif(filenames,duration)
					'''
				else:
					print '{0}LS{1} - Lightcurve folder does not exist.'.format(O_ARR[j],C_ARR[i])

#image_maker_by_coordinates()
#show_red_dots()

# Create manual gifs. Not really needed but may be useful if you forgot to produce gifs during the image making process. Output_loc gifs needs to be changed.
def create_gif():
	PATH = raw_input('PATH:                                      ')
	#duration = raw_input('Enter duration of each image in gif file:  ')
	duration = 0.04 # Default duration is 0.04
	items = sorted(os.listdir(PATH))
	filenames = []
	for names in items:
		filenames.append(PATH+'/'+names)
	print filenames
	images = []
	for filename in filenames:
		images.append(imageio.imread(filename))
	output_loc_gif = '/data5/bruinsma/1630269_LSC_pr=30_20171118.gif'
	try: os.makedirs('/data5/bruinsma')
	except OSError as sys.exit:
		if sys.exit.errno != errno.EEXIST: raise
	imageio.mimsave(output_loc_gif,images,duration=duration)
	sys.stdout.write('File saved as {0}.\n\n'.format(output_loc_gif))