###################################################################################################
# EECS4415 Assignment 1                                                                           #
# Filename: songprofiling.py                                                                      #
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

    
listOfLyrics=[]        # List of Tuples where each tuple represents (song,map) structure
                       # The map in the tuple is a map where key is a word in the lyrics 
                       # of a song and value is the number of times it appears in that song
                       # using list allows for two different songs that have the same name
                       # to coexist in the list 
vocabulary={}          # Map that consists of word as the key and the value is an integer 
                       # that represents the number of songs this word appears in the dataset
tokenzr = TweetTokenizer()

for row in data:
    Words = {}              # Map where key is a word in the lyrics of a song and value is 
                            # the number of times it appears in the song
    # TweetTokenizer will keep words that have apostrophes in it as a one words
    for word in tokenzr.tokenize(row["text"]):
        word = word.lower()                         # the word comparision should be case insensitive
        # Make sure the length is greater than one and word starts with a character and it is not a stop word or punctuation
        if len(word) > 1 and re.match('^[a-zA-Z]',word) and word not in stopwords.words('english') + list(punctuation):
            value = 1 + Words.get(word,0)       # default return is zero which means it does not exist in the map
            Words.update({word:value})          # update the number of appearance of this word in this song
            if value == 1:                           # if this is the first time this word appears in this song
                count = 1 + vocabulary.get(word,0)   # then add it to the list(map) of the total words and increment 
                vocabulary.update({word:count})      # the count value for this word
    listOfLyrics.append((row["song"],Words))


for lyrics in listOfLyrics:
    print("Top words in {}".format(lyrics[0]))
    # calculate tfidf for all all the words in this song
    scores = {word: (1 + math.log(lyrics[1][word])) * (math.log(len(listOfLyrics) / (vocabulary.get(word,0)))) for word in lyrics[1]}
    # sort the list in descending order of the score for the given word
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True) 
    for word, score in sorted_words[:50]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))  
    
