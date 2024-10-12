import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
import os, sys, random

# Paths and filenames.
PATH = "/home/auke/Desktop/NN/NN_ass_1/" # Change this to the directory where the code is located.
train_in_path = "data/train_in.csv" # Put all the .csv files in a folder called data.
train_out_path = "data/train_out.csv"
test_in_path = "data/test_in.csv"
test_out_path = "data/test_out.csv"

# Importing data.
train_in = np.genfromtxt(PATH+train_in_path,dtype='float',delimiter=',')
train_out = np.genfromtxt(PATH+train_out_path,dtype='float',delimiter=',')
test_in = np.genfromtxt(PATH+test_in_path,dtype='float',delimiter=',')
test_out = np.genfromtxt(PATH+test_out_path,dtype='float',delimiter=',')

def reshaper(data_set): # Converts (1707,256) vectors to (1707,16,16) matrices.
	return data_set.reshape(len(data_set),int(len(data_set[0])**0.5),int(len(data_set[0])**0.5))

def terminal_printer(data_set,label,n):
	sys.stdout.write("\n")
	for i in range(len(data_set[n])):
		for j in range(len(data_set[n][i])):
			if data_set[n][i][j] < 0: sys.stdout.write("{:05.2f} ".format(data_set[n][i][j]))
			else: sys.stdout.write(" {:04.2f} ".format(data_set[n][i][j]))
		sys.stdout.write("\n")
	sys.stdout.write("\n")

def printer(data_set,label,string,n):
	plt.imshow(data_set[n],interpolation='nearest')
	plt.set_cmap('Greys')
	plt.title("{0}".format(int(label[n])))
	plt.xlabel("pixel")
	plt.ylabel("pixel")
	plt.colorbar()
	if not os.path.exists(PATH+"plots/NN_ass_01_digits/"): os.makedirs(PATH+"/plots/NN_ass_01_digits/")
	plt.savefig("plots/NN_ass_01_digits/{1}_{0}.png".format(n,string))
	#plt.show()
	#sys.stdout.write("Image saved as plots/NN_ass_01_digits/{1}_{0}.png.\n".format(n,string))
	plt.close()

def show_me_the_digit(data_set,label,string,start,stop):
	for n in range(stop-start):
		#print(sum(i == -1 for i in train_in[start+n]))
		#print(sum(sum(i == -1 for i in train_in[start+n])))
		#terminal_printer(data_set,label,start+n)
		printer(data_set,label,string,start+n)

train_in = reshaper(train_in)
test_in = reshaper(test_in)
data_set = test_in
label = test_out
string = "test"
start = 0
stop = 1000

show_me_the_digit(data_set,label,string,start,stop)

