import matplotlib as plt
import numpy as np
import pandas as pd

from scipy.stats import mode

from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import KFold
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics

def inp():
	f = open("test.csv", "r")
	df = pd.read_csv(f)
	df.rename(columns={'Unnamed: 0': 'S_No'}, inplace=True)
	return df

def done():
	f.close()

def processing():
	df = inp()
	print df.columns.values

	privacyOptions = ['public', 'private', 'unlisted', 'localized']
	df.privacyStatus = df.privacyStatus.replace(to_replace=df.privacyStatus[~df.privacyStatus.isin(privacyOptions)], value='public')

	# for categorical variables
	privacy_map_dict = {'public':3, 'localized':2, 'unlisted':1, 'private':0}
	df.privacyStatus = df.privacyStatus.map(privacy_map_dict)

	def_map_dict = {'public':2, 'sd':1, 'defaultAudioLanguage':0}
	df.definition = df.definition.map(def_map_dict)

	print pd.unique(df.categoryId.ravel())

	df['regionRestriction'].fillna(0, inplace=True)
	# use number of regions as a measure
	# for index, row in df.iterrows():
		# if row['regionRestriction'] != 0:
			# print row['regionRestriction']

	# print pd.unique(df.defaultAudioLanguage.ravel())
	# print pd.unique(df.definition.ravel())
	# print pd.unique(df.projection.ravel())
	# print pd.unique(df.liveBroadcastContent.ravel())
	# print "Check need for imputation"
	# print df.apply(lambda x: sum(x.isnull()),axis=0)

processing()