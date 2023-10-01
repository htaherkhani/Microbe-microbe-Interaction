mport numpy as np
import pandas as pd
from scipy import stats
from pandas.core.frame import DataFrame
import seaborn as sb
import csv
dataset = pd.read_csv('sample3.csv')
stest=stats.shapiro(dataset)
print(stest)
