import matplotlib as mpl
import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import KFold
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics

f = open("data.csv", "r")
df = pd.read_csv(f)
print df.shape
f.close()