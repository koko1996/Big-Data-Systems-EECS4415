##########################################
# EECS4415 Assignment 3                  #
# Filename: plot.py                      #
# Author: NANAH JI, KOKO                 #
# Email: koko96@my.yorku.com             #
# eecs_num: *********                    #
##########################################
# This plotiing script is meant to be used for both spark_counts.py and spark_sentiment.py output
# files, this will keep displaying the results of aforementioned scripts in real time 

import matplotlib.pyplot as plt
from matplotlib import animation
import re
import time
import argparse


# parser to parse the command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("fileName", help="path to the file that contains the data to visualize")
args = parser.parse_args()

# open the file to read from
f = open(args.fileName,"r")
tags = {}

# initialize the figure 
fig = plt.figure()
# 1x1 grid, first subplot
ax1 = fig.add_subplot(1,1,1)

# this will be called iteratively by animation.FuncAnimation on each interval
def animate(i):
    # where are we in the file
    where = f.tell()
    # read next line
    line = f.readline()
    # if this is not an empty line and it is not the seperator line from the spark's output
    if line and (not re.match('^-',line)):
        # parse the line 
        parse = line.split()
        tags[parse[0]]=int(parse[1])
    # sort the output for easier visualization 
    sorted_values = sorted(tags.items(), key=lambda x: x[0])
    ax1.clear()
    ax1.bar(range(len(sorted_values)), [val[1] for val in sorted_values] , align='center', color="b")
    ax1.set_xticks(range(len(sorted_values)), minor=False, )
    ax1.set_xticklabels([val[0] for val in sorted_values], fontsize=6, rotation=20)
    ax1.plot()

ani = animation.FuncAnimation(fig, animate, interval=1)

# start the animation
plt.show()