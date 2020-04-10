# funciones para importar las datos

import pandas as pd
import numpy as np

def import_data_poetry(path):
    df=pd.read_csv(path)
    print(f"Data imported from -->  ""{path}""")
    print(f"{len(df)} lines was imported")
    columnas_str='\n'.join((list(df.columns)))
    print(f'The columns are:\n{columnas_str}')
    df=df.drop(['Unnamed: 0'],axis=1)
    print(f"The column 'Unnamed: 0' was dropped.")
    df['count_l']=df['Poem'].apply(lambda x:len(x.split('\n')))
    print('the column count_l (numbers of line by poem) was creatted, description:')
    print(df['count_l'].describe())
    df['count_w']=df['Poem'].apply(lambda x:len(x.replace('\n',' ').split(' ')))
    print('the column count_w (numbers of words by poem) was creatted, description:')
    print(df['count_w'].describe())
    df['count_wu']=df['Poem'].apply(lambda x:len(set(x.replace('\n',' ').split(' '))))
    print('the column count_wu (numbers of words (non repeted) by poem) was creatted, description:')
    print(df['count_wu'].describe())
            




