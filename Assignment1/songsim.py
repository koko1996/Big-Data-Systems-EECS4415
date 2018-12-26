###################################################################################################
# EECS4415 Assignment 1                                                                           #
# Filename: songsim.py                                                                            #
# Author: NANAH JI, KOKO                                                                          #
# Email: koko96@my.yorku.com                                                                      #
# eecs_num: *********                                                                             #
# I have written my own jaccard similarity calculator as well as the tfidf calculator             #
# Which made the performance of this script slower since the built in (python packages)           #
# implementation makes use of parallel execution and this script is single threaded               #
###################################################################################################
import sys
import math
import csv
import re
import nltk
import argparse
import collections
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import matplotlib.pyplot as plt
from pprint import pprint

# function that given two sets of words returns the jaccard similarity of 
# these two sets as a float between [0,1] representing their similarity
# higher value means they are more similar 
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = (len(set1) + len(set2)) - intersection
    return round(float(intersection) / union,5)


# parser to parse the command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("fileName", help="path to the file that contains the song collection")
parser.add_argument("song1_id", help="The id of the first song to be compared")
parser.add_argument("song2_id", help="The id of the second song to be compared")
args = parser.parse_args()


#Read the input as comma seperated file from the file name passed in the arguument. I assume that the input conists
#of a header row which is the first line and it contains the names of the columns which are artist,song,link,text 
#and every following row is the data artist represents the artist's name, song represents the song's name, link
#represent the path to the file (not used in this assignment), text represents the lyrics of the song
#no assumptions are made about the order of the input rows
data = csv.DictReader(open(args.fileName), delimiter=',')

listOfSongs=[]      # list of sets where the first set represents the set of words 
                    # used in the song with id song1_id and second set represents  
                    # the list of words in the song with id song2_id
                    # This list will have exactly two elements at the end
vocabulary={}       # Map that consists of word as the key and the value is an integer 
                    # that represents the number of songs this word appears in the dataset
songCount=0         # Total number of songs in the input dataset


tokenzr = TweetTokenizer()

i=1    
for row in data:
    songCount +=1                                   # each row represents a song
    Words = {}
    # TweetTokenizer will keep words that have apostrophes in it as a one word        
    for word in tokenzr.tokenize(row["text"]):
        word = word.lower()         # the word comparision should be case insensitive
        # Make sure the length is greater than one and word starts with a character and it is not a stop word or punctuation
        if len(word) > 1 and re.match('^[a-zA-Z]',word) and word not in stopwords.words('english') + list(punctuation):
            value = 1 + Words.get(word,0)       # default return is zero which means it does not exist in the map
            Words.update({word:value})          # update the number of appearance of this word in this song
            if value == 1:                           # if this is the first time this word appears in this song
                count = 1 + vocabulary.get(word,0)   # then add it to the list(map) of the total words and increment 
                vocabulary.update({word:count})      # the count value for this word
    if i == int(args.song1_id) or i == int(args.song2_id): # add to the list if and only if this is one of the songs that matches the id 
        listOfSongs.append((row["song"],Words))            # that the user is interested 
    i+=1                                                   # increment the counter of songs (documents)


# error checking for the user input
if  songCount < int(args.song1_id) or  songCount < int(args.song2_id): # if the input is incorrect
    print ("The largest song id entered should be equal to the number of songs in the collection")
else :            
    important_words = []                  # list of tuples (two tuples) where each tuple represents the song name as the first element
    for lyrics in listOfSongs:            # and the top 50 words in that songs is the second element (based on tfidf score)
        # calculate the tfidf score of each word (my implementation)
        scores = {word: (1 + math.log(lyrics[1][word])) * (math.log( songCount / (vocabulary.get(word,0)))) for word in lyrics[1]}
        # get a sorted list of top 50 words of each song (based on tfidf score)
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:50]
        # put the name of the song and top 50 words of that song in the list
        important_words.append((lyrics[0],set(word[0] for word in sorted_words)))

    # calculate and print the Jaccard similarity of two songs where each song in the dataset represents a document    
    print("Jaccard similarity of the songs with ids "+important_words[0][0]+" and "+ important_words[1][0] + " is: ", jaccard_similarity(important_words[0][1], important_words[1][1]))


    
