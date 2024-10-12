# Imports.
import numpy as np
import matplotlib.pyplot as plt
import h5py,sys,os,errno

#from astropy.io import fits
#from time import sleep
#from pprint import pprintq

from lsreduce import io
from astropy.io import fits
from lsreduce import astrometry
from lsreduce import photometry

import handy as hd

# Catalogue
cat = io.read_catalogue('/data3/mascara/configuration/bringcat20180428.fits')

# Global variables.
C_ARR = np.array(['C','E','N','S','W'])
Q_ARR = np.array(['2015Q1','2015Q2','2015Q3','2015Q4',
                  '2016Q1','2016Q2','2016Q3','2016Q4',
                  '2017Q1','2017Q2','2017Q3','2017Q4',
                  '2018Q1','2018Q2','2018Q3','2018Q4'])

# Lists folders in /data5/mascara/LaPalma directory and states if certain subofolders exist or not.
def lapalma_list_folders():
	start_date = '20170101'
	end_date = '20181030'
	ob_arr = hd.observation_dates(start_date,end_date,skip=False)
	lp_folder_array = ('binned','fLC','sLC')
	PATH = '/data5/mascara/LaPalma'

	output_loc_txt = '/data5/bruinsma/general_documents/lapalma_list_folders.txt'
	try: os.makedirs('/data5/bruinsma/general_documents')
	except OSError as sys.exit: 
		if sys.exit.errno != errno.EEXIST: raise
	textfile = open(output_loc_txt,'w')

	for i in range(len(ob_arr)):
		hd.double_printer('\n   ### {0} $$$\n\n'.format(ob_arr[i]),textfile)
		for j in range(len(C_ARR)):
			folder = PATH+'/{0}LP{1}'.format(ob_arr[i],C_ARR[j])
			if os.path.isdir(folder) == True:
				hd.double_printer('{0} {1}\n'.format(os.path.isdir(folder),folder),textfile)
				for k in range(len(lp_folder_array)):
					sub_folder = folder + '/{0}'.format(lp_folder_array[k])
					if os.path.isdir(sub_folder) == True:
						hd.double_printer('{0}    {1}'.format(os.path.isdir(sub_folder),sub_folder),textfile)
						if k == 0 and os.path.isdir(sub_folder) == True:
							file_counter = 0
							items = os.listdir(sub_folder)
							for names in items:
								if names.endswith ( ".fits" ) == True and names.endswith ( "t.fits" ) == False and names.endswith ( "k.fits" ) == False:
									file_counter += 1
							hd.double_printer('      {0}\n'.format(file_counter),textfile)
						else: hd.double_printer('\n',textfile)
					else: hd.double_printer('         {0}    <--- False\n'.format(sub_folder),textfile)
			else: hd.double_printer('     {0}    <--- False\n'.format(folder),textfile)
	textfile.close()

# Same previous function but now for LaSilla. It is a distinct function since the folder structure is slightly different and it makes it less messy.
def lasilla_list_folders():
	start_date = '20171116'
	end_date = '20181231'
	ob_arr = hd.observation_dates(start_date,end_date,skip=False)
	ls_folder_array = ('binned','lightcurves')
	PATH = '/data5/mascara/LaSilla'

	output_loc_txt = '/data5/bruinsma/general_documents/lasilla_list_folders.txt'
	try: os.makedirs('/data5/bruinsma/general_documents')
	except OSError as sys.exit: 
		if sys.exit.errno != errno.EEXIST: raise
	textfile = open(output_loc_txt,'w')

	for i in range(len(ob_arr)):
		hd.double_printer('\n   ### {0} ### \n\n'.format(ob_arr[i]),textfile)
		for j in range(len(C_ARR)):
			folder = PATH+'/{0}LS{1}'.format(ob_arr[i],C_ARR[j])
			if os.path.isdir(folder) == True:
				hd.double_printer('{0} {1}\n'.format(os.path.isdir(folder),folder),textfile)
				for k in range(len(ls_folder_array)):
					sub_folder = folder + '/{0}'.format(ls_folder_array[k])
					if os.path.isdir(sub_folder) == True:
						hd.double_printer('{0}    {1}'.format(os.path.isdir(sub_folder),sub_folder),textfile)
						if k == 0 and os.path.isdir(sub_folder) == True:
							file_counter = 0
							items = os.listdir(sub_folder)
							for names in items:
								if names.endswith(".fits.gz") == True or (names.endswith('.fits') == True and names.endswith('k.fits') == False and names.endswith('t.fits') == False and names.endswith('s.fits') == False):
									file_counter += 1
							hd.double_printer('      {0}\n'.format(file_counter),textfile)
						else: hd.double_printer('\n',textfile)
					else: hd.double_printer('         {0}    <--- False\n'.format(sub_folder),textfile)
			else: hd.double_printer('     {0}    <--- False\n'.format(folder),textfile)
	textfile.close()

