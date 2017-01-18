import matplotlib as plt
import numpy as np
import pandas as pd

from scipy.stats import mode

from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import KFold
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics

def input():
	f = open("test.csv", "r")
	df = pd.read_csv(f)
	df.rename(columns={'Unnamed: 0': 'S_No'}, inplace=True)
	return df

def done():
	f.close()

def processing():
	df = input()
	# df = df.dropna(subset=['v_id'])
	print df.head()
	print "Shape of dataframe is " + str(df.shape)

processing()