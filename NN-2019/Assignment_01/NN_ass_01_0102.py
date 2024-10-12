import numpy as np
import matplotlib.pyplot as plt
import random
import sys
from scipy.spatial import distance

# Paths and filenames.
DATA_PATH = "/vol/home/s1594443/Desktop/NN/Assignment_01/data/"
train_in_path = "train_in.csv"
train_out_path = "train_out.csv"
test_in_path = "test_in.csv"
test_out_path = "test_out.csv"

# Importing data.
train_in = np.genfromtxt(DATA_PATH+train_in_path,dtype='float',delimiter=',')
train_out = np.genfromtxt(DATA_PATH+train_out_path,dtype='float',delimiter=',')
test_in = np.genfromtxt(DATA_PATH+test_in_path,dtype='float',delimiter=',')
test_out = np.genfromtxt(DATA_PATH+test_out_path,dtype='float',delimiter=',')

# Functions
def dist_calc(vector1,vector2,calc_method='euclid'):
	# Computes distances between centers.
	if calc_method == 'euclid': return distance.euclidean(vector1,vector2)
	if calc_method == 'cosine': return distance.cosine(vector1,vector2)
	if calc_method == 'mahal': return distance.mahalanobis(vector1,vector2)

def center_calc(labels,vectors,method='euclid'):
	# Computes centers and distances.
	center = np.zeros((10,256))
	counter = np.zeros((10,1))
	dist_centers = np.zeros((10,10))

	for i in range(len(labels)):
		digit = int(labels[i])
		center[digit] = center[digit]+vectors[i]
		counter[digit] += 1
	for i in range(len(center)):
		center[i] /= counter[i]
	for i in range(dist_centers):
		for j in range(dist_centers[i]):
			dist_centers = dist_calc(center[i],center[j],method)
			
	return center,dist_centers

d_center,dist_centers = center_calc(train_out,train_in)


'''
train_in = train_in.reshape ( dim_1, dim_3, dim_3 ) # Reshape the 256 vector space into an image of 16 by 16 pixels.
test_in = test_in.reshape ( dim_4, dim_3, dim_3 )

d_center = np.zeros ( ( dim_5, dim_3, dim_3 ) ) # Cloud for each digit. Classifies all images for each digit.
d_radius = np.zeros ( dim_5 ) 
distance_centers = np.zeros ( ( dim_5, dim_5 ) )

d_counter_train = np.zeros ( dim_5 ) # Counts the amount each digit occurs. The sum of all elements equals 1707.
d_counter_test = np.zeros ( dim_4 )
d_distance_train = np.zeros ( ( dim_1, dim_5 ) ) # Distance from each image to each center.
d_distance_test = np.zeros ( ( dim_4, dim_5 ) )
confusion_matrix_train = np.zeros ( ( dim_5, dim_5 ) )
confusion_matrix_test = np.zeros ( ( dim_5, dim_5 ) )

# Compute center.
for i in range ( dim_1 ):
	digit = int ( train_out[i] )
	d_center[digit] = d_center[digit] + train_in[i]
	d_counter_train[digit] += 1
for i in range ( dim_5 ):
	d_center[i] = d_center[i] / d_counter_train[i]

# Compute radius for each digit d.
for k in range ( dim_1 ): # Loop over all 1707 images.
	digit = int ( train_out[k] )
	radius = 0
	for i in range ( dim_3 ): # Loop over width image.
		for j in range ( dim_3 ): # Loop over length image.
			radius += ( d_center[digit][i][j] - train_in[k][i][j] ) ** 2
	radius = radius ** 0.5 # Compute Euclidean image.
	if radius > d_radius[digit]: # If radius is larger than current value ...
		d_radius[digit] = radius # ... replace it.

# Compute distances for each element to each center.
for k in range ( dim_5 ):
	for l in range ( dim_5 ):
		for i in range ( dim_3 ):
			for j in range ( dim_3 ):
				distance_centers[k][l] += ( d_center[k][i][j] - d_center[l][i][j] ) ** 2
		distance_centers[k][l] = distance_centers[k][l] ** 0.5

# Computes distances and confusion-matrices.
def make_confusion_matrix ( data_in, data_out ):

	d_counter = np.zeros ( dim_5 )
	d_distance = np.zeros ( ( len ( data_in ), dim_5 ) )
	confusion_matrix = np.zeros ( ( dim_5, dim_5 ) )

	for i in range ( len ( data_in ) ):
		digit = int ( data_out[i] )
		d_counter[digit] += 1

	for k in range ( len ( data_in ) ):
		for l in range ( dim_5 ):
			d_distance[k] = paired_distances ( d_center[l], data_in[k], metric = 'euclidean' )
			
			distance = 0
			for i in range ( dim_3 ):
				for j in range ( dim_3 ):
					distance += ( d_center[l][i][j] - data_in[k][i][j] ) ** 2
			distance = distance ** 0.5
			d_distance[k][l] = distance

	for k in range ( len ( data_in ) ):
		digit = int ( data_out[k] )
		smallest = 1e10
		smallest_element = 10
		for l in range ( dim_5 ):
			if d_distance[k][l] < smallest:
				smallest = d_distance[k][l]
				smallest_element = l
		confusion_matrix[digit][smallest_element] += 1

	# Convert confusion_matrix_train to percentages.
	for i in range ( dim_5 ):
		for j in range ( dim_5 ):
			confusion_matrix[i][j] /= d_counter[i] / 100
			# Visualisation purposes.
			sys.stdout.write ( "{:03.1f}".format ( confusion_matrix[i][j] ) )
			if confusion_matrix[i][j] < 10: sys.stdout.write ( " " )
			if confusion_matrix[i][j] < 100: sys.stdout.write ( " " )
			sys.stdout.write ( "  " )
		print ( "" )
	print ( "" )
		
	return d_counter, d_distance, confusion_matrix

d_counter_train, d_distance_train, confusion_matrix_train = make_confusion_matrix ( train_in, train_out )
d_counter_test, d_distance_test, confusion_matrix_test = make_confusion_matrix ( test_in, test_out )








	

#for i in range ( dim_5 ):
#	plt.imshow ( d_center[i] )
#	plt.show ()


















