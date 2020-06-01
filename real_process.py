import numpy as np
import pandas as pd
import csv
from tqdm import tqdm

input_file = '../data/test.csv'
data = pd.read_csv(input_file)
print("read file")

val=250
data_proc = pd.DataFrame()
for index, row in tqdm(data.iterrows(), total=data.shape[0]):
	if len(str(row[1])) == val:
		data_proc = data_proc.append(row)
	elif len(str(row[1])) > val:
		#print(data.loc[index])
		#print(row[1][0:val])t
		newrow = {row[0], row[1][0:val]}
			#print(newrow)
		data_proc = data_proc.append(pd.DataFrame(newrow), ignore_index=True)
data.to_csv('realdata250.csv');
