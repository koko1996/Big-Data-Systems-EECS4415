##########################################
# EECS4415 Assignment 3                  #
# Filename: readme.txt                   #
# Author: NANAH JI, KOKO                 #
# Email: koko96@my.yorku.com             #
# eecs_num: *********                    #
##########################################

Introduction:
- This module implements a streaming applications for performing basic analytics on textual data that will be coming from Twitter stream.
This module has two processing scripts one spark_counts that counts the number of occurance of 5 hashtags in 
real time and the other one is spark_sentiment that counts the number of positive, negative and neutral tweet that was recieved based on the topic of the tweet

Twitter Client
- To run either one of these processing scripts you need to first run twitter app client on a docker image that 
gets the tweets from twitter and sends to the app that connects to it (data source)
start the docker image as follows:
    docker run -it -v $PWD:/app --name twitter -p 9009:9009 python bash
Packages to install:
    pip install -U git+https://github.com/tweepy/tweepy.git
run the client app:
    python twitter_app.py

Spark Streaming:
- To run the spark_counts.py script you need start a new docker image besides the client image that you just started (called twitter), you don't need to install 
any additional packages 
start the docker image:
    docker run -it -v $PWD:/app --link twitter:twitter eecsyorku/eecs4415
run the script:
    spark-submit spark_counts.py

output is written to both stdout and a file in the same directory named counts.txt

- To run the spark_sentiment.py script you need start a new docker image besides the client image that you just started (called twitter), you need to install any 
additional packages 
start the docker image:
    docker run -it -v $PWD:/app --link twitter:twitter eecsyorku/eecs4415
Packages to install:
    pip install nltk
    # issue the command "python"
    import nltk 
    nltk.download('vader_lexicon')
run the script:
    spark-submit spark_counts.py

output is written to both stdout and a file in the same directory named sentiments.txt

Note: to run either one of spark_counts.py and spark_sentiment.py the twitter client must be running simultaneously in another docker image named twitter 
Note: you can run both spark_counts.py and spark_sentiment.py in the same docker container (not at the same time )

Real Time Reporting:
- To run the plot.py script to visualize the output of either spark_counts.py and spark_sentiment.py (one script works for both outputs) on the output files of each Spark 
Streaming script on the local machine (not in docker)

To visualize the output of spark_counts.py
run plot.py on counts.txt as follows:
                python plot.py counts.txt

To visualize the output of spark_sentiment.py
run plot.py on sentiments.txt as follows 
                python plot.py sentiments.txt
