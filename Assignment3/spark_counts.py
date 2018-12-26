"""
    This Spark app connects to a script running on another (Docker) machine
    on port 9009 that provides a stream of raw tweets text. That stream is
    meant to be read and processed here, it processes the tweets by counting the 
    number of occurance of each tweet in the hashlist RDD, it outputs the values
    to Both a file called "counts.txt" and stdout. Both apps are designed to
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
# Filename: spark_counts.py              #
# Author: NANAH JI, KOKO                 #
# Email: koko96@my.yorku.com             #
# eecs_num: *********                    #
##########################################


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

# open the file counts.txt in append mode for the results
f= open("counts.txt","a+")

# split each tweet into words
words = dataStream.flatMap(lambda line: line.split(" "))

# list that containt the 5 hashtags that this app is counting
hashlist = sc.parallelize(['#bitcoin' , '#blockchain', '#ai', '#machinelearning', '#cyber' ]).collect()
# broadcast the list so that all workers get it one instead of having to send it on each interval
sc.broadcast(hashlist)

# filter the words to get only the five hashtags
hashtags = words.filter(lambda w: w.lower() in  hashlist )


# map each hashtag to be a pair of (hashtag,1)
hashtag_counts = hashtags.map(lambda x: (x.lower(), 1))


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
        # sort counts (desc) in this time instance 
        sorted_rdd = rdd.sortBy(lambda x:x[1], False)
        all_elements = sorted_rdd.collect()

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
