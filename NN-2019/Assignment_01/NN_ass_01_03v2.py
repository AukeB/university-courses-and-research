import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
import os, sys, random

# Paths and filenames.
PATH = "/vol/home/s1594443/Desktop/NN/NN_ass_1/" # Change this to the directory where the code is located.
train_in_path = "data/train_in.csv" # Put all the .csv files in a folder called data.
train_out_path = "data/train_out.csv"
test_in_path = "data/test_in.csv"
test_out_path = "data/test_out.csv"

# Importing data.
train_in = np.genfromtxt(PATH+train_in_path,dtype='float',delimiter=',')
train_out = np.genfromtxt(PATH+train_out_path,dtype='float',delimiter=',')
test_in = np.genfromtxt(PATH+test_in_path,dtype='float',delimiter=',')
test_out = np.genfromtxt(PATH+test_out_path,dtype='float',delimiter=',')

def binner(min_value,max_value,bin_size): # Bins.
	return np.linspace(min_value,max_value,(1/bin_size)*(max_value-min_value)+1)

def featurer(data_in,label):
	count_arr = np.zeros(10) # Array that displays the occurence of each digit.
	feature = np.zeros(len(data_in)) # Values of our Bayesian classifier.
	feature_sorted = np.zeros((10,len(data_in))) # Same as feature array, but now sorted (Contains a lot of empty spaces).
	feature_binned = np.zeros((10,len(bins)-1)) # In binned format.

	for i in range(len(data_in)):
		feature[i] = sum(k < -0.99 for k in data_in[i])/float(len(data_in[i])) # <--- Feature (Amount of elements equal to -1).
		feature_sorted[int(label[i])][int(count_arr[int(label[i])])] += feature[i]
		count_arr[int(label[i])] += 1

	for i in range(10):
		temp_arr = np.histogram(feature_sorted[i][0:int(count_arr[i])],bins)
		for j in range(len(temp_arr[0])):
			feature_binned[i][j] = temp_arr[0][j]

	return count_arr,feature_sorted,feature_binned

def probabilitinator(number_array,bins,count_arr,feature_binned):
	P_C = np.zeros(len(number_array))
	P_X_C = np.zeros((len(number_array),len(bins)-1))
	P_X = np.zeros(len(bins)-1)
	P_C_X = np.zeros((len(number_array),len(bins)-1))
	total_counts = 0

	for i in range(len(number_array)):
		total_counts += count_arr[number_array[i]]

	for i in range(len(number_array)):
		P_C[i] = count_arr[number_array[i]]/total_counts
		for j in range(len(bins)-1):
			P_X_C[i][j] = feature_binned[number_array[i]][j]/count_arr[number_array[i]]

	for j in range(len(bins)-1):
		for i in range(len(number_array)):
			P_X[j] += (P_X_C[i][j]*P_C[i])

	for i in range(len(number_array)):
		for j in range(len(bins)-1):
			if P_X[j] == 0: P_C_X[i][j] = 0
			else: P_C_X[i][j] = P_X_C[i][j]*P_C[i]/P_X[j]

	return P_C_X

def tester(data_in,label,number_array,P_C_X):
	count_arr = np.zeros(10) # Array that displays the occurence of each digit.
	correctly_classified = 0
	false_classified = 0
	not_classified = 0
	total_counts = 0

	for i in range(len(data_in)):
		count_arr[int(label[i])] += 1

	for i in range(len(number_array)):
		total_counts += count_arr[number_array[i]]

	for i in range(len(data_in)):
		for j in range(len(number_array)):
			if label[i] == number_array[j]:
				feature = sum(k == -1 for k in data_in[i])/float(len(data_in[i])) # <--- Feature (Amount of elements equal to -1).

				# Find the corresponding bin by checking how many times it is possible to subtract the bin size from the current value.
				temp_value = feature
				k = 0

				while temp_value > min_value: 
					temp_value -= bin_size
					k += 1

				# Find the largest probability for the bin.
				P = 0; digit = 10

				for l in range(len(number_array)):
					if P_C_X[l][k] > P:
						P = P_C_X[l][k]
						digit = number_array[l]

				if label[i] == digit:
					correctly_classified += 1
				elif digit == 10:
					not_classified += 1
				else: 
					false_classified += 1

	return correctly_classified, false_classified

