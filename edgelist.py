import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame as df
import seaborn as sb
import csv
import networkx as nx
import matplotlib.pyplot as plt

dataset = pd.read_csv('corr_res_sp.csv') 
print(dataset.head())


#edge_list_df = pd.read_csv('corr_res_sp.csv')
#g =  nx.pandas_edgelist(edge_list_df,source='source') #,target='target',edge_attr='weight')
#print(g)

#df.stack().reset_index()
#Source = dataset
def edgelist(df):
    a = df.values
    c = df.columns
    n = len(c)
    
    c_ar = np.array(c)
    out = np.empty((n, n, 2), dtype=c_ar.dtype)
    
    out[...,0] = c_ar[:,None]
    out[...,1] = c_ar
    
    mask = ~np.eye(n,dtype=bool)
    df_out = pd.DataFrame(out[mask], columns=[['Source','Target']])
    df_out['Weight'] = a[mask]
    print(df_out() )
