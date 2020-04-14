# Data|Analysis|Pipeline Poetry

## Introduction

Have You heard about the Orson Welles's clasic: "1984"?  Perhaps You have heard about Big Brother, the almigthy state that can control all your movements and finally all your thoughts. This analisys is based in another idea takes from the book: **If you can control the words the people use, you can control what people thinks**. This analysis attemps to see if there are any trend in the words used by poets. 

The analysis will use a public database from [kaggle](https://www.kaggle.com/tgdivy/poetry-foundation-poems/data#PoetryFoundationData.csv), that contains all poems (13854) from the [Poetry Foundation Poems](https://www.poetryfoundation.org). The data is complemented by some statistics like:

- Quantity of lines
- Quantity of words
- Number of words used (non repeated)
- List of words used one time (for each poem)

In order to find trends, it is necessary to join some data-time related with each poem. The data decided is the date of born of the Poet 
- Date the Poet was born (from Wikipedia API, and some webscraping)

## The Reports

The posiible reports are three at the moment. their are saved in the "output" folder:

1. Report by year: given a year, the program return a graph with the most prolific Poets.
	* --year
2. Report by word: given a word, the program return a graph with the use of this word as unique word in poems durign the time
	* --word
3. General report: the graph returned by the program is the evolution of the "complexity", calculate this complexity like the relation between words used just one time and the total number of words in the poem.
	* --general

(* --mailto : still for developed)

## Update the data and create unique words table

The program has two different option to manage the data base:

* --query_ybirth 	: option to update year of birthday. Its could takes about an hour because the scrapping in the web is slow.
* --create_unique_word	: with this option, the table of the unique words is recalculated. This table has the relation between words and Poems. 