#lasilla_list_folders()

# Lists all the LSTMID's of all fits files in period of 2017-2018.
def lapalma_fits_info(): # Takes approximately an hour to run, produces a .txt file with 2*10^5 lines.
	output_loc_txt = '/data5/bruinsma/general_documents/lapalma_fits_info.txt'
	try: os.makedirs('/data5/bruinsma/general_documents')
	except OSError as sys.exit: 
		if sys.exit.errno != errno.EEXIST: raise
	textfile = open(output_loc_txt,'w')

	hd.double_printer('JDMID, LSTMID, EXPTIME, NEXP, BINNED data for each .fits file for each camera, in the period of 2017-2018, extracted from the header.\n',textfile)

	PATH = '/data5/mascara/LaPalma'
	date_and_cam_folders = sorted(os.listdir(PATH))

	for k in range(len(date_and_cam_folders)):
		hd.double_printer('\n   ### {0} ###\n\n'.format(date_and_cam_folders[k]),textfile)
		image_folder = PATH+'/'+date_and_cam_folders[k]+'/binned'
		if os.path.isdir(image_folder):
			raw_images_list = sorted(os.listdir(image_folder))
			images_list = []
			for i in range(len(raw_images_list)):
				if raw_images_list[i].endswith ( ".fits" ) == True and raw_images_list[i].endswith ( "t.fits" ) == False and raw_images_list[i].endswith ( "k.fits" ) == False:
					images_list.append(raw_images_list[i])
			for i in range(len(images_list)):
				if i == 0: hd.double_printer('File                    JDMID         LSTMID  EXPTIME NEXP BINNING\n',textfile)
				file = PATH+'/'+date_and_cam_folders[k]+'/binned/'+images_list[i]
				if images_list[i] == '20170516T020454LPE.fits' or images_list[i] == '20170912T233213LPC.fits' or images_list[i] == '20170912T225459LPE.fits' or images_list[i] == '20171226T212116LPW.fits': # The files that cannot be opened (for some unknown reason).
					hd.double_printer('{0} ### CORRUPT FILE ###\n'.format(images_list[i]),textfile)
				else:
					header = fits.getheader(file,1)
					if 'BINNING' in header: # Apparently BINNED doesn't exist in every header.
						hd.double_printer('{0} {1:13.5f} {2:06.3f}  {3:05.4f}  {4:02.0f}   {4:02.0f}\n'.format(images_list[i],header['JDMID'],header['LSTMID'],header['EXPTIME'],header['NEXP'],header['BINNING']),textfile)
					else:
						hd.double_printer('{0} {1:13.5f} {2:06.3f}  {3:05.4f}  {4:02.0f}   NON-EXISTENT\n'.format(images_list[i],header['JDMID'],header['LSTMID'],header['EXPTIME'],header['NEXP']),textfile)

	textfile.close()

