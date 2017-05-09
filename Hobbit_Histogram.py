# -*- coding: utf-8 -*-
"""
Created on Tue May 09 12:47:14 2017
Comparison of color histograms to determine similarity between images
@author: tsrivas
"""
#import the necessary packages
import numpy as np
import cv2

#The image descriptor for this example will be a 3D RGB Histogram
#Define the image descriptor class
# We initialize the descriptor with the # of bins parameter.
# It returns a feature vector (flattened bins) for the image.
class RGBHistogram:
    def __init__(self,bins):
        # store the number of bins the histogram will use        
        self.bins=bins
        
    def describe(self,image):
        #compute a 3D histogram in the RGB colorspace,
        # then normalize the histogram so that images
        # with the same content, but either scaled larger
        # or smaller will have (approx) the same histogram
        hist = cv2.calcHist([image],[0,1,2],None,self.bins,[0,256,0,256,0,256])
        cv2.normalize(hist,hist) #The images may be scaled 
        
        #return a flattened array of the 3D histogram
        return hist.flatten()


        
