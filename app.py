import pandas as pd
import numpy as np

def percentil(x):
    pc = df2[(df2['Puntaje'] <= x) ]['T']
    return pc


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


array = np.random.random(10)
#print(array) # [ 0.21069679 0.61290182 0.63425412 0.84635244 0.91599191 0.00213826 # 0.17104965 0.56874386 0.57319379 0.28719469]
value = 0.5
#print(find_nearest(array, value))



df1= pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSsfQ0qPqGYLRzWt6mtD4YZga_1Oi6gNV2bO3f1wuBLpXysOWvE0AUvaAih49RLqQHylL9chhkUk2zn/pub?output=csv')
df2 = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSa6Id3sW4bG8kBcy0pO2pDZBtQVNLtoAQYDb34XIwK2U0dqhtDQqFPHf5fNzxWWRvSbB7y10RtRmht/pub?output=csv')
#df1['Percentil']= df1['Puntaje'].apply(percentil)
opciones= list(df2.loc[:,'T'])
opciones_pc= list(df2.loc[:,'PC'])
condiciones= [df1['Puntaje']>=30, df1['Puntaje']>=25, df1['Puntaje']>=20, df1['Puntaje']>=0]
df1['Punt. T'] = np.select(condiciones, opciones)
df1['PC'] = np.select(condiciones, opciones_pc)
df1.to_pickle('pruebas.pkl')
def print_hi():
    #print(percentil(21))
    #print(find_nearest(df2['Puntaje'], 21))
    print(opciones)
    print(df1.head())  # Press Ctrl+F8 to toggle the breakpoint.
    print(df2.head())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()
