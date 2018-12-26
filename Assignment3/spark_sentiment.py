"""
    This Spark app connects to a script running on another (Docker) machine
    on port 9009 that provides a stream of raw tweets text. That stream is
    meant to be read and processed here, it processes the tweets by counting the 
    number of positive, negative and neutral tweet that was recieved for each topic
    in the topic_list based on the hashtags in hashlist_by_topic ,it outputs the values
    to Both a file called "sentiments.txt" and stdout. Both apps are designed to
    be run in Docker containers.

    To execute this in a Docker container, do:
    
        docker run -it -v $PWD:/app --link twitter:twitter eecsyorku/eecs4415

    and inside the docker:

        spark-submit spark_app.py

    Based on: https://www.toptal.com/apache/apache-spark-streaming-twitter
    Original author: Hanee' Medhat, Tilemachos Pechlivanoglou

"""
##########################################
# EECS4415 Assignment 3                  #
# Filename: spark_sentiment.py           #
# Author: NANAH JI, KOKO                 #
# Email: koko96@my.yorku.com             #
# eecs_num: *********                    #
##########################################

from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys
import requests


# create spark configuration
conf = SparkConf()
conf.setAppName("TwitterStreamApp")
# create spark context with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
# create the Streaming Context from spark context, interval size 10 seconds
ssc = StreamingContext(sc, 10)
# setting a checkpoint for RDD recovery (necessary for updateStateByKey)
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 9009
dataStream = ssc.socketTextStream("twitter",9009)

# open the file sentiments.txt in append mode for the results
f= open("sentiments.txt","a+")

# list of topics to analyze
topic_list = sc.parallelize(['apple','twitter','cryptocurrency', 'facebook' ,'google']).collect()
# broadcast the list so that all workers get it one instead of having to send it on each interval
sc.broadcast(topic_list)

# list of list where each list inide the big list has two values that represent the hashtags to follow for each
# topic in topic_list and the mapping between the topiclist and hashlist_by_topic is that each hashtag in 
# hashlist_by_topic[i] is for topic topiclist[i] for all i in [0,1,2,3,4,5]
hashlist_by_topic = sc.parallelize([ ['#aapl', '#mac'], ['#twitter', '#twtr'], ['#bitcoin' , '#blockchain'], ['#fb', '#facebook'], ['#youtube', '#googl'] ]).collect()
# broadcast the list so that all workers get it one instead of having to send it on each interval
sc.broadcast(hashlist_by_topic)

# checks if the line has hashtags that are related to exactly one topic in the topic_list
# so that if we get a line that has more than one hashtag and at least two of them are related to
# a different topic in the topic_list we disregard this line because of the ambiguity
def has_hashtags(line):
    ans = 0 
    for word in line.split(" "):
        for hashtags in hashlist_by_topic:
            if word.lower() in hashtags:
                ans += 1 
    return (ans == 1)

# filter out the tweets that don't have the hashtags that we are looking for or has at least 
# two hashtags from two different topics
hashtags = dataStream.filter(has_hashtags)

# find the topic that this line (tweet) is about
def find_topic(line):
    ans=-1
    for word in line.split(" "):
        i = 0
        for hashtags in hashlist_by_topic:
            if word.lower() in hashtags:
                ans = i
            i+=1  
    return topic_list[ans]
        
# find the sentiment of this tweet based on nlt SentimentIntensityAnalyzer compound value
def find_polarity(sentence):
    sia = SIA()
    score = sia.polarity_scores(sentence)
    if score["compound"] > 0.2: 
        return 'positive'
    elif score["compound"] < -0.2: 
        return 'negative'
    else: 
        return 'neutral'
  

# map each hashtag to be a pair of (hashtag,1)
hashtag_counts = hashtags.map(lambda x: (find_topic(x)+"_"+find_polarity(x), 1 ))

# adding the count of each hashtag to its last count
def aggregate_tags_count(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)

# do the aggregation, note that now this is a sequence of RDDs
hashtag_totals = hashtag_counts.updateStateByKey(aggregate_tags_count)

# process a single time interval
def process_interval(time, rdd):
    # print a separator
    print("----------- %s -----------" % str(time))
    f.write("----------- %s -----------\n" % str(time))
    try:
        all_elements = rdd.collect()

        # print it nicely
        for tag in all_elements:
            print('{:<40} {}'.format(tag[0], tag[1]))
            f.write('{:<40} {}\n'.format(tag[0], tag[1]))
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)


# do this for every single interval
hashtag_totals.foreachRDD(process_interval)



# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()

# close the file
f.close() 
