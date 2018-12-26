#!/usr/bin/python

##########################################
# EECS4415 Assignment 2                  #
# Filename: iireducer.py                 #
# Author: NANAH JI, KOKO                 #
# Email: koko96@my.yorku.com             #
# eecs_num: *********                    #
##########################################

import sys

previous = None         # Store the value of the previous word
index =[]               # List To store the indexes 

# iterate through the input stream
for row in sys.stdin:   
        key,value = row.split('\t')  # parse the input line
        # check if this is a new key 
        if key != previous:
                # check if this is not the first iteration
                if previous is not None:
                    print(previous + '\t' + str(sorted(index)) )
                previous = key
                index = []       
        # append the id of the document to the list of indexes where this word appears       
        index.append(int(value)) 
print(previous + '\t' + str( sorted(index) ))
