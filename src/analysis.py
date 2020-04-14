# Tools to elaborate the analysis

#libraries
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

# Analysis unique word:
# Receive the dataframe and a word. Return True if the word is present
# in the unique word and False in other cases. If the word is present in 
# the data base of unique words, the function creates a report in a cvs file 
# calls report.csv 

def analysis_unique_word(df,word):

    df_uw = pd.read_csv('data/unique_words.csv')
    df_uws = df_uw.loc[df_uw['unique word']==word]
    df_uws.rename(columns={'id_Poem':'idPoem'}, inplace=True)
    df_uws_w=df_uws.groupby(['idPoem']).count()

    Numbers_poems = len(df_uws_w)

    if Numbers_poems==0:
        return False

    f=open("output/report.csv","w")
    f.write(f"The word {word} appear as unique word in {Numbers_poems} Poems")
    
    df=df.reset_index().set_index(['idPoem'])
    df_temp=df.join(df_uws_w)
    print(df_temp.columns)
    Numbers_poets = len(df_temp.loc[df_temp['unique word'].notna()].groupby(["Poet"]).count())
    f.write(f"That number of Poems correspond with {Numbers_poets} Poets")
        
    df_temp=df_temp.loc[df_temp['unique word'].notna()]
    df_temp.groupby('year').count()
    x=list(df_temp.index)
    y=list(df_temp['Title'])
   
    plt.bar(x,y)
    plt.title(f"Number of Poems with the word {word} by year")
    plt.ylabel('number of poems')
    plt.xlabel('Years')
    # falta mejorar la gráfica!!!
    plt.savefig('output/f_uw.png', bbox_inches='tight')
    f.close()
    return True
# 
def analysis_year(df,year_int):
    df=df.loc[df.year > 10*int(year_int/10) ]
    df=df.loc[df.year < 10*(int(year_int/10)+1) ]
    grap=df.groupby(level='Poet').count()
    grap=grap.sort_values(by=['Poem'],ascending=False)
    y=list(grap.Poem.values)[:10]
    x=list(grap.index)[:10]  
    decade = 10*int(year_int/10)
    plt.barh(x,y)
    plt.title(f"Ten more prolific authors in the {decade}'s ")
    plt.ylabel('number of poems')
    plt.xlabel('Author')
    plt.savefig('output/f_year.png', bbox_inches='tight')

    return True

def analysis_general(df):
    df_grap=df.groupby('year').mean()
    df_grap=df_grap.reset_index()
    df_grap['decade']=df_grap.year.apply(lambda x: 10*int(x/10))
    df_grap=df_grap.drop(['idPoem','year','count_w','count_wu','count_l'], axis=1)
    data_grap=df_grap.groupby('decade').mean()
    x=list(data_grap.index)
    y=list(data_grap['complexity'].values)
    plt.scatter(x,y)
    plt.title(f"Complexity evolution")
    plt.ylabel('Complexity (Unique words/Number words)')
    plt.xlabel('Years')
    plt.savefig('output/f_complex.png', bbox_inches='tight')

    return True


