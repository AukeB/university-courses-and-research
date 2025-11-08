# Imports
import numpy

from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.nddata.utils import Cutout2D
from astropy.io import fits
from astropy.wcs import WCS
from astropy.visualization import ZScaleInterval
from astropy.table import Table

import handy

def cutout_lofar(pointing_dir,pointing,output_dir,ra,dec,cutout_size,make_fits=True):
	pointing_path = f'{pointing_dir}{pointing}.fits'
	
	# Make Astropy sky coordinates.
	cutout_coords = SkyCoord(ra,dec,frame='icrs',unit=(u.deg,u.deg))

	# Open the fits file, but do not load all the data into RAM but read what is necessary
	with fits.open(pointing_path,memmap=True) as hdul:
		data = hdul[0].data
		header = hdul[0].header

		wcs = WCS(header)

	#the field objects have 2 extra dimensions which we have to collapse!
	#the mosaics have the proper 2 dimensions already
	#we also need to make a new WCS
	if len(data.shape) > 2:
		data = data[0,0]

		wcs = WCS(naxis = 2)
		wcs.wcs.ctype = [header['CTYPE1'], header['CTYPE2']]#['RA---TAN', 'DEC--TAN']
		wcs.wcs.crval = [header['CRVAL1'], header['CRVAL2']]
		wcs.wcs.crpix = [header['CRPIX1'], header['CRPIX2']]
		wcs.wcs.cunit = [header['CUNIT1'], header['CUNIT2']]
		wcs.wcs.cdelt = [header['CDELT1'], header['CDELT2']]

	# Makes a cutout object
	cutout = Cutout2D(data, cutout_coords, cutout_size, wcs = wcs, mode = 'partial')
	
	if make_fits == True:
		# Save cutout as fits file.
		fits_output_dir = output_dir+'fits/'
		handy.folder(fits_output_dir)
		hdul[0].data = cutout.data
		hdul[0].header.update(cutout.wcs.to_header())
		cutout_filename = '{0}{1}_{2:.2f}_{3:.2f}_{4:.0f}.fits'.format(fits_output_dir,pointing,ra,dec,cutout_size)
		hdul.writeto(cutout_filename,overwrite=True)
		print(f' Cutout .fits file has been saved as {cutout_filename}.')

	return cutout

def cutout_panstarrs(fig, ra, dec, cutout_size, already_downloaded, rgb_filters = 'irg', subplot_idx = 122, percentile_value = 99.5):
	#### now plot as RGB image
	#load the three filters
	img_array = []
	wcs_array = []
	for f in rgb_filters:
		p_downloadname = getPanSTARRSdownloadname(P_download_loc, f_ra, f_dec, p_size, f)

		#open the fits file, but do not load all the data into RAM but read what is necessary
		with fits.open(p_downloadname, memmap = False) as hdul:
			# print(hdul[0].info())
			header = hdul[0].header
			# print(header['NAXIS1'], header['NAXIS2'])

			try:
				data = hdul[0].data
			except ValueError: #array has incorrect shape
				tqdm.write('Warning: data has incorrect shape, replacing with zeroes')
				data = np.zeros((header['NAXIS1'], header['NAXIS2']))

			wcs = WCS(header)

		#smooth image using a gaussian filter
		data = gaussian_filter(data, 2)

		img_array.append(data)
		wcs_array.append(wcs)

	img_array = np.array(img_array)
	img_array = np.moveaxis(img_array, 0, 2)

	#scale with minmax
	# img_array = scaleRGBarray(img_array)
	#apply transformations for visualization
	transform = AsinhStretch() + PercentileInterval(percentile_value)
	t_image = transform(img_array)

	#set all pixels with nans to 1
	t_image[np.isnan(t_image)] = 1

	#### Plot
	ax = fig.add_subplot(subplot_idx, projection = wcs_array[0])

	ax.imshow(t_image)

	setAxisLabels(ax)
	setTitle(ax, f'PanSTARRS {rgb_filters[0]}, {rgb_filters[1]} and {rgb_filters[2]}')

	return ax, wcs_array[0], img_array.shape[:2], plot_bbox
	
