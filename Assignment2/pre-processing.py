#!/usr/bin/python

##########################################
# EECS4415 Assignment 2                  #
# Filename: pre-processing.py            #
# Author: NANAH JI, KOKO                 #
# Email: koko96@my.yorku.com             #
# eecs_num: *********                    #
##########################################

# The purpose of this script is to clean up and prepare the data for the rest of the mappers
# If you want to save the output you can redirect the STDOUT of this script to a file and use that file
# python pre-processing.py < songdata.csv > preprocessed.out

import re
import sys
import csv
from nltk.tokenize import TweetTokenizer

# save the input to data where input is from a csv file
data = csv.DictReader(sys.stdin, delimiter=',')
# TweetTokenizer for better tokenizing the lyrics
tokenzr = TweetTokenizer()

id=0         # The document ID   
# loop through the input
for row in data:
    id+=1
    # save the lyrics of each song in a list after lowercaseing each word in it and cleaning up
    words = [ i.lower().replace("-","") for i in tokenzr.tokenize(row["text"]) if re.match('^[a-zA-Z]+[a-zA-Z\-]*$',i) and not re.match('(pre-)?(post-)?chorus',i.lower()) and not re.match('verse',i.lower()) and not re.match('break-down',i.lower()) ]
    # print each songs lyrics as a comma seperated words 
    print( str(id)+"," +','.join(map(str, words)))    
