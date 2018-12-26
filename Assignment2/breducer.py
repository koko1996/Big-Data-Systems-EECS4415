#!/usr/bin/python

##########################################
# EECS4415 Assignment 2                  #
# Filename: breducer.py                  #
# Author: NANAH JI, KOKO                 #
# Email: koko96@my.yorku.com             #
# eecs_num: *********                    #
##########################################

import sys

previous = None         # To keep The previous word 
count =0                # Total running Number of elements with this key


# Iterate through the input stram
for row in sys.stdin:
        # We know that he input is in key'\t'value format based on the umapper.py
        key,value = row.split('\t')
        # Reset the counter if this key does not match the previous key (keys are sorted)
        if key != previous:
                # Make sure this is not the first iteration 
                if previous is not None:
                    print(previous + '\t' + str(count) )
                previous = key
                count = 0
        # incremet the counter by value which should be one 
        count = count + int (value)
# Print the count for the last key        
print(previous + '\t' + str(count))
