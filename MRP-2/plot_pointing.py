# Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import Ellipse
from astropy import units as u
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage.filters import gaussian_filter
from astropy.visualization import ZScaleInterval, PercentileInterval, AsinhStretch




import handy

def plot_cutout_lofar(cutout,pointing,output_dir,cutout_size):
	# Some changes to the data.
	data = cutout.data*1e3 # Convert to mJy/beam
	data[data<0]=0 # Change negative values to zero for no warnings during sqrt scaling.
	
	norm = (colors.PowerNorm(gamma=1),colors.LogNorm(),colors.PowerNorm(gamma=2),colors.PowerNorm(gamma=0.5))
	norm_names = ('linear','logarithmic','quadratic','square')

	# Plot figure for different color normalizations.
	for i in range(len(norm)):
		fig = plt.figure(figsize=(12,12)) # Initialise figure with figure size.
		ax = fig.add_subplot(111,projection=cutout.wcs)
		im = ax.imshow(data,origin='lower',cmap='hot',norm=norm[i])
		ra = ax.coords[0]; dec = ax.coords[1] # Correct labels.
		ra.set_format_unit(u.deg); dec.set_format_unit(u.deg)
		ax.set_xlabel('RA (deg)',fontsize=14)
		ax.set_ylabel('DEC (deg)',fontsize=14)
		ax.set_title('LOFAR 150 MHz',fontsize=16)
		txt= f'Pointing: {pointing}\nCutout size: {cutout_size}\nScaling: {norm_names[i]}'	
		plt.figtext(0.128,0.06,txt,wrap=True,horizontalalignment='left',verticalalignment='top',fontsize=12)
		cax = plt.axes([0.92,0.1095,0.025,0.77]) # Manually set. Don't change figsize.
		plt.colorbar(im,cax=cax) # Colorbar.
		cax.set_ylabel('Flux [mJy/beam]',fontsize=13)
		filename = f'{output_dir}/{pointing}_cutout_{cutout_size}_{norm_names[i]}.png'
		plt.savefig(filename,dpi=200,bbox_inches='tight')
		print(f' Cutout .png file has been saved as {filename}')
		plt.close()

def subplot_cutout_lofar(cutout,pointing,output_dir,cutout_size):
	data = cutout.data*1e3 # Convert to mJy/beam
	data[data<0]=0 # Change negative values to zero for no warnings during sqrt scaling.
	
	norm = (colors.PowerNorm(gamma=1),colors.LogNorm(),colors.PowerNorm(gamma=2),colors.PowerNorm(gamma=0.5))
	norm_names = ('linear','logarithmic','quadratic','square')

	fig = plt.figure(figsize=(14,14)) # Initialise figure with figure size.

	ax1 = fig.add_subplot(221,projection=cutout.wcs)
	ax2 = fig.add_subplot(222,projection=cutout.wcs)
	ax3 = fig.add_subplot(223,projection=cutout.wcs)
	ax4 = fig.add_subplot(224,projection=cutout.wcs)
	
	im1 = ax1.imshow(data,origin='lower',cmap='hot',norm=norm[0])
	im2 = ax2.imshow(data,origin='lower',cmap='hot',norm=norm[1])
	im3 = ax3.imshow(data,origin='lower',cmap='hot',norm=norm[2])
	im4 = ax4.imshow(data,origin='lower',cmap='hot',norm=norm[3])

	ra1 = ax1.coords[0]; dec1 = ax1.coords[1]
	ra2 = ax2.coords[0]; dec2 = ax2.coords[1]
	ra3 = ax3.coords[0]; dec3 = ax3.coords[1]
	ra4 = ax4.coords[0]; dec4 = ax4.coords[1]

	ra1.set_format_unit(u.deg); dec1.set_format_unit(u.deg)
	ra2.set_format_unit(u.deg); dec2.set_format_unit(u.deg)
	ra3.set_format_unit(u.deg); dec3.set_format_unit(u.deg)
	ra4.set_format_unit(u.deg); dec4.set_format_unit(u.deg)

	ax1.set_xlabel('RA (deg)',fontsize=14)
	ax2.set_xlabel('RA (deg)',fontsize=14)
	ax3.set_xlabel('RA (deg)',fontsize=14)
	ax4.set_xlabel('RA (deg)',fontsize=14)

	ax1.set_ylabel('DEC (deg)',fontsize=14)
	ax2.set_ylabel('DEC (deg)',fontsize=14)
	ax3.set_ylabel('DEC (deg)',fontsize=14)
	ax4.set_ylabel('DEC (deg)',fontsize=14)

	ax1.set_title(f'LOFAR 150 MHz - {norm_names[0]}',fontsize=16)
	ax2.set_title(f'LOFAR 150 MHz - {norm_names[1]}',fontsize=16)
	ax3.set_title(f'LOFAR 150 MHz - {norm_names[2]}',fontsize=16)
	ax4.set_title(f'LOFAR 150 MHz - {norm_names[3]}',fontsize=16)

	txt1= f'Pointing: {pointing}\nCutout size: {cutout_size}'	
	plt.figtext(0.128,0.06,txt1,wrap=True,horizontalalignment='left',verticalalignment='top',fontsize=12)
	#cax1 = plt.axes([0.92,0.1095,0.025,0.77]) # Manually set. Don't change figsize.
	#plt.colorbar(im1,cax=cax1) # Colorbar.
	#cax1.set_ylabel('Flux [mJy/beam]',fontsize=13)
	filename = f'{output_dir}/{pointing}_cutout_{cutout_size}_subplot.png'
	plt.savefig(filename,dpi=200,bbox_inches='tight')
	print(f' Cutout .png file has been saved as {filename}')
	plt.close()