def plotter(correct,incorrect,feature_sorted,count_arr,number_array,single):
	if not os.path.exists(PATH+"plots/NN_ass_01_03_plots/bin_size={0}".format(bin_size)): os.makedirs(PATH+"plots/NN_ass_01_03_plots/bin_size={0}".format(bin_size)) # Creates folder where plots will be stored.
	if single == False:
		plt.xlim(0,1)
		plt.ylim(0,75)
		plt.title("{:03.1f}% Correctly classified.".format((correctly_classified/float(correctly_classified+false_classified)*100)))
		for i in range(len(number_array)):
			plt.hist(feature_sorted[number_array[i]][0:int(count_arr[number_array[i]])],bins,label="Digit {0} (#{2}), bin_size = {1}".format(number_array[i],bin_size,int(count_arr[number_array[i]])))
		plt.legend()
		plt.savefig("plots/NN_ass_01_03_plots/bin_size={1}/digit_{0}_bin_size_{1}.png".format(number_array,bin_size))
		print("Figure saved as 'plots/NN_ass_01_03_plots/bin_size={1}/digit_{0}_bin_size_{1}.png'".format(number_array,bin_size))
		plt.close()
	if single == True:
		for i in range(len(number_array)):
			plt.xlim(0,1)
			plt.ylim(0,75)
			plt.title("{:03.1f}% Correctly classified.".format((correctly_classified/float(correctly_classified+false_classified)*100)))
			plt.hist(feature_sorted[number_array[i]][0:int(count_arr[number_array[i]])],bins,label="Digit {0} (#{2}), bin_size = {1}".format(number_array[i],bin_size,int(count_arr[number_array[i]])))
			plt.legend()
			plt.savefig("plots/NN_ass_01_03_plots/bin_size={1}/digit_{0}_bin_size_{1}.png".format(number_array[i],bin_size))
			print("Figure saved as 'plots/NN_ass_01_03_plots/bin_size={1}/digit_{0}_bin_size_{1}.png'".format(number_array[i],bin_size))
			plt.close()

# Bin data.
min_value = 0 # Minimum value. Large values to make sure all 1707 (and the 1000 from the test set) digits are within the range of the bin array.
max_value = 1 # Maximum value.
bin_size = 0.05 # Width of a bin
bins = binner(min_value,max_value,bin_size)

# Feature data
count_arr_train,feature_sorted_train,feature_binned_train = featurer(train_in,train_out)
count_arr_test,feature_sorted_test,feature_binned_test = featurer(test_in,test_out)

# Single plots.
number_array = np.array([0,1,2,3,4,5,6,7,8,9]) # Numbers to investigate
P_C_X = probabilitinator(number_array,bins,count_arr_train,feature_binned_train) # Compute probability.
correctly_classified,false_classified = tester(test_in,test_out,number_array,P_C_X) # Test the probability distribution.
plotter(correctly_classified,false_classified,feature_sorted_test,count_arr_test,number_array,single=True) # Plot histograms

# Double plots
confusion_matrix = np.zeros((10,10))
for i in range(10):
	for j in range(10):
		if i != j:
			number_array = np.array([i,j]) 
			P_C_X = probabilitinator(number_array,bins,count_arr_train,feature_binned_train)
			correctly_classified,false_classified = tester(test_in,test_out,number_array,P_C_X)
			plotter(correctly_classified,false_classified,feature_sorted_test,count_arr_test,number_array,single = False)
			confusion_matrix[i][j] = (correctly_classified)*100/float((correctly_classified+false_classified))
				
plt.imshow(confusion_matrix,interpolation='nearest')
plt.set_cmap('cool')
plt.title("Confusion matrix, bin size = {0}".format(bin_size))
plt.xlabel("digits")
plt.ylabel("digits")
for i in range(len(confusion_matrix)):
	for j in range(len(confusion_matrix[i])): 
		plt.text(i,j,"{0:0.1f}".format(confusion_matrix[i][j]),ha="center",va="center",color="k")
plt.colorbar()
plt.savefig("plots/NN_ass_01_03_plots/bin_size={0}/confusion_matrix_bin_size_{0}.png".format(bin_size))
sys.stdout.write("Figure saved as plots/NN_ass_01_03_plots/bin_size={0}/confusion_matrix_bin_size_{0}.png\n".format(bin_size))
plt.close()