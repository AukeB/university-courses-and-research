import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from scipy.spatial import distance
import itertools

# Setting paths and file names:
#DATA_PATH = '/vol/home/s1587064/Documents/Neural_Networks/data/'
DATA_PATH = 'C:/Users/Christiaan/Desktop/NN/data/'
tr_dat_in = 'train_in.csv'
tr_dat_out = 'train_out.csv'
tst_dat_in = 'test_in.csv'
tst_dat_out = 'test_out.csv'

# Importing the data:
train_in = np.genfromtxt(DATA_PATH+tr_dat_in,dtype='float',delimiter=',')
train_out = np.genfromtxt(DATA_PATH+tr_dat_out,dtype='float',delimiter=',')
test_in = np.genfromtxt(DATA_PATH+tst_dat_in,dtype='float',delimiter=',')
test_out = np.genfromtxt(DATA_PATH+tst_dat_out,dtype='float',delimiter=',')

# FUNCTIONS:

def dist_calc(vector1,vector2,method='euclid'):
# Returns distance between two vectors using specified calculation method
	if method == 'euclid':			
		return distance.euclidean(vector1,vector2)
	if method == 'cosine':			
		return distance.cosine(vector1,vector2)
	if method == 'mahal':			
		return distance.mahalanobis(vector1,vector2)	
#end dist_calc

def center_calc(labels,vectors,method='euclid'):
# Calculates the centers for given labels and vectors and gives distance between them
	center = np.zeros((10,256))
	counter = np.zeros((10,1))
	dist_centers = np.zeros((10,10))	
	for i in range(len(labels)): 
		digit = int(labels[i])
		center[digit] = center[digit]+vectors[i]
		counter[digit] += 1 
	for i in range(len(center)):
		center[i] = center[i]/counter[i]
	for i in range(10):
		for j in range(10):
			dist_centers[i][j] = dist_calc(center[i],center[j],method)
	return center,dist_centers
#end center_calc

def radius_calc(labels,vectors,center,method='euclid'):	
# Calculates the radius for given labels, vectors and center 
	radius = np.zeros((10,1))
	for i in range(len(labels)):
		digit = int(labels[i])
		if dist_calc(center[digit],vectors[i],method) > radius[digit]:
			radius[digit] = dist_calc(center[digit],vectors[i],method)
	return radius
#end radius_calc	

def dist_classifier(input_d,d_center,method='euclid'):
# Distance based classifier, accepts input_d and d_center and returns output_d
	output_d = np.zeros((len(input_d),1))
	for i in range(len(input_d)):
		min_d = 1e9		
		for j in range(len(d_center)):			
			dist = dist_calc(input_d[i],d_center[j],method)
			if dist < min_d:
				min_d = dist
				output_d[i] = j
	return output_d
#end dist_classifier

def checker(output,labels):
# Checks the given labels to the actual labels
	check = np.zeros((len(output),1))
	for i in range(len(output)):
		if output[i] == labels[i]:
			check[i] += 1 
	percent = (sum(check)/len(check))*100
	print 'The given data was classified with a {}% accuracy.'.format(percent[0])	
	return percent
#end checker
	
def confusion_matrix_gen(pred,truth):
# Creates a confusion matrix (can also be done using sklearn)
	matrix = np.zeros((10,10))
	count = np.zeros((10,1))
	for i in range(len(pred)):
		matrix[int(truth[i]),int(pred[i])] += 1	
		count[truth[i]] += 1
	for i in range(len(matrix)):
		matrix[i] = (matrix[i]/count[i])*100
	return np.around(matrix,2)
#end confusion_matrix_gen


def plot_confusion_matrix(cm,title='Confusion matrix',cmap=plt.cm.Blues):
# Function that plots a confusion matrix (modified version of function available in the scikit-learn documentation)
	plt.figure()    
	plt.imshow(cm, interpolation='nearest', cmap=cmap)
	plt.title(title)
	plt.colorbar()
	tick_marks = np.arange(0,10)
	plt.xticks(tick_marks, rotation=45)
	plt.yticks(tick_marks)

	fmt = 'd'
	thresh = cm.max() / 2.
	for i,j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
		plt.text(j,i,format(cm[i,j]),
		         horizontalalignment="center",
		         color="white" if cm[i, j] > thresh else "black")
	plt.ylabel('True label')
	plt.xlabel('Predicted label')
	plt.tight_layout()
	plt.show()
#end plot_confusion_matrix


# COMMANDS
'''
#Calculate the center, distance between centers and the radius of the given data-set
d_center,dist_centers = center_calc(train_out,train_in)
d_radius = radius_calc(train_out,train_in,d_center)
plot_confusion_matrix(np.around(dist_centers,2), title='Distances between centers')

#Use the distance classifier to predict the labels on the training and testing data and give the resulting accuracies
dc_output_train = dist_classifier(train_in,d_center)
dc_output_test = dist_classifier(test_in,d_center)
#Overal accuracy
dc_accur_train = checker(dc_output_train,train_out)
dc_accur_test = checker(dc_output_test,test_out)
#Plotting and calculating confusion matrices
matrix_train = confusion_matrix_gen(dc_output_train,train_out)
matrix_test = confusion_matrix_gen(dc_output_test,test_out)
plot_confusion_matrix(matrix_train, title='Confusion matrix - Distance based classifier (train)')
plot_confusion_matrix(matrix_test, title='Confusion matrix - Distance based classifier (test)')
'''

#Make the classifications using different distance calculation methods
#--------------COSINE-------------------------------------------------
d_center,dist_centers = center_calc(train_out,train_in, method ='cosine') 
dc_output_train_cos = dist_classifier(train_in,d_center,method ='cosine')
dc_output_test_cos = dist_classifier(test_in,d_center,method ='cosine')
#Overal accuracy
dc_accur_train = checker(dc_output_train,train_out)
dc_accur_test = checker(dc_output_test,test_out)
#Plotting and calculating confusion matrices
matrix_train = confusion_matrix_gen(dc_output_train,train_out)
matrix_test = confusion_matrix_gen(dc_output_test,test_out)
plot_confusion_matrix(matrix_train, title='Confusion matrix - Distance based (cosine) classifier (train)')
plot_confusion_matrix(matrix_test, title='Confusion matrix - Distance based (cosine) classifier (test)')
'''
#Make the classifications using different distance calculation methods
#--------------MINKOWSKI	------------------------------------------------- 
d_center,dist_centers = center_calc(train_out,train_in,'minkowski') 
dc_output_train = dist_classifier(train_in,d_center,'minkowski')
dc_output_test = dist_classifier(test_in,d_center,'minkowski')
#Overal accuracy
dc_accur_train = checker(dc_output_train,train_out)
dc_accur_test = checker(dc_output_test,test_out)
#Plotting and calculating confusion matrices
matrix_train = confusion_matrix_gen(dc_output_train,train_out)
matrix_test = confusion_matrix_gen(dc_output_test,test_out)
plot_confusion_matrix(matrix_train, title='Confusion matrix - Distance based (Minkowski) classifier (train)')
plot_confusion_matrix(matrix_test, title='Confusion matrix - Distance based (Minkowski) classifier (test)')
'''
