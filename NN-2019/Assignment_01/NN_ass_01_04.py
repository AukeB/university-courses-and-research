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

# Functions.
def train_perceptron(data_in,labels,weights): # Changes weights.
	iteration = 0 # Counts the amount of iterations done before 100% correct classification is reached.
	output_indices = np.zeros((len(data_in),1)) # Initializing array.
	weighted_sum = np.zeros((len(data_in),len(weights[0]))) # Initializing array.

	while np.array_equal(output_indices,labels) == False: # While there are still incorrectly classified digits ...
		false_classified_indices = [] # Array that will contain all indices of wrong
		iteration += 1 # Counts the number of iterations needed to reach 100%.

		for i in range(len(data_in)):
			if output_indices[i] != labels[i]:
				false_classified_indices.append(i)

		percentage_correct = (len(data_in)-len(false_classified_indices))*100/float(len(data_in))

		plt.plot(iteration,percentage_correct,'.')
		sys.stdout.write("{:03.1f}% ".format(percentage_correct))
		sys.stdout.write ( " {0}\r".format(iteration)); sys.stdout.flush ()

		k = false_classified_indices[random.randint(0,len(false_classified_indices)-1)] # Choose a random element that is incorrectly classified.

		for j in range(len(weights[0])): # The algorithm that changes the weights.
			if weighted_sum[k][j] > weighted_sum[k][int(labels[k])]:
				weights[:,j] -= data_in[k] # Changing of the weights.
			if j == int ( labels[k] ):
				weights[:,j] += data_in[k] # Changing of the weights.

		weighted_sum = np.dot(data_in,weights)
		output_indices = np.argmax(weighted_sum,axis=1)

	plt.xlabel("Number of iterations ({0} total).".format(iteration))
	plt.ylabel("Percentage correctly classified digits.")
	if not os.path.exists(PATH+"plots/NN_ass_01_04_plots"): os.makedirs(PATH+"plots/NN_ass_01_04_plots") # Creates folder where plots will be stored.
	plt.savefig("plots/NN_ass_01_04_plots/NN_ass_01_04_iter={0}.png".format(iteration))
	plt.close()
	sys.stdout.write("Figure saved as plots/NN_ass_01_04_plots/NN_ass_01_04_iter={0}.png\n".format(iteration))
	sys.stdout.write ( "Iterations: {0}\n".format ( iteration ) )

	return weights, iteration

def test_perceptron ( data_in, labels, weights ): # Test new weights values for a certain dataset.
	weighted_sum = np.dot ( data_in, weights ) # Definition
	output_indices = np.argmax ( weighted_sum, axis = 1 ) # Get the index with highest value.

	correct_counter = 0 # Amount of correctly classified digits.

	for i in range(len(data_in)):
		if output_indices[i] == labels[i]:
			correct_counter += 1

	sys.stdout.write ( "Accuracy:   {:03.1f}%\n".format(correct_counter*100/len(labels)))

def perceptron(data_in,labels,weights,train):
	bias = np.ones((len(data_in),1)) # Create bias array filled with ones.
	data_in = np.append(data_in,bias,axis=1) # Merge data_in and bias.
	if train == True: return train_perceptron(data_in,labels,weights) # Training program.
	if train == False: test_perceptron(data_in,labels,weights) # Testing program.

def main(n): # n = Number of times you want to run the program.
	iter_dist=[]
	for i in range(n):
		sys.stdout.write ( "Run {0}\n".format ( i + 1 ) )
		weights = np.random.rand(257,10) # Initialise weights array.randomly.
		weights, iteration = perceptron(train_in,train_out,weights,train=True) # Train the weights.
		iter_dist.append(iteration)
		perceptron(train_in,train_out,weights,train=False) # Test weights on train_data (should be 100%).
		perceptron(test_in,test_out,weights,train=False) # Test weights on test_data.
		sys.stdout.write ("\n")

main(4)