def plot_cutout_panstarrs(panstarrs_dir,ra,dec,p_size,rgb_filter='irg'):
	# Now plot as RGB image. Load the three filters.
	img_array = []
	wcs_array = []

	# The RA and DEC used in the filenames.
	f_ra = f'{ra:.2f}'
	f_dec = f'{dec:.2f}'

	for f in rgb_filter:
		file_path = f'{panstarrs_dir}ra={f_ra}_dec={f_dec}_s={p_size}_{f}.fits'

		# Open the fits file, but do not load all the data into RAM but read what is necessary
		with fits.open(file_path,memmap = False) as hdul:
			header = hdul[0].header

			try:
				data = hdul[0].data
			except ValueError: # Array has incorrect shape.
				tqdm.write('Warning: data has incorrect shape, replacing with zeroes')
				data = np.zeros((header['NAXIS1'],header['NAXIS2']))

			wcs = WCS(header)

		# Smooth image using a gaussian filter.
		data = gaussian_filter(data,2)

		img_array.append(data)
		wcs_array.append(wcs)

	img_array = np.array(img_array)
	img_array = np.moveaxis(img_array,0,2)

	# Scale with minmax.
	#img_array = scaleRGBarray(img_array)
	# Apply transformations for visualization.
	percentile_value = 99.5
	transform = AsinhStretch() + PercentileInterval(percentile_value)
	t_image = transform(img_array)

	# Set all pixels with nans to 1.
	t_image[np.isnan(t_image)] = 1

	# Plot.
	fig = plt.figure(figsize=(12,12)) # Initialise figure with figure size.
	ax = fig.add_subplot(111,projection = wcs_array[0])

	ax.imshow(t_image)

	ax.set_title(f'PanSTARRS {rgb_filter[0]}, {rgb_filter[1]} and {rgb_filter[2]}')
	file_path = f'{panstarrs_dir}panstarrs_ra={f_ra}_dec={f_dec}_s={p_size}.png'
	plt.savefig(file_path,dpi=200,bbox_inches='tight')
	print(f' PanSTARRS .png saved as {file_path}.')
	#plt.show()
	plt.close()