def lasilla_fits_info():
	output_loc_txt = '/data5/bruinsma/general_documents/lasilla_fits_info_2018.txt'
	try: os.makedirs('/data5/bruinsma/general_documents')
	except OSError as sys.exit: 
		if sys.exit.errno != errno.EEXIST: raise
	textfile = open(output_loc_txt,'w')

	hd.double_printer('FILENAME, LSTSEQ, JDMID, LSTMID, EXPTIME, NIMAGES data for each .fits file for each camera, in the period of nov-dec 2018, extracted from the header.\n',textfile)

	PATH = '/data5/mascara/LaSilla'
	date_and_cam_folders_raw = sorted(os.listdir(PATH))
	date_and_cam_folders = []

	for k in range(len(date_and_cam_folders_raw)):
		if date_and_cam_folders_raw[k][3] == '8':
			date_and_cam_folders.append(date_and_cam_folders_raw[k])

	for k in range(len(date_and_cam_folders)):
		hd.double_printer('\n   ### {0} ###\n\n'.format(date_and_cam_folders[k]),textfile)
		image_folder = PATH+'/'+date_and_cam_folders[k]+'/binned'
		if os.path.isdir(image_folder):
			raw_images_list = sorted(os.listdir(image_folder))
			images_list = []
			for i in range(len(raw_images_list)):
				if raw_images_list[i].endswith ('.fits.gz') == True or (raw_images_list[i].endswith('.fits') == True and raw_images_list[i].endswith('s.fits') == False and raw_images_list[i].endswith('t.fits') == False and raw_images_list[i].endswith('k.fits') == False):
					images_list.append(raw_images_list[i])
			for i in range(len(images_list)):
				if i == 0: hd.double_printer('FILENAME                LSTSEQ   JDMID         LSTMID  EXPTIME  NIMAGES\n',textfile)
				file = PATH+'/'+date_and_cam_folders[k]+'/binned/'+images_list[i]
				header = fits.getheader(file)
				if 'LSTSEQ' in header:
					hd.double_printer('{0} {1:08.0f} {2:13.5f} {3:06.3f}  {4:05.4f}   {5:02.0f}\n'.format(images_list[i],header['LSTSEQ'],header['JDMID'],header['LSTMID'],header['EXPTIME'],header['NIMAGES']),textfile)
				else:
					header = fits.getheader(file,1)
					hd.double_printer('{0} {1:08.0f} {2:13.5f} {3:06.3f}  {4:05.4f}   {5:02.0f}\n'.format(images_list[i],header['LSTSEQ'],header['JDMID'],header['LSTMID'],header['EXPTIME'],header['NIMAGES']),textfile)
	textfile.close()

lasilla_fits_info()

def lapalma_fits_julian_date(): # Takes approximately an hour to run, produces a .txt file with 2*10^5 lines.
	PATH = '/data5/mascara/LaPalma'
	date_and_cam_folders = sorted(os.listdir(PATH))

	# Create arrays for each camera.
	center = []; eastern = []; northern = []; southern = []; western = []

	# Split date_and_cam_folders into 5 arrays; 1 for each camera.
	for k in range(len(date_and_cam_folders)):
		if date_and_cam_folders[k][-1] == 'C': center.append(date_and_cam_folders[k])
		elif date_and_cam_folders[k][-1] == 'E': eastern.append(date_and_cam_folders[k])
		elif date_and_cam_folders[k][-1] == 'N': northern.append(date_and_cam_folders[k])
		elif date_and_cam_folders[k][-1] == 'S': southern.append(date_and_cam_folders[k])
		elif date_and_cam_folders[k][-1] == 'W': western.append(date_and_cam_folders[k])

	date_and_cam_folders = []
	date_and_cam_folders.append(center); date_and_cam_folders.append(eastern); date_and_cam_folders.append(northern)
	date_and_cam_folders.append(southern); date_and_cam_folders.append(western)

	for k in range(len(date_and_cam_folders)):
		output_loc_txt = '/data5/bruinsma/general_documents/julian_dates/{0}_lapalma_fits_julian_date.txt'.format(date_and_cam_folders[k][0][-1])
		try: os.makedirs('/data5/bruinsma/general_documents/julian_dates')
		except OSError as sys.exit: 
			if sys.exit.errno != errno.EEXIST: raise

		textfile = open(output_loc_txt,'w')

		for j in range(len(date_and_cam_folders[k])):
			image_folder = PATH+'/'+date_and_cam_folders[k][j]+'/binned'
			if os.path.isdir(image_folder):
				raw_images_list = sorted(os.listdir(image_folder))
				images_list = []
				for i in range(len(raw_images_list)):
					if raw_images_list[i].endswith ( ".fits" ) == True and raw_images_list[i].endswith ( "t.fits" ) == False and raw_images_list[i].endswith ( "k.fits" ) == False:
						images_list.append(raw_images_list[i])
				for i in range(len(images_list)):
					file = PATH+'/'+date_and_cam_folders[k][j]+'/binned/'+images_list[i]
					if images_list[i] == '20170516T020454LPE.fits' or images_list[i] == '20170912T233213LPC.fits' or images_list[i] == '20170912T225459LPE.fits' or images_list[i] == '20171226T212116LPW.fits': # The files that cannot be opened (for some unknown reason).
						hd.double_printer('{0} ### CORRUPT FILE ###\n'.format(images_list[i]),textfile)
					else:
						header = fits.getheader(file,1)
						hd.double_printer('{0} {1}\n'.format(images_list[i],header['JDMID']),textfile)

		textfile.close()

