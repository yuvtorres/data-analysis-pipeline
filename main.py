#Programa para análizar poesía
import sys
sys.path.insert(0, 'src/')
from import_tool import import_data_poetry
import argparse

# Define the description of the programa
file1 = open("src/description.txt","r")
description_text = '\n'.join( file1.readlines() )
file1.close()
parser = argparse.ArgumentParser(description=description_text)

# optional arguments for initialize the analysis
parser.add_argument('--ini_stat', action='store_true',
            help='Show the initial statistics of the Database (default: False)')
parser.add_argument('--create_unique_word', action='store_true',
        help='Rebuild the analysis by unique word (takes about 20 sec!)')
parser.add_argument('--query_ybird_wiki', action='store_true',
        help='Remake the complete query for year of born to wikipedia API (takes about 5 min!)')

# optional arguments for present the analysis
parser.add_argument('--word', metavar='W', type=str, help='Show the statistics by decade of the word')
parser.add_argument('--year', metavar='Y', type=int, help='Show the statistics of the Year when it is possible')
parser.add_argument('--mailto', metavar='W', type=str, help='Send a report to the email address provided, this command expects a valid email as parameter.')


args = parser.parse_args()

print(args)

# Import data and create new variables
path='input/PoetryFoundationData.csv'
df=import_data_poetry(path,args.ini_stat,args.create_unique_word,args.query_ybird_wiki)


