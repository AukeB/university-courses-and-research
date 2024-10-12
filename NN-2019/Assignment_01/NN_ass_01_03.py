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

# Bin data.
min_value = 0 # Minimum value. Large values to make sure all 1707 (and the 1000 from the test set) digits are within the range of the bin array.
max_value = 1 # Maximum value.
bin_size = 0.05 # Width of a bin
bins = np.linspace(min_value,max_value,(1/bin_size)*(max_value-min_value)+1) # Bins.

# Feature data.
count_arr = np.zeros(10) # Array that displays the occurence of each digit.
feature = np.zeros(len(train_in)) # Values of our Bayesian classifier.
feature_sorted = np.zeros((10,len(train_in))) # Contains a lot of empty spaces.
feature_binned = np.zeros((10,len(bins)-1))

# Results
correctly_classified = 0

# Probabilities.
P_C = np.zeros(10)
P_X_C = np.zeros((10,len(bins)-1))
P_X = np.zeros(len(bins)-1)
P_C_X = np.zeros((10,len(bins)-1))

# Compute features.
for i in range(len(train_in)):
	feature[i] = sum(k == -1 for k in train_in[i])/len(train_in[i])
	feature_sorted[ int ( train_out[i] ) ][ int ( count_arr[ int ( train_out[i] ) ] ) ] += feature[i]
	count_arr[ int ( train_out[i] ) ] += 1
for i in range (10 ):
	temp_arr = np.histogram ( feature_sorted[i][0:int ( count_arr[i] ) ], bins )
	for j in range ( len ( temp_arr[0] ) ):
		feature_binned[i][j] = temp_arr[0][j]

# Compute probablities.
for i in range (10 ):
	P_C[i] = count_arr[i] / len(train_in)
	for j in range ( len ( bins ) - 1 ):
		P_X_C[i][j] = feature_binned[i][j] / count_arr[i]
for j in range ( len ( bins ) - 1):
	for i in range (10 ):
		P_X[j] += ( P_X_C[i][j] * P_C[i] )
for i in range (10 ):
	for j in range ( len ( bins ) - 1 ):
		if P_X[j] == 0: P_C_X[i][j] = 0
		else: P_C_X[i][j] = P_X_C[i][j] * P_C[i] / P_X[j]

# To the test data set.
for i in range ( len(test_in) ):
	feature_test = sum(k == -1 for k in test_in[i])/len(test_in[i])

	# Find the corresponding bin by checking how many times it is possible to subtract the bin size from the current value.
	temp_value = feature_test; k = 0
	while temp_value > min_value: 
		temp_value -= bin_size
		k += 1

	# Find the largest probability for the bin.
	P = 0; digit = 10
	for l in range (10 ):
		if P_C_X[l][k-1] > P:
			P = P_C_X[l][k-1]; digit = l

	if test_out[i] == digit: correctly_classified += 1

sys.stdout.write("Correctly classified digits: {0}%".format(correctly_classified/float(len(test_in))*100))

for i in range (10 ):
	plt.xlim ( 0, 1 )
	plt.ylim ( 0, 200 )
	plt.hist ( feature_sorted[i][0:int ( count_arr[i] ) ], bins, label = "Digit {0} (#{2}), bin_size = {1}".format ( i, bin_size, int ( count_arr[i] ) ) )
	plt.legend ()
	if not os.path.exists(PATH+"plots/NN_ass_01_03_plots"): os.makedirs(PATH+"plots/NN_ass_01_03_plots") # Creates folder where plots will be stored.
	plt.savefig ( "plots/NN_ass_01_03_plots/digit_{0}_bin_size_{1}.png".format( i, bin_size ) )
	print ( "Figure saved as 'plots/NN_ass_01_03_plots/digit_{0}_bin_size_{1}.png'".format( i, bin_size ) )
	plt.close ()