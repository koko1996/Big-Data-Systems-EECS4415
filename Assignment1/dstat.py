##########################################
# EECS4415 Assignment 1                  #
# Filename: dstat.py                     #
# Author: NANAH JI, KOKO                 #
# Email: koko96@my.yorku.com             #
# eecs_num: *********                    #
##########################################

import sys
import csv
import re
import nltk
import collections
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import matplotlib.pyplot as plt


#Read the input as comma seperated file from the STDIN. I assume that the input conists of a header row which
#is the first line and it contains the names of the columns which are artist,song,link,text and every following
#row is the data where artist represents the artist's name, song represents the song's name, link represent the path to
#the file (not used in this assignment), text represents the lyrics of the song
#no assumptions are made about the order of the input rows
data = csv.DictReader(sys.stdin, delimiter=',')
    

uniqueArtists={}            # Map of all artists (no duplicate artist because it is a map with key being the artist)
                            # the value consists of a list of two elements where the first element represents the number of 
                            # songs this artist have in the dataset and second element represent the sum of the number 
                            # of unique words per song for all the songs of this artist
songCount=0                 # Total number of songs in the input dataset
uniqueWordsPerSong=0        # Total number of unique words per song for all songs
tokenzr = TweetTokenizer()

for row in data:
    songCount +=1                                   # each row represents a song
    uniqueWords = set()                             # set to identify the unique words in a given song
    # TweetTokenizer will keep words that have apostrophes in it as a one word
    for word in tokenzr.tokenize(row["text"]):
        word = word.lower()                         # the word comparision should be case insensitive
        # Make sure the length is greater than one and word starts with a character and it is not a stop word or punctuation
        if len(word) > 1 and re.match('^[a-zA-Z]',word) and word not in stopwords.words('english') + list(punctuation):
            uniqueWords.add(word)    
    numUniqueWords = len(uniqueWords)
    uniqueWordsPerSong += numUniqueWords
    value= numUniqueWords + uniqueArtists.get(row["artist"],[0,0])[1]       # number of unique words per song for all songs of this artist
    count = uniqueArtists.get(row["artist"],[0,0])[0] + 1                   # number of songs this artist has in the dataset
    uniqueArtists.update({row["artist"]:[count,value]})                     
    
# Turn the value in the map uniqueArtists to represent the average number of uniqe words per song of an artist
# since this is the value that we are interested in
for k,v in uniqueArtists.items():
    value = v[1]
    count = v[0]
    uniqueArtists.update({k:value/count})


print("number of artists/bands in the collection is: " + str(len(uniqueArtists)))
print("number of songs in the collection is: " + str(songCount))
print("average number of songs per artist/band is: " + str(songCount/len(uniqueArtists)))
print("average number of unique words per song in the collection is: " + str(uniqueWordsPerSong/songCount))

print("average  number of  unique  words  per  song  of  an  artist/band,  sorted  by  artist/band  name  in  an alphanumerically ascending order is:")
for key, value in sorted(uniqueArtists.items(), key=lambda x: x[0]): 
    print("{} : {}".format(key, value))
print("\n")

# List of the top ten element that have the highes value of the "average number of unique words per song"
topTen = [(k,uniqueArtists[k]) for k in sorted(uniqueArtists, key=uniqueArtists.get, reverse=True)][:10]
plt.bar(range(len(topTen)), [val[1] for val in topTen], align='center')
plt.xticks(range(len(topTen)), [val[0] for val in topTen])
plt.xticks(rotation=70)
plt.show()
