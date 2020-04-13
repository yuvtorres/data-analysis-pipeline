# funciones para importar las datos
import pandas as pd
import numpy as np
import re
from datetime import datetime
import time
import timeit
import requests
from bs4 import BeautifulSoup

# function to fit the Poem for analysis
def fit_Poem(poem):
    poem_fit= " ".join(re.split('\W+', poem))
    poem_fit=poem_fit.strip()
    poem_fit=poem_fit.replace('\r','\n')
    poem_fit=poem_fit.replace('\n\n','\n' )
    return poem_fit

##### Function to import, create initial variables and show initial statistics #####
def import_data_poetry(path, ini_stats=False,create_unique=False,create_born_wiki=False):
    df=pd.read_csv(path)
    print(f"Data imported from -->  {path} ")
    print(f"{len(df)} lines was imported, each line is equivalent to a poem.")
    print(f"{len(df.Poet.value_counts())} Poets")

    #### If ini_stats is True then show the result  ####
    columnas_str='\n'.join((list(df.columns)))
    if ini_stats: print(f'\nThe columns are:\n{columnas_str}\n')
    
    # Clean the column Unamed: 0
    df=df.drop(['Unnamed: 0'],axis=1)
    if ini_stats: print(f"\nThe column 'Unnamed: 0' was dropped.\n")
    
    # clean the title column
    df.Title=df.Title.apply(lambda x: x.replace('\r\r\n','').strip()) 
 
    # Create the column with a fit Poem for analysis
    df['Poem_fit']=df['Poem'].apply(fit_Poem)
    # Create the variable of numbers of lines by poem
    df['count_l']=df['Poem'].apply(lambda x:  len(x.split('\r\r\n')))    
    if ini_stats: print('\nthe column count_l (numbers of line by poem) was creatted, description:')
    if ini_stats: print(df['count_l'].describe())
    
    # Create the column with numbers of words
    count_words=lambda x : len(x.replace('\n',' ').replace('  ',' ').split(' '))
    df['count_w']=df['Poem_fit'].apply(count_words) 
    if ini_stats: print('\nthe column count_w (numbers of words by poem) was creatted, description:')
    if ini_stats: print(df['count_w'].describe())

    #Create the column with number of unique words
    count_unique_words=lambda x : len(set(x.replace('\n',' ').replace ('  ',' ').split(' '))) 
    df['count_wu']=df['Poem_fit'].apply(count_unique_words)
    if ini_stats: print('\nthe column count_wu (numbers of words (non repeted) by poem) was creatted, description:')
    if ini_stats: print(df['count_wu'].describe())

    # Create the variable "complexity": numbers of unique words by total number of words
    df['complexity']=df[['count_w', 'count_wu']].apply(lambda x : x['count_wu']/x['count_w'],axis=1)
    if ini_stats: print('\nthe column complexity (numbers of words (non repeted) / total number of words by poem) was creatted, description:')
    if ini_stats: print(df['complexity'].describe())
   
    print(f"""\nthe Poem {df.loc[df['count_w'].idxmax()].Title} from {df.loc[df['count_w'].idxmax()].Poet} id:{df['count_w'].idxmax()}, has the maximum numbers of words""")

    # Create the variable "Unique words" takes about 30 minute, so 
    # this option is deactivate by default

    if create_unique: build_unique_word(df)
    df_uw=pd.read_csv('data/unique_words.csv')
    if ini_stats: print(f'the uw variable was created:\n {df_uw.describe()}')
    
    # Create the variable "b-year" takes time, it is done making a query to 
    # wikipedi API and scrapping the poetry foundation

    authors=set([e for e in df.Poet])
    if create_born_wiki:create_looking_for_year(authors) 
    df_au_ye=pd.read_csv('data/byear_wiki.csv')
    if ini_stats:print(df_au_ye)
    
    if create_born_wiki:create_looking_for_year_scarp(authors)
    df_au_ye2=pd.read_csv('data/byear_pfun.csv')
    if ini_stats:print(df_au_ye2)
    
    return df
     
#Build the analisys of the unique words by poem in the df 
def build_unique_word(df):
    try:
        print('\n--> Building the analysis by unique words')
        f=open('data/unique_words.csv','w')
        start = timeit.default_timer()
        f.write('id_Poem,unique word\n')
        for k in range(len(df['Poem_fit'])):
            x=df['Poem_fit'][k].split(' ')
            x_dict=set(filter(lambda x:len(x)>4,x))
            [f.write( str(k) + ',' + e + '\n') for e in x_dict if x.count(e)==1]
        
        stop = timeit.default_timer()
        print('\n--> Total time creating the analysis of unique words: ', stop - start) 
        f.close
        return True
    except:
        print(f'Error building the analysis of unique words\n {start}\n {f} \n')
        return False
    
def create_looking_for_year(authors):
    print('\n--> Beginning the query to MediaWiki API\n')
    start = timeit.default_timer()
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    authors_wiki=[]

    for author in authors:
        PARAMS = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": author
        }   
        try:
            R = S.get(url=URL, params=PARAMS)
        except:
            print(f"\n!!!! error in query API wiki:{PARAMS}")
        DATA = R.json()
        if len(DATA['query']['search'])>0:
            
            if DATA['query']['search'][0]['title'] == author:
                authors_wiki.append(author)
    au_wi_born=[]
    for author in authors_wiki:
        PARAMS = {
                "action": "parse",
                "page": author,
                "format": "json"
                }

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        data_bs=BeautifulSoup(DATA["parse"]["text"]["*"],"lxml")
        if len( data_bs.select('span.bday') ) > 0:
                data_str=data_bs.select('span.bday')[0].text
                if len(data_str)==4:
                    date_born = datetime.strptime(data_str, '%Y')
                elif len(data_str)==10:
                    date_born = datetime.strptime(data_str, '%Y-%m-%d')
                else:
                    date_born=date_str

                au_wi_born.append([author,date_born])
    
    df=pd.DataFrame(au_wi_born,columns=['Poet','birthday'])
    print('Saving wiki query')
    df.to_csv('data/byear_wiki.csv')
    print('\n--> Total time query to MediaWiki: ', round(time.time() - start,2) ) 
    print(f"We can check {len(authors_wiki)} birthday date from {len(authors)} Poets")
    
    return True

def create_looking_for_year_scarp(authors):
    print('\n--> Beginning the scram to poetry foundation\n')
    start = timeit.default_timer()
    S = requests.Session()

    link_authors=[]
    for author in authors:
        author = author.replace(' ','%20')
        URL = "https://www.poetryfoundation.org/search?query="+author+"&refinement=poets"
        R = S.get(url=URL)
        data_bs=BeautifulSoup(R.text)
        link_n=data_bs.select('.c-hdgSans > a:nth-of-type(1)')
        if len(link_n)>0:
            link_authors.append([author, link_n[0]['href']])
    
    year_author=[]
    for link in link_autors:
        URL="https://www.poetryfoundation.org"+link[1]
        R=S.get(url=URL)
        data_bs=BeautifulSoup(R.text)
        birthday=data_bs.select('span.c-txt_poetMeta')
        if len(birthday)>0:
            year_author.append([link[0] ,birthday[0].text[:4]])


    df=pd.DataFrame(year_author,columns=['Poet','birthday'])
    print("\n--> saving data...\n" )
    df.to_csv("data/byear_pfun.csv")

    return True
