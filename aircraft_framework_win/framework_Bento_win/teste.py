import pandas as pd
import numpy as np


df = pd.read_table('PQ1.dat' ,header=None,skiprows=[0],sep=',')

print(df.head())

df2 = pd.read_csv('PQ1.dat' ,sep='\s+', delimiter=None, header=None,skiprows=[0])

# df2 = df2.reset_index(drop=False)
# pandas.read_csv(filepath_or_buffer, sep=', ', delimiter=None, header='infer', names=None, index_col=None, ....)

print(df2.head())

print(df2.shape)
