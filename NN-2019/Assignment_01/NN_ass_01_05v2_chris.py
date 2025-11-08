import numpy as np
import matplotlib.pyplot as plt
import random
import sys

#DATA_PATH = 'C:/Users/Christiaan/Desktop/NN/data/'
'''
train_in_path = "train_in.csv"
train_out_path = "train_out.csv"
test_in_path = "test_in.csv"
test_out_path = "test_out.csv"

train_in = np.genfromtxt ( DATA_PATH + train_in_path, dtype = 'float', delimiter = ',' )
train_out = np.genfromtxt ( DATA_PATH + train_out_path, dtype = 'float', delimiter = ',' )
test_in = np.genfromtxt ( DATA_PATH + test_in_path, dtype = 'float', delimiter = ',' )
test_out = np.genfromtxt ( DATA_PATH + test_out_path, dtype = 'float', delimiter = ',' )
'''
def activation_f(x,f='sigmoid'):
#Uses a sigmoid function to calculate activation
	if f = 'sigmoid':
		return 1./(1.+np.exp(-x))
	if f = 'relu':
		if x == 0:		
			return 0
		else 
			return x
	if f = 'tanh':
		return np.tanh(x)
	if f = 'arctan':
		return np.arctan(x)
  
#end activation_f

def xor_net(x1,x2,weights,train=True,f='sigmoid'):
	bias = 1
	hidden = []	
	# Node 3
	hidden.append(activation_f(x1*weights[0]+x2*weights[1]+bias*weights[2],f))
	hidden.append(activation_f(x1*weights[3]+x2*weights[4]+bias*weights[5],f))
	output = activation_f(hidden[0]*weights[6]+hidden[1]*weights[7]+bias*weights[8],f)
	if train: 	
		return output
	elif output > 0.5:
		return 1
	else:
		return 0
#end xor_net

def mse(weights,f='sigmoid'):
#Calculates mean square error for given weights
	in4 = [[0,0],[0,1],[1,0],[1,1]]
	target = np.array([0,1,1,0])	
	output = []
	correct = 0
	for i in range(4):
		output.append(xor_net(in4[i][0],in4[i][1],weights,f))
		if target[i] == 1 and output[i] >= 0.5:
			correct += 1
		elif target[0] == 0 and output[i] < 0.5:
			correct += 1
	return np.sum((np.asarray(output)-target)**2) /4,correct	
#end mse

def grdmse_calc(weights,f='sigmoid'): 
#Calculates the gradient of the error function for the given weights
	epsylon = 1.e-3	
	grdmse = np.zeros(len(weights))
	for i in range(len(weights)):
		e_weights = np.array(weights)
		e_weights[i] = e_weights[i]+epsylon
		grdmse[i] = (mse(e_weights,f)[0]-mse(weights,f)[0])/epsylon
	return grdmse
#end grdmse

def train(weights,n,f='sigmoid'):
#Rocky Balboa 
	iteration = 0 
	grdmse = np.ndarray((1,9))
	er_it = []
	while(mse(weights,f)[0]>0.001) and iteration < 8000:
		iteration += 1		
		er,accuracy = mse(weights,f)
		sys.stdout.write ( "Iterations {0} ".format(iteration))
		sys.stdout.write ( "Accuracy {0}/4 ".format(accuracy))
		sys.stdout.write ( "Mse {0}\r".format(er)); sys.stdout.flush()
		grdmse = grdmse_calc(weights,f)
		weights = weights - n*grdmse
		er_it.append((er,iteration))		
		
	sys.stdout.write ( "\nTraining complete. \n".format(iteration, n))

	return weights,np.array(er_it)
#end train

weights = np.random.rand(9)

# Testing different step values
'''
trained_weights,er_it4 = train(weights,4)
trained_weights,er_it64 = train(weights,64)
trained_weights,er_it32 = train(weights,32)
trained_weights,er_it16 = train(weights,16)
trained_weights,er_it8 = train(weights,8)
trained_weights,er_it2 = train(weights,2)
trained_weights,er_it1 = train(weights,1)
trained_weights,er_it05 = train(weights,0.5)


plt.title('Mean squared error as a function of iterations for different $\eta$ values',fontsize = 16)
plt.xlabel('Iterations (log-scale)',fontsize = 16)
plt.ylabel('MSE',fontsize = 16)
plt.plot(a5.er_it32[:,1],a5.er_it32[:,0], label = '$\eta$ = 32')
plt.plot(a5.er_it16[:,1],a5.er_it16[:,0], label = '$\eta$ = 16')
plt.plot(a5.er_it8[:,1],a5.er_it8[:,0], label = '$\eta$ = 8')
plt.plot(a5.er_it4[:,1],a5.er_it4[:,0], label = '$\eta$ = 4')
plt.plot(a5.er_it2[:,1],a5.er_it2[:,0], label = '$\eta$ = 2')
plt.plot(a5.er_it1[:,1],a5.er_it1[:,0], label = '$\eta$ = 1')
plt.plot(a5.er_it05[:,1],a5.er_it05[:,0], label = '$\eta$ = 0.5')
plt.xscale('log')
plt.legend()
plt.tight_layout()
plt.show()
''' 
# Testing different initialisation methods
'''
weights = np.random.rand(9)
#weights = np.random.randint(2,size=(9))
#weights = np.random.randint(9,size=(9))
trained_weights,er_it_rand = train(weights,4)
trained_weights,er_it_zeros = train(np.zeros(9),4)
trained_weights,er_it_ones = train(np.ones(9),4)
trained_weights,er_it_half = train(np.array([0.5]*9),4)


plt.title('Mean squared error as a function of iterations for different weight initialisations',fontsize = 14)
plt.xlabel('Iterations (log-scale)',fontsize = 14)
plt.ylabel('MSE',fontsize = 14)
plt.plot(er_it_rand[:,1],er_it_rand[:,0], label = 'Random (between -1 and 1)')
plt.plot(er_it_zeros[:,1],er_it_zeros[:,0], label = 'All 0')
plt.plot(er_it_ones[:,1],er_it_ones[:,0], label = 'All 1')
plt.plot(er_it_half[:,1],er_it_half[:,0], label = 'All 0.5')
plt.legend()
plt.xscale('log')
plt.tight_layout()
plt.show()
'''
# Testing different activation functions
weights = np.random.rand(9)
	

