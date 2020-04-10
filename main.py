#Programa para análizar poesía
import sys
sys.path.insert(0, 'src/')
from import_tool import import_data_poetry

# Import and Process Data
path='input/PoetryFoundationData.csv'
df=import_data_poetry(path)


