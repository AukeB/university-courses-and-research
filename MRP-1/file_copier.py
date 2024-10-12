import os
import numpy as np
import shutil

def gif_copier():
	star = 'ProxCen'#raw_input('Star [ASCC/NAME]: ')

	MAIN_PATH = '/data5/bruinsma/stars/'+star
	folder_list = sorted(os.listdir(MAIN_PATH))
	file_path_list = []

	for i in range(len(folder_list)):
		PATH = MAIN_PATH+'/'+folder_list[i]+'/gifs'+'/pr20'
		file_list = os.listdir(PATH)
		for j in range(len(file_list)):
			FILE_PATH = PATH+'/'+file_list[j]
			file_path_list.append(FILE_PATH)

	for i in range(len(file_path_list)):
		shutil.copy(file_path_list[i],'/home/bruinsma/Desktop/gifs')
		print(i,len(file_path_list))

def lightcurve_copier():
	star = 'ProxCen'#raw_input('Star [ASCC/NAME]: ')

	MAIN_PATH = '/data5/bruinsma/stars/'+star
	folder_list = sorted(os.listdir(MAIN_PATH))
	file_path_list = []

	for i in range(len(folder_list)):
		PATH = MAIN_PATH+'/'+folder_list[i]+'/lightcurves'+'/individual'
		file_list = os.listdir(PATH)
		for j in range(len(file_list)):
			FILE_PATH = PATH+'/'+file_list[j]
			file_path_list.append(FILE_PATH)

	for i in range(len(file_path_list)):
		shutil.copy(file_path_list[i],'/home/bruinsma/Desktop/files/lightcurves')
		print(i,len(file_path_list))

lightcurve_copier()