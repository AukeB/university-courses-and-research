import numpy as np
import matplotlib.pyplot as plt
import random
import sys

DATA_PATH = '/vol/home/s1594443/Desktop/NN/Assignment_01/data/'
train_in_path = "train_in.csv"
train_out_path = "train_out.csv"
test_in_path = "test_in.csv"
test_out_path = "test_out.csv"

train_in = np.genfromtxt ( DATA_PATH + train_in_path, dtype = 'float', delimiter = ',' )
train_out = np.genfromtxt ( DATA_PATH + train_out_path, dtype = 'float', delimiter = ',' )
test_in = np.genfromtxt ( DATA_PATH + test_in_path, dtype = 'float', delimiter = ',' )
test_out = np.genfromtxt ( DATA_PATH + test_out_path, dtype = 'float', delimiter = ',' )

def activation_f(x):
#Uses a sigmoid function to calculate activation
	return 1./(1.+np.exp(-x)) 
#end activation_f

def xor_labeler(x):
#XOR function used to label data
	labels = np.zeros(len(x))
	for i in range(len(x)):
		if bool(x[i][0])^bool(x[i][1]):
			labels += 1
	return labels
#end xor_labeler

def xor_net(x1,x2,weights):
	bias = 1
	hidden = []	
	# Node 3
	hidden.append(activation_f(x1*weights[0]+x2*weights[1]+bias*weights[2]))
	hidden.append(activation_f(x1*weights[3]+x2*weights[4]+bias*weights[5]))
	output = activation_f(hidden[0]*weights[6]+hidden[1]*weights[7]+bias*weights[8])
	return output
#end xor_net

def mse(weights):
#Calculates mean square error for given weights
	in4 = [[0,0],[0,1],[1,0],[1,1]]
	target = np.array([0,1,1,0])	
	output = []
	for i in range(4):
		output.append(xor_net(in4[i][0],in4[i][1],weights))
	return np.sum((np.asarray(output)-target)**2) /4	
#end mse

#N = 100
#rand_in = np.random.randint(2,size=(N,2))
#labels = xor_labeler(rand_in)

#output = []
#for i in range(4):
#	output.append(xor_net(in4[i][0],in4[i][1],weights))
#print output

weights = np.random.rand(9)
print mse(weights)




		

	 
	

