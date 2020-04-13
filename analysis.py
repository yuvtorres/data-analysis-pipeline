# Tools to elaborate the reports

#libraries
import numpy as np 
import pandas as pd

# Analysis by word:
# Receive the dataframe and a word. Return True if the word is present
# in the unique word and False in other cases. If the word is present in 
# the data base of unique words, the function creates a report in a cvs file 
# calls report.csv 

def analysis_word(df,word):
    df_uw=pd.read_csv('data/unique_words.csv')
    df_uws=df_uw.loc[df_uw['unique word']==word]

    Numbers_poems=len(df_uw)
    if Numbers_poems==0:
        return False
    
    Poets=[poet for poet in df_uws['id_Poem']]
    Numbers_poets=len(Poets)
    years_poet=df['year']
    years=[df['year'].loc[df['Poet']==poet] for poet in Poets]
    
    return True


# 
def analysis_year(df,year):
    df_uw=pd.read_csv('data/unique_words.csv')

    return True

def analysis_general(df,word):
    df_uw=pd.read_csv('data/unique_words.csv')

    return True