# Displays the RA/DEC range of each camera for a chosen night/period of nights.
# Probably does not work 100 percent correctly. However, this is a relatively unimportant program, so it doesn't matter that much. Probably would take a 1~2 hours to fix, if not less.
def lasilla_camera_range():
	start_date = raw_input('First night of observation (YYYYMMDD):     ')
	end_date = raw_input('Last night of observation:                 ')
	raw_ob_arr = hd.observation_dates(start_date,end_date,skip=True)
	step_size_days = raw_input('Day interval:                              ')
	O_ARR = []

	for i in range(len(raw_ob_arr)):
		if i % int(step_size_days) == 0:
			O_ARR.append(raw_ob_arr[i])
	
	step_size_binned = raw_input('Step size binned images:                   ')

	output_loc_txt = '/data5/bruinsma/general_documents/camera_range/lasilla_camera_range_{0}_{1}_stepsizedays={2}_stepsizebinned={3}.txt'.format(start_date,end_date,step_size_days,step_size_binned)
	try: os.makedirs('/data5/bruinsma/general_documents/camera_range') # Make star directory if it does not exist.
	except OSError as sys.exit:
		if sys.exit.errno != errno.EEXIST: raise

	textfile = open(output_loc_txt,'w') # Open text file.

	for i in range(len(O_ARR)):
		for j in range(len(C_ARR)):
			hd.double_printer('\n   ### {0}LS{1} ###\n\n'.format(O_ARR[i],C_ARR[j]),textfile)
			datafile = '/data5/mascara/LaSilla/{0}LS{1}/lightcurves/fast_{0}LS{1}.hdf5'.format(O_ARR[i],C_ARR[j])

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
					imagefile = '/data5/mascara/LaSilla/{0}LS{1}/binned/bin_{2}LS{1}.fits.gz'.format ( O_ARR[i], C_ARR[j], lstseq1[k])

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

					RA_min_0 = 360; RA_max_0 = 0
					RA_min_1 = 360; RA_max_1 = 360		
					DEC_min = 90; DEC_max = -90
					

					for n in range(len(newcat)):
						if newcat[n][6] < RA_min_0: RA_min_0 = newcat[n][6]
						if newcat[n][6] > RA_max_0: RA_max_0 = newcat[n][6]
						if newcat[n][6] <= 180:
							if newcat[n][6]+360 > RA_max_1: RA_max_1 = newcat[n][6]
						if newcat[n][6] > 180:
							if newcat[n][6] < RA_min_1: RA_min_1 = newcat[n][6]
						if newcat[n][8] < DEC_min: DEC_min = newcat[n][8]
						if newcat[n][8] > DEC_max: DEC_max = newcat[n][8]

					if k == 0: hd.double_printer('k    LST1     LSTSEQ1   RA_MIN_0  RA_MAX_0  RA_MIN_1  RA_MAX_1  DEC_MIN  DEC_MAX  RA_RANGE_0  RA_RANGE_1  DEC_RANGE\n',textfile)
					hd.double_printer('{10:03.0f}  {11}  {0}  {1:07.3f}   {2:07.3f}   {3:07.3f}   {4:07.3f}   {5:07.3f}  {6:07.3f}  {7:07.3f}     {8:07.3f}     {9:07.3f}\n'.format(lstseq1[k],RA_min_0,RA_max_0,RA_min_1,RA_max_1,DEC_min,DEC_max,RA_max_0-RA_min_0,RA_max_1-RA_min_1+360,DEC_max-DEC_min,k,hd.h2hm(lst1[k])),textfile)

	textfile.close()