def double_plot(cutout,pointing,pointing_dir,cutout_dir,panstarrs_dir,
ra,dec,cutout_size,p_size,rgb_filters='irg'):
	fig = plt.figure(figsize=(16,16)) # Initialise figure with figure size.
	
	# LOFAR Plot.
	
	# Some changes to the data.
	data = cutout.data*1e3 # Convert to mJy/beam
	data[data<0]=0 # Change negative values to zero for no warnings during sqrt scaling.
	
	norm = colors.PowerNorm(gamma=0.5)
	norm_names = 'quadratic'

	ax1 = fig.add_subplot(111,projection=cutout.wcs)
	im = ax1.imshow(data,origin='lower',cmap='hot',norm=norm,alpha=0.7)
	ra = ax1.coords[0]
	dec = ax1.coords[1] # Correct labels.
	ra.set_format_unit(u.deg); dec.set_format_unit(u.deg)
	ax1.set_xlabel('RA (deg)',fontsize=14)
	ax1.set_ylabel('DEC (deg)',fontsize=14)
	ax1.set_title('LOFAR 150 MHz',fontsize=16)
	#txt= f'Pointing: {pointing}\nCutout size: {cutout_size}\nScaling: {norm_names}'	
	#plt.figtext(0.128,0.06,txt,wrap=True,horizontalalignment='left',verticalalignment='top',fontsize=12)
	cax = plt.axes([0.92,0.1095,0.025,0.77]) # Manually set. Don't change figsize.
	plt.colorbar(im,cax=cax) # Colorbar.
	cax.set_ylabel('Flux [mJy/beam]',fontsize=13)

	# PanSTARRS Plot.
	# Now plot as RGB image. Load the three filters.
	img_array = []
	wcs_array = []

	# The RA and DEC used in the filenames.
	#f_ra = f'{ra:.2f}'
	#f_dec = f'{dec:.2f}'

	for f in rgb_filters:
		file_path = f'{panstarrs_dir}ra=217.52_dec=7.26_s={p_size}_{f}.fits'

		# Open the fits file, but do not load all the data into RAM but read what is necessary
		with fits.open(file_path,memmap = False) as hdul:
			header = hdul[0].header

			try:
				data = hdul[0].data
			except ValueError: # Array has incorrect shape.
				tqdm.write('Warning: data has incorrect shape, replacing with zeroes')
				data = np.zeros((header['NAXIS1'],header['NAXIS2']))

			wcs = WCS(header)

		# Smooth image using a gaussian filter.
		data = gaussian_filter(data,2)

		img_array.append(data)
		wcs_array.append(wcs)

	img_array = np.array(img_array)
	img_array = np.moveaxis(img_array,0,2)

	# Scale with minmax.
	#img_array = scaleRGBarray(img_array)
	# Apply transformations for visualization.
	percentile_value = 99.5
	transform = AsinhStretch() + PercentileInterval(percentile_value)
	t_image = transform(img_array)

	# Set all pixels with nans to 1.
	t_image[np.isnan(t_image)] = 1

	# Plot.
	ax2 = fig.add_subplot(111,projection = wcs_array[0])
	ax2.imshow(t_image,alpha=0.7)

	filename = f'{cutout_dir}/{pointing}_PanSTARRS_cutout_{cutout_size}.png'
	plt.savefig(filename,dpi=200,bbox_inches='tight')
	print(f' Cutout .png file has been saved as {filename}')
	plt.show()
	plt.close()

	

def plot_removed_sources(pointing,box_center,box_size,cutout_image,subtracted_image,table_data,pixel_size,
is_point_source,output_dir,draw_ellipses=True):

	fig = plt.figure(figsize=(16,12))
	
	ax1 = fig.add_subplot(121)#,projection=cutout.wcs)
	ax2 = fig.add_subplot(122)#,projection=cutout.wcs)

	im1 = ax1.imshow(cutout_image,cmap='cool')
	im2 = ax2.imshow(subtracted_image,cmap='cool')

	ax1.set_title('Original image',fontsize=16)
	ax2.set_title('Subtracted image',fontsize=16)

	ax1.set_xlabel('Pixels',fontsize=14)
	ax1.set_ylabel('Pixels',fontsize=14)
	ax2.set_xlabel('Pixels',fontsize=14)
	ax2.set_ylabel('Pixels',fontsize=14)

	for i in range(len(table_data['Maj'])):
		amp,x0,y0,Majsigma,Minsigma,theta = handy.getGaussianParams(table_data,pixel_size,i)

		if draw_ellipses == True:
			e = Ellipse((x0, y0),width=Majsigma,height=Minsigma,angle=theta,linewidth=2)
			e.set_facecolor('none')

			# Mark removed sources red, sources which are still present green.
			if i in is_point_source:
				e.set_edgecolor('red')
			else:
				e.set_edgecolor('green')

			ax1.add_artist(e)

	# Check if folder exists.
	handy.folder(output_dir)

	# Save file.
	filename = f'{output_dir}{pointing}_removed_({box_center[0]},{box_center[1]})_({box_size[0]},{box_size[1]}).png'
	print(f' Image saved as {filename}')
	plt.savefig(filename,dpi=200,bbox_inches='tight')
	plt.close()








































