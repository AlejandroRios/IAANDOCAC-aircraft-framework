import pandas as pd
import numpy as np


DOC_ik = np.load('my_file.npy',allow_pickle=True)
# DOC_ik = DOC_ik.to_dict()
# print(DOC_ik)

departure_airport =  ['CD1','CD2','CD3','CD4','CD5','CD6','CD7','CD8','CD9','CD10']
first_stop_airport =  ['CD1','CD2','CD3','CD4','CD5','CD6','CD7','CD8','CD9','CD10']

doc = DOC_ik.item()
print(type(doc))
# doc = {}
# for i in range(len(departure_airport)):
#     for k in range(len(first_stop_airport)):
#         doc = DOC_ik
#         print(DOC_ik)
# print(DOC_ik)

# for i in departure_airport:
#     for k in first_stop_airport:
#         print(DOC_ik[i][k])