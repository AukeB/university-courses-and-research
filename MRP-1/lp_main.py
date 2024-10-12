# Imports.
import numpy as np
import sys

import lp_lightcurves as lplc
import lp_info as lpinfo
import general_info as gi
import lp_images as lpim

# Instruction program.
def instructions ():
	string = '''
	Instructions:
	1.  Find the star's ASCC number.
	2.  Check if the star is in the FOV of one of the LaPalma
	    cameras using the .hdf5 files in /data3                        [f]
	3.  Check JDMID, LST, LSTSEQ, MAG0, NOBS, X, Y in the .hdf5 
	    data of the star.                                              [m]
	4a. Make lightcurves for each day in the period of 2015-2018.      [l]
	4b. Make lightcurves for each quarter in the period of 2015-2018.  [u]
	    (Only shows images so you can inspect it, does not save it.)
	5a. Make images of a specific star, using the x and y coordinates
	    in the .hdf5 file in the reduced data folder                   [a]

	Other:
	 -  Print and save JDMID, LSTMID, EXPTIME, NEXP, BINNED data 
	    for each .fits file for each camera, in the period of 
	    2017-2018, extracted from the header. Only for LaPalma data.   [j]
	 -  Check which folders exist.                                     [s]           
	'''
	print string

def main():
	sys.stdout.write('\n')
	while True:
		entry = raw_input('Which program do you want to start? ["i" for instructions] ')

		if entry == "i": sys.stdout.write('\nInstruction program executed.\n\n'); instructions()
		if entry == 'f': sys.stdout.write('\nLaPalma visibility program executed.\n\n'); lpinfo.hdf5_checker()
		if entry == 'm': sys.stdout.write('\nLa Palma more data program exectued.\n\n'); lpinfo.hdf5_info()
		if entry == 'l': sys.stdout.write('\nLaPalma lightcurve program executed.\n\n'); lplc.lapalma_lightcurve()
		if entry == 'u': sys.stdout.write('\nLaPalma lightcurve program executed.\n\n'); lplc.lapalma_quarter_lightcurve()
		if entry == 'a': sys.stdout.write('\nLaPalma image maker program executed.\n\n'); lpim.lapalma_images_by_hdf5_coordinates()
		if entry == 'j': sys.stdout.write('\nLaPalma check fits program executed.\n\n'); gi.lapalma_fits_info()
		if entry == 's': sys.stdout.write('\nLaPalma folder check program executed.\n\n'); gi.lapalma_list_folders()
		if entry == "q": sys.stdout.write('\nProgram terminated.\n'); break

	sys.stdout.write('\n')

main()