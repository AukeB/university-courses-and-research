import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Import data
test_results_cols=['source_name0','score1','component1','peak1','score2','component2','peak2','score3','component3','peak3','score4','component4','peak4']
test_results = pd.read_csv('data/test_results.txt',sep=',',names=test_results_cols,skiprows=1)
labels = pd.read_csv('data/curatedcurated_list_labeled.csv',header=0)

# Counts different amount of sources in curatedcurated_list_labeld.csv.
def count_dif_amount_orig_sources(column):
	count_array = []
	count_array.append(0)
	for i in range(1,len(column)):
		count_array[-1] += 1
		if column[i] != column[i-1]:
			count_array.append(0)
	count_array[-1] += 1
	return count_array

# Counts the amount of sources recognized in test_results.txt
def count_test_results_column(test_results):
	test_results_sources = np.zeros(360)
	for i in range(len(test_results)):
		if np.isnan(test_results.iloc[i]['score1']) == True:
			test_results_sources[i] = 1
		elif np.isnan(test_results.iloc[i]['score2']) == True:
			test_results_sources[i] = 2
		elif np.isnan(test_results.iloc[i]['score3']) == True:
			test_results_sources[i] = 3
		elif np.isnan(test_results.iloc[i]['score4']) == True:
			test_results_sources[i] = 4
		else:
			test_results_sources[i] = 5
	return test_results_sources

dif_sources = count_dif_amount_orig_sources(labels['Orig_Source_Name'])
test_sources = count_test_results_column(test_results)

def compare(x,y):
	counter = 0
	counter_2 = 0
	counter_3 = 0
	for i in range(len(x)):
		if y[i] > x[i]:
			counter_2 += 1
		if x[i] == int(y[i]):
			counter += 1
		if x[i] > y[i]:
			counter_3 += 1
	percentage = counter/float(len(x))*100
	percentage_2 = counter_2/float(len(x))*100
	percentage_3 = counter_3/float(len(x))*100
	return percentage,percentage_2,percentage_3

percentage_correct,false_positives,false_negatives = compare(dif_sources,test_sources)
print('Total number of sources from catalogue  {0}'.format(sum(dif_sources)))
print('Total number of sources recognized      {0}'.format(int(sum(test_sources))))
print('Percentage sources recognized:          {0}%'.format(100*sum(test_sources)/sum(dif_sources)))
print('Percentage correct:                     {0}%'.format(percentage_correct))
print('False positives:                        {0}%'.format(false_positives)) 
print('False negatives:                        {0}%'.format(false_negatives)) 
