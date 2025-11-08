# Imports
import numpy as np
import pandas as pd

import lofar_surveys

df = pd.read_csv('ra_decs.txt',sep=', ',engine='python')

Field_name = np.array(df['Field_name'],dtype=str)
RA = np.array(df['RA'],dtype=float)
DEC = np.array(df['DEC'],dtype=float)

for i in range(30,40):
	lofar_surveys.cutout_pipeline(Field_name[i],RA[i],DEC[i])
	print('\n')
