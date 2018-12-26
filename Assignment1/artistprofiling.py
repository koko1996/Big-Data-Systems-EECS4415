###################################################################################################
# EECS4415 Assignment 1                                                                           #
# Filename: artistprofiling.py                                                                    #
# Author: NANAH JI, KOKO                                                                          #
# Email: koko96@my.yorku.com                                                                      #
# eecs_num: *********                                                                             #
# I have written my own calculator as well as the tfidf calculator                                #
# Which made the performance of this script slower since the built in (python packages)           #
# implementation makes use of parallel execution and this script is single threaded               #
###################################################################################################

import sys
import csv
import re
import nltk
import math
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer


#Read the input as comma seperated file from the STDIN. I assume that the input conists of a header row which
#is the first line and it contains the names of the columns which are artist,song,link,text and every following
#row is the data artist represents the artist's name, song represents the song's name, link represent the path to
#the file (not used in this assignment), text represents the lyrics of the song
#no assumptions are made about the order of the input rows
data = csv.DictReader(sys.stdin, delimiter=',')

    
listOfLyricsByArtist={}            # map that has the artist name as the key and value is a map that consists
                                   # of words that this artist uses across the songs and the value is the number
                                   # of occurence of this word accross songs of this artist
vocabulary={}                      # Map that consists of word as the key and the value is an integer that represents
                                   # the number of artists use this word across their songs  in the dataset
tokenzr = TweetTokenizer()      

for row in data:
    Words = listOfLyricsByArtist.get(row["artist"],{})
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
    listOfLyricsByArtist.update({row["artist"]:Words})

    
for artist,value in listOfLyricsByArtist.items():
    print("Top words in {}".format(artist))
    # calculate tfidf for all words used by each artist across artists
    scores = {word: ( (1 + math.log(value[word])) *(math.log(len(listOfLyricsByArtist) /  vocabulary.get(word,0))) ) for word in value}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:100]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))  
    
