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


count_4 = np.count_nonzero(test_out == 4)
count_7 = np.count_nonzero(test_out == 7)
PC4 = count_4/float((count_4+count_7))
PC7 = count_7/float((count_4+count_7))

print PC4, PC7

train_X = np.zeros(len(train_in))

for i in range(len(train_in)):
	train_X[i] = sum(train_in[i][:128])/sum(train_in[i][128:])

#plt.scatter(train_out,train_X)
#plt.show()

train_X4 = []
train_X7 = []

for i in range(len(train_out)):
	if train_out[i] == 4:
		train_X4.append(train_X[i])
	elif train_out[i] == 7:
		train_X7.append(train_X[i])	

bins = np.linspace(0,4,21)
train_X4_bin = np.histogram(train_X4,bins)
train_X7_bin = np.histogram(train_X7,bins)

plt.hist(train_X4,bins)
plt.hist(train_X7,bins)
plt.show()

PXC4 = []
PXC7 = []

for i in range(len(train_X4_bin[0])):
	PXC4.append(train_X4_bin[0][i]/float(count_4))
	PXC7.append(train_X7_bin[0][i]/float(count_7))

PCX4 = PXC4*PC4
PCX7 = PXC7*PC7

print PCX4
print PCX7

# Task 3: Implement a Bayes rule classidier - we will be clasifying images as 5 or 7 
# What feature do we want to use to discriminate between the classes? 
# Feature that we want to use: X = height/width not very useful due to all digits being of similar dimention. Hence we decide to use X = #of filled pixels in top half / # of filled pixels in bottom half

# Implement the feature, apply it to the training data, discretize is and create corresponding histograms.
# Calculate the terms P(X|C) and P(C) so that you can apply the Bayes rule to find P(C|X) over the training set. 

