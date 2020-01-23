import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import csv

input_filename = '../data/data64_4500_4_30.csv'
output_dir = '../data/train80_test20'
train_filename = output_dir + '/train.csv'
test_filename = output_dir + '/test.csv'

data = pd.read_csv(input_filename)
train, test = train_test_split(data, test_size=0.2)
train.to_csv(train_filename, index=False, header=False)
test.to_csv(test_filename, index=False, header=False)