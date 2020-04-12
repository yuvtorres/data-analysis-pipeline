# funciones para importar las datos
import pandas as pd
import numpy as np
import re
from datetime import datetime
import timeit

# function to fit the Poem for analysis
def fit_Poem(poem):
    poem_fit= " ".join(re.split('\W+', poem))
    poem_fit=poem_fit.strip()
    poem_fit=poem_fit.replace('\r','\n')
    poem_fit=poem_fit.replace('\n\n','\n' )
    #poem_fit.translate(str.maketrans('', '', string.punctuation))
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
    df_uw=pd.read_csv('output/unique_words.txt')
    if ini_stats: print(f'the uw variable was created:\n {df_uw.describe()}')
    
    # Create the variable "b-year" takes time, it is done making a query to wikipedi API
    if create_born_wiki:create_looking_for_year()
    df_au_ye=pd.read_csv('output/byear_wiki.txt')

    
    return df
     
# Analysis by word
def analysis_word(df,word):

    return True

#Build the analisys of the unique words by poem in the df 
def build_unique_word(df):
    try:
        print('\n--> Building the analysis by unique words')
        f=open('output/unique_words.txt','w')
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
    
def create_looking_for_year(author):
    print('--> Beginning the query to MediaWiki API')
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
            print(f"error in query API wiki:{PARAMS}")
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
        data_bs=BeautifulSoup(DATA["parse"]["text"]["*"])
        data_bs.select('span.bday')[0].text
        date_born = datetime.strptime(data_bs.select('span.bday')[0].text, '%Y-%m-%d')
        au_wi_born.append(author,date_born)

    df=pd.DataFrame(au_wi_born)
    df.to_csv('output/byear_wiki.csv')
    stop = timeit.default_timer()
    print('\n--> Total time query to MediaWiki: ', stop - start) 
    print("We can check {len(authors_wiki)} birthday date from {len(autrhos)} Poets")

    return True
    
