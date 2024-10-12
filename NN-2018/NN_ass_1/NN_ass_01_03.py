# Create the folder "ass_1_3_figures/" in the folder the code is located.

import numpy as np
import matplotlib.pyplot as plt

DATA_PATH = "/home/bruinsma/Desktop/NN/data/"
train_in_path = "train_in.csv"
train_out_path = "train_out.csv"
test_in_path = "test_in.csv"
test_out_path = "test_out.csv"

train_in = np.genfromtxt ( DATA_PATH + train_in_path, dtype = 'float', delimiter = ',' )
train_out = np.genfromtxt ( DATA_PATH + train_out_path, dtype = 'float', delimiter = ',' )
test_in = np.genfromtxt ( DATA_PATH + test_in_path, dtype = 'float', delimiter = ',' )
test_out = np.genfromtxt ( DATA_PATH + test_out_path, dtype = 'float', delimiter = ',' )

dim_1_train = len ( train_in ) # 1707. Number of digits in training data.
dim_1_test = len ( test_in ) # 1000. Number of digits in testing data.
dim_2 = len ( train_in[0] ) # 256. 256 dimensional space.
dim_3 = 10 # Number of possible digits.

# Bin data.
min_value = -600 # Minimum value. Large values to make sure all 1707 (and the 100 from the test set) digits are within the range of the bin array.
max_value = 600 # Maximum value.
bin_size = 0.1 # Width of a bin
bins = np.linspace ( min_value, max_value, ( 1 / bin_size ) * ( max_value - min_value ) + 1 ) # Bins.

# Feature data.
count_arr = np.zeros ( dim_3 ) # Array that displays the occurence of each digit.
feature = np.zeros ( dim_1_train ) # Values of our Bayesian classifier.
feature_sorted = np.zeros ( ( dim_3, dim_1_train ) ) # Contains a lot of empty spaces.
feature_binned = np.zeros ( ( dim_3, len ( bins ) - 1 ) )

# Results
correctly_classified = 0

# Probabilities.
P_C = np.zeros ( dim_3 )
P_X_C = np.zeros ( ( dim_3, len ( bins ) - 1 ) )
P_X = np.zeros ( len ( bins ) - 1 )
P_C_X = np.zeros ( ( dim_3, len ( bins ) - 1 ) )

# Compute features.
for i in range ( dim_1_train ):
	feature[i] = sum ( train_in[i][:dim_2 / 2] ) / sum ( train_in[i][dim_2 / 2:] ) # <--- Feature.
	feature_sorted[ int ( train_out[i] ) ][ int ( count_arr[ int ( train_out[i] ) ] ) ] += feature[i]
	count_arr[ int ( train_out[i] ) ] += 1
for i in range ( dim_3 ):
	temp_arr = np.histogram ( feature_sorted[i][0:int ( count_arr[i] ) ], bins )
	for j in range ( len ( temp_arr[0] ) ):
		feature_binned[i][j] = temp_arr[0][j]

# Compute probablities.
for i in range ( dim_3 ):
	P_C[i] = count_arr[i] / dim_1_train
	for j in range ( len ( bins ) - 1 ):
		P_X_C[i][j] = feature_binned[i][j] / count_arr[i]
for j in range ( len ( bins ) - 1):
	for i in range ( dim_3 ):
		P_X[j] += ( P_X_C[i][j] * P_C[i] )
for i in range ( dim_3 ):
	for j in range ( len ( bins ) - 1 ):
		if P_X[j] == 0: P_C_X[i][j] = 0
		else: P_C_X[i][j] = P_X_C[i][j] * P_C[i] / P_X[j]

# To the test data set.
for i in range ( dim_1_test ):
	# Find the feature values for the test set.
	feature_test = sum ( test_in[i][:dim_2 / 2] ) / sum ( test_in[i][dim_2 / 2:] )

	# Find the corresponding bin by checking how many it is possible to subtract the bin size from the current value.
	temp_value = feature_test; k = 0
	while temp_value > min_value: 
		temp_value -= bin_size
		k += 1

	# Find the largest probability for the bin.
	P = 0; digit = 10
	for l in range ( dim_3 ):
		if P_C_X[l][k-1] > P:
			P = P_C_X[l][k-1]; digit = l

	if test_out[i] == digit: correctly_classified += 1

print "Correctly classified digits:", correctly_classified / float ( dim_1_test ) * 100, "%"

for i in range ( dim_3 ):
	plt.xlim ( -1, 5 )
	plt.ylim ( 0, 170 )
	plt.hist ( feature_sorted[i][0:int ( count_arr[i] ) ], bins, label = "Digit {0} (#{2}), bin_size = {1}".format ( i, bin_size, int ( count_arr[i] ) ) )
	plt.legend ()
	plt.savefig ( "ass_1_3_figures/digit_{0}_bin_size_{1}.png".format( i, bin_size ) ) # Make this directory if it does not exist.
	print ( "Figure saved as 'ass_1_3_figures/digit_{0}_bin_size_{1}.png'".format( i, bin_size ) )
	plt.close ()