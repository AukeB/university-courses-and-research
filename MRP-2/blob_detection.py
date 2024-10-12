import numpy as np
import os
import bdsf
import argparse

def main(pointing,frequency,pointing_dir,catalog_dir,box_center,box_size,show_fit=False,):
	# Filenames.
	filename = '{0}{1}.fits'.format(pointing_dir,pointing)
	catalog_filename = '{0}{1}_catalog_({2},{3})_({4},{5}).fits'.format(catalog_dir,pointing,box_center[0],box_center[1],box_size[0],box_size[1])

	# Compute box parameters.
	box = (box_center[0]-box_size[0]/2,box_center[0]+box_size[0]/2,box_center[1]-box_size[1]/2,box_center[1]+box_size[1]/2)

	#if os.path.exists(catalog_filename) == True:
	x = bdsf.process_image(filename,frequency=frequency,thresh_isl=4.0,thresh_pix=5.0,trim_box=box)
	if show_fit == True:		
		x.show_fit()
	x.write_catalog(outfile=catalog_filename,catalog_type='gaul',format='fits',clobber=True)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('-pointing')
	parser.add_argument('-frequency')
	parser.add_argument('-pointing_dir')
	parser.add_argument('-catalog_dir')
	parser.add_argument('--box_center', help = 'Center pixel coordinates of the trim box.', default = '5500,5500')
	parser.add_argument('--box_size', help = 'Size of the trim box.', default = '1000,1000')
	parser.add_argument('--show_fit', help = 'Show the fit of the gaussians produced by PyBDSF', default = True)

	args = parser.parse_args()

	box_center = np.array(args.box_center.split(','),dtype = int)
	box_size = np.array(args.box_size.split(','),dtype = int)

	main(pointing=args.pointing,frequency=args.frequency,pointing_dir=args.pointing_dir,catalog_dir=args.catalog_dir,
box_center=box_center,box_size=box_size,show_fit=False)
