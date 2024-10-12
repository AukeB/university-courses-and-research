# Imports.
import numpy as np
import sys

import general_info as gi
import handy as hd
import ls_info as lsinfo
import ls_images as im
import ls_lightcurves as lc
import neighbours as nb

# Instructions program.
def instructions ():
    string = '''
    Instructions:
    1.  Find the star's ASCC number.
    2.  Find out when/where it's in the FOV of the camera's.           [n], [2] or [3]
    3.  Check which stars are nearby.                                  [7]
    4a. Plot lightcurves of the star and its surrounding stars.        [4]
    4b. Plot normalized lightcurves.                                   [5]
    5.  Make images/gif files of these stars that correspond 
        with the lightcurves [im.image_maker()].                       [6]

    Other:
     -  Print and save LSTSEQ, JDMID, LSTMID, EXPTIME, NIMAGES data 
        for each .fits file for each camera, in the period of 
        nov-dec 2018, extracted from the header. Only for LaSilla data.[j]
     -  Check which folders exist.                                     [s]  
     -  Check the RA/DEC range of each camera.                         [c]         
    '''
    print string
		
def main ():
    telescope_loc = 'LaSilla' # Default. # <--- Line needs to deleted.

    sys.stdout.write('\n')
    while True:
        entry = raw_input('Which program do you want to start? ["i" for instructions] ')
        if entry == 'i': sys.stdout.write('Instruction program executed.\n\n'); instructions ()
        if entry == 's': sys.stdout.write('LaSilla folder check program executed.\n\n'); gi.lasilla_list_folders()
        if entry == 'j': sys.stdout.write('LaSilla fits file check program executed.\n\n'); gi.lasilla_fits_info()
        if entry == 'n': sys.stdout.write('info.star() executed.\n\n'); lsinfo.info_star()
        if entry == 'v': sys.stdout.write('Star visibility program executed:\n\n'); lsinfo.star_visibility()
        #if entry == '2': sys.stdout.write('info.whole_night() executed.\n\n'); info.whole_night ( telescope_loc )
        #if entry == '3': sys.stdout.write('info.part_night () executed.\n\n'); info.part_night ( telescope_loc )
        if entry == 'l': sys.stdout.write('lc.lightcurve_plotter() executed.\n\n'); lc.lightcurve_plotter()
        if entry == '5': sys.stdout.write('lc.lightcurve_normalizer() executed.\n\n'); lc.lightcurve_normalizer()
        #if entry == '6': sys.stdout.write('im.image_maker() executed.\n\n'); im.image_maker()
        if entry == 'm': sys.stdout.write('LaSilla image maker program executed\n\n'); im.image_maker()
        if entry == '7': sys.stdout.write('nb.closest_star() executed.\n\n'); nb.closest_stars()
        
        if entry == 'c': sys.stdout.write('Check camera range program executed.\n\n'); gi.lasilla_camera_range()
        if entry == 'q': sys.stdout.write('\nProgram terminated.\n'); break

    sys.stdout.write('\n')

main ()