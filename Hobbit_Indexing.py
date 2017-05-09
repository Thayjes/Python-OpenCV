# -*- coding: utf-8 -*-
"""
Created on Tue May 09 13:53:43 2017

@author: tsrivas
"""

from Hobbit_Histogram import RGBHistogram
import cv2
import argparse
import glob # To get the paths of the image we are going to index
import cPickle # To dump our index to disk

#construct the argument parser
ap=argparse.ArgumentParser()
ap.add_argument("-d","--dataset",help='Path to the directory that contains images \
to be indexed')
ap.add_argument("-i","--index",help='Path to where the computed index will be stored')
args=vars(ap.parse_args())

#initialize dictionary for indices, to store our quanitifed images,
# with the 'key' of the dictionary bring the image filename
# and the 'value' our computed features

index={} # Dictionary initialization

# initialize the image descriptor -- a 3D RGB histogram with
# 8 bins per channel

desc=RGBHistogram([8,8,8])

# Using glob
# Use glob to grab the image paths and loop over them

for imagePath in glob.glob(args["dataset"] + "/*.png"):
    # extract out unique image ID (i.e the filename)
    k = imagePath[imagePath.rfind("/")+1:] #?
    
    # load the image, describe it using RGB Histogram
    # descriptor and update the index
    image=cv2.imread(imagePath)
    features=desc.describe(image)
    index[k]=features

# we are done indexing our image, now we can write our
# index to disk

f=open(args["index"],"w")
f.write(cPickle.dumps(index))
f.close

