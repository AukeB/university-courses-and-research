import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from scipy.spatial import distance
import itertools
from sklearn import svm, datasets

DATA_PATH = '/vol/home/s1587064/Documents/Neural_Networks/data/'
tr_dat_in = 'train_in.csv'
tr_dat_out = 'train_out.csv'
tst_dat_in = 'test_in.csv'
tst_dat_out = 'test_out.csv'

train_in = np.genfromtxt(DATA_PATH+tr_dat_in,dtype='float',delimiter=',')
train_out = np.genfromtxt(DATA_PATH+tr_dat_out,dtype='float',delimiter=',')
test_in = np.genfromtxt(DATA_PATH+tst_dat_in,dtype='float',delimiter=',')
test_out = np.genfromtxt(DATA_PATH+tst_dat_out,dtype='float',delimiter=',')

def perceptron(in_data,weights,n):
# Perceptron function that returns an output vector 
# in_data = 256 dimensional vector
# weights = 257x10 matrix 
# n = number of outputs (10)
# output  = 10 dimensional vector
	
	output = np.zeros((len(in_data),n)) #output 	
	in_data = np.append(in_data,np.zeros((len(in_data),1))) #adding bias
	for i in range(len(in_data)):
		output[i] = np.dot(in_data,weights) 
	return output

	



#end perceptron

#def weights_training(labels,weights,predictions):
#	for i in range(len(labels)): 





weights = np.random.rand(10,257)# initialise weights
in_data = train_in 

print perceptron(in_data,weights,10)
	
