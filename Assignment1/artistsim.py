###################################################################################################
# EECS4415 Assignment 1                                                                           #
# Filename: artistsim.py                                                                          #
# Author: NANAH JI, KOKO                                                                          #
# Email: koko96@my.yorku.com                                                                      #
# eecs_num: *********                                                                             #
# I have written my own jaccard similarity calculator as well as the tfidf calculator             #
# Which made the performance of this script slower since the built in (python packages)           #
# implementation makes use of parallel execution and this script is single threaded               #
###################################################################################################
import sys
import csv
import re
import nltk
import math
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
parser.add_argument("artist1_id", help="The id of the first artist to be compared")
parser.add_argument("artist2_id", help="The id of the second artist to be compared")
args = parser.parse_args()

    
#Read the input as comma seperated file from the file name passed in the arguument. I assume that the input conists
#of a header row which is the first line and it contains the names of the columns which are artist,song,link,text 
#and every following row is the data artist represents the artist's name, song represents the song's name, link
#represent the path to the file (not used in this assignment), text represents the lyrics of the song
#no assumptions are made about the order of the input rows
data = csv.DictReader(open(args.fileName), delimiter=',')


uniqueArtists=set()   # set of names of the artist 
wordsByArtist={}      # map that has the artist name as the key and the value is all the words that this
                      # artist used in all the songs in the dataset as a set
vocabulary={}        # Map that consists of word as the key and the value is an integer that represents
                     # the number of artists use this word across their songs  in the dataset                      
tokenzr = TweetTokenizer()

for row in data:
        # check if the artist has been seen before 
        if row["artist"] not in uniqueArtists:
                uniqueArtists.add(row["artist"])
        # will return an empty map if it does not exists in the map
        Words = wordsByArtist.get(row["artist"],{})
        # TweetTokenizer will keep words that have apostrophes in it as a one word
        for word in tokenzr.tokenize(row["text"]):
                word = word.lower()                         # the word comparision should be case insensitive
                # Make sure the length is greater than one and word starts with a character and it is not a stop word or punctuation
                if len(word) > 1 and re.match('^[a-zA-Z]',word) and word not in stopwords.words('english') + list(punctuation):
                        value = 1 + Words.get(word,0)
                        Words.update({word:value})
                        # if this is the first time this word is seen from a song of this artist
                        # then increment the count of this word's appearance across artists
                        if value == 1:
                                count = 1 + vocabulary.get(word,0)
                                vocabulary.update({word:count})
        keys = list(wordsByArtist)      # get the artist names that we are interested in 
        # only add it to the list if this Words (lyrics) belongs to the artists that we are interested 
        if len(uniqueArtists) == int(args.artist1_id) or len(uniqueArtists) == int(args.artist2_id) or row["artist"] in keys:
                wordsByArtist.update({row["artist"]:Words})

# error checking for the user input
if  len(uniqueArtists) < int(args.artist1_id) or len(uniqueArtists) < int(args.artist2_id):
        print ("The largest artist id entered should be equal to the number of unique artists in the collection")                
else :                
    important_words = []                             # list of tuples (two tuples) where each tuple represents the artist name as the first element
    for name,lyrics in wordsByArtist.items():        # and the top 100 words in that the artists uses across all of his/her songs is the second element (based on tfidf score)
            # calculate the tfidf score of each word (my implementation)
            scores = {word: (1 + math.log(lyrics[word])) * (math.log( len(uniqueArtists) / (vocabulary.get(word,0)))) for word in lyrics}
            # get a sorted list of top 100 words of each artist (based on tfidf score)        
            sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:100]
            # put the name of the artist and top 100 words of that artist in the list
            important_words.append((name,set(word[0] for word in sorted_words)))

    # calculate and print the Jaccard similarity of two artists where all the songs of each artist in the dataset represents a document
    # Therefore the total number of documents is the number of unique artists
    print("Jaccard similarity of the artists with ids "+important_words[0][0]+" and "+ important_words[1][0] + " is: ", jaccard_similarity(important_words[0][1], important_words[1][1]))