# Displays folder structure inside /data5/bruinsma. This function isn't written that efficient and nice, but it works.
def folder_structure():
	output_loc_txt = '/data5/bruinsma/general_documents/folder_structure.txt'
	try: os.makedirs('/data5/bruinsma/general_documents/') # Make directory if it does not exist.
	except OSError as sys.exit:
		if sys.exit.errno != errno.EEXIST: raise

	textfile = open(output_loc_txt,'w') # Open text file.

	l0 = '/data5/bruinsma'
	PATH = l0
	l1 = os.listdir(PATH)
	file_counter = 0
	for i in range(len(l1)):
		if os.path.isfile(PATH+'/'+l1[i]):
			file_counter += 1
	if file_counter == 0: hd.double_printer('      {1}\n'.format(file_counter,PATH),textfile)
	if file_counter > 0 and file_counter < 10: hd.double_printer('{0}     {1}\n'.format(file_counter,PATH),textfile)
	if file_counter >= 10 and file_counter < 100: hd.double_printer('{0}    {1}\n'.format(file_counter,PATH),textfile)
	if file_counter >= 100 and file_counter < 1000: hd.double_printer('{0}   {1}\n'.format(file_counter,PATH),textfile)
	if file_counter >= 1000 and file_counter < 10000: hd.double_printer('{0}  {1}\n'.format(file_counter,PATH),textfile)
	for i in range(len(l1)):
		PATH = l0+'/'+l1[i]
		if os.path.isdir(PATH):
			l2 = os.listdir(PATH)
			file_counter = 0
			for j in range(len(l2)):
				if os.path.isfile(PATH+'/'+l2[j]):
					file_counter += 1
			if file_counter == 0: hd.double_printer('      {1}\n'.format(file_counter,PATH),textfile)
			if file_counter > 0 and file_counter < 10: hd.double_printer('{0}     {1}\n'.format(file_counter,PATH),textfile)
			if file_counter >= 10 and file_counter < 100: hd.double_printer('{0}    {1}\n'.format(file_counter,PATH),textfile)
			if file_counter >= 100 and file_counter < 1000: hd.double_printer('{0}   {1}\n'.format(file_counter,PATH),textfile)
			if file_counter >= 1000 and file_counter < 10000: hd.double_printer('{0}  {1}\n'.format(file_counter,PATH),textfile)
			for j in range(len(l2)):
				PATH = l0+'/'+l1[i]+'/'+l2[j]
				if os.path.isdir(PATH):
					l3 = os.listdir(PATH)
					file_counter = 0
					for k in range(len(l3)):
						if os.path.isfile(PATH+'/'+l3[k]):
							file_counter += 1
					if file_counter == 0: hd.double_printer('      {1}\n'.format(file_counter,PATH),textfile)
					if file_counter > 0 and file_counter < 10: hd.double_printer('{0}     {1}\n'.format(file_counter,PATH),textfile)
					if file_counter >= 10 and file_counter < 100: hd.double_printer('{0}    {1}\n'.format(file_counter,PATH),textfile)
					if file_counter >= 100 and file_counter < 1000: hd.double_printer('{0}   {1}\n'.format(file_counter,PATH),textfile)
					if file_counter >= 1000 and file_counter < 10000: hd.double_printer('{0}  {1}\n'.format(file_counter,PATH),textfile)
					for k in range(len(l3)):
						PATH = l0+'/'+l1[i]+'/'+l2[j]+'/'+l3[k]
						if os.path.isdir(PATH):
							l4 = os.listdir(PATH)
							file_counter = 0
							for l in range(len(l4)):
								if os.path.isfile(PATH+'/'+l4[l]):
									file_counter += 1
							if file_counter == 0: hd.double_printer('      {1}\n'.format(file_counter,PATH),textfile)
							if file_counter > 0 and file_counter < 10: hd.double_printer('{0}     {1}\n'.format(file_counter,PATH),textfile)
							if file_counter >= 10 and file_counter < 100: hd.double_printer('{0}    {1}\n'.format(file_counter,PATH),textfile)
							if file_counter >= 100 and file_counter < 1000: hd.double_printer('{0}   {1}\n'.format(file_counter,PATH),textfile)
							if file_counter >= 1000 and file_counter < 10000: hd.double_printer('{0}  {1}\n'.format(file_counter,PATH),textfile)
							for l in range(len(l4)):
								PATH = l0+'/'+l1[i]+'/'+l2[j]+'/'+l3[k]+'/'+l4[l]
								if os.path.isdir(PATH):
									l5 = os.listdir(PATH)
									file_counter = 0
									for m in range(len(l5)):
										if os.path.isfile(PATH+'/'+l5[m]):
											file_counter += 1
									if file_counter == 0: hd.double_printer('      {1}\n'.format(file_counter,PATH),textfile)
									if file_counter > 0 and file_counter < 10: hd.double_printer('{0}     {1}\n'.format(file_counter,PATH),textfile)
									if file_counter >= 10 and file_counter < 100: hd.double_printer('{0}    {1}\n'.format(file_counter,PATH),textfile)
									if file_counter >= 100 and file_counter < 1000: hd.double_printer('{0}   {1}\n'.format(file_counter,PATH),textfile)
									if file_counter >= 1000 and file_counter < 10000: hd.double_printer('{0}  {1}\n'.format(file_counter,PATH),textfile)
									for m in range(len(l5)):
										PATH = l0+'/'+l1[i]+'/'+l2[j]+'/'+l3[k]+'/'+l4[l]+'/'+l5[m]
										if os.path.isdir(PATH):
											l6 = os.listdir(PATH)
											file_counter = 0
											for n in range(len(l6)):
												if os.path.isfile(PATH+'/'+l6[n]):
													file_counter += 1
											if file_counter == 0: hd.double_printer('      {1}\n'.format(file_counter,PATH),textfile)
											if file_counter > 0 and file_counter < 10: hd.double_printer('{0}     {1}\n'.format(file_counter,PATH),textfile)
											if file_counter >= 10 and file_counter < 100: hd.double_printer('{0}    {1}\n'.format(file_counter,PATH),textfile)
											if file_counter >= 100 and file_counter < 1000: hd.double_printer('{0}   {1}\n'.format(file_counter,PATH),textfile)
											if file_counter >= 1000 and file_counter < 10000: hd.double_printer('{0}  {1}\n'.format(file_counter,PATH),textfile)
											for n in range(len(l6)):
												PATH = l0+'/'+l1[i]+'/'+l2[j]+'/'+l3[k]+'/'+l4[l]+'/'+l5[m]+'/'+l6[n]
												if os.path.isdir(PATH):
													l7 = os.listdir(PATH)
													file_counter = 0
													for o in range(len(l7)):
														if os.path.isfile(PATH+'/'+l7[o]):
															file_counter += 1
													if file_counter == 0: hd.double_printer('      {1}\n'.format(file_counter,PATH),textfile)
													if file_counter > 0 and file_counter < 10: hd.double_printer('{0}     {1}\n'.format(file_counter,PATH),textfile)
													if file_counter >= 10 and file_counter < 100: hd.double_printer('{0}    {1}\n'.format(file_counter,PATH),textfile)
													if file_counter >= 100 and file_counter < 1000: hd.double_printer('{0}   {1}\n'.format(file_counter,PATH),textfile)
													if file_counter >= 1000 and file_counter < 10000: hd.double_printer('{0}  {1}\n'.format(file_counter,PATH),textfile)
													for o in range(len(l7)):
														PATH = l0+'/'+l1[i]+'/'+l2[j]+'/'+l3[k]+'/'+l4[l]+'/'+l5[m]+'/'+l6[n]+'/'+l7[o]
														if os.path.isdir(PATH):
															l8 = os.listdir(PATH)
															file_counter = 0
															for p in range(len(l8)):
																if os.path.isfile(PATH+'/'+l8[p]):
																	file_counter += 1
															if file_counter == 0: hd.double_printer('      {1}\n'.format(file_counter,PATH),textfile)
															if file_counter > 0 and file_counter < 10: hd.double_printer('{0}     {1}\n'.format(file_counter,PATH),textfile)
															if file_counter >= 10 and file_counter < 100: hd.double_printer('{0}    {1}\n'.format(file_counter,PATH),textfile)
															if file_counter >= 100 and file_counter < 1000: hd.double_printer('{0}   {1}\n'.format(file_counter,PATH),textfile)
															if file_counter >= 1000 and file_counter < 10000: hd.double_printer('{0}  {1}\n'.format(file_counter,PATH),textfile)