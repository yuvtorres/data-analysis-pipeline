#Programa para análizar poesía
import argparse
import sys
sys.path.insert(0, 'src/')
from import_tool import import_data_poetry
from analysis import analysis_unique_word
from analysis import analysis_year
from analysis import analysis_general
from report import generate_report
from report import generate_mail_report

def main():
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
    parser.add_argument('--query_ybirth', action='store_true',
            help='Remake the complete query for year of born in wikipedia API and scraping Poetry foundation (takes about 5 min!)')
    
    # optional arguments for the analysis
    parser.add_argument('--word', metavar='W', type=str,nargs='+',help='Show the statistics by decade of the word')
    parser.add_argument('--year', metavar='Y', type=int,nargs='+',help='Show the statistics of the Year when it is possible')
    parser.add_argument('--general', action='store_true', help='If active a general report is generated')
    
    #optional arguments for the report
    parser.add_argument('--mailto', type=str,nargs='+', help='Send a report to the email address provided, this command expects a valid email as parameter.')
    
    args = parser.parse_args()
    
    print(args)
    
    # Import data and create new variables
    path='input/PoetryFoundationData.csv'
    df=import_data_poetry(path,args.ini_stat,args.create_unique_word,args.query_ybirth)
    
    tipo_var=[]
    # Get the analysis by words
    if args.word:
        analysis_unique_word(df,args.word[0])
        tipo_var.append(["word",args.word[0]])
    
    if args.year:
        analysis_year(df,args.year[0])
        tipo_var.append(["year",args.year[0]])
    
    if args.general:
        analysis_general(df)
        tipo_var.append(["general",''])
    
    # Generate the report
    for e in tipo_var:
        generate_report(e)
    
    if args.mailto:
        generate_mail_report(args.mailto[0])

if __name__=="__main__":
    main()
