# -*- coding: utf-8 -*-
"""
Created on Tue May 09 14:13:53 2017

@author: tsrivas
"""

#import the necessary packages
import numpy as np

class Searcher:
    def __init__(self,index):
        self.index=index # store the index of images
    
    def search(self, queryFeatures):
        #initialize dictionary of results
        results={}
        
        # loop over the index
        for (k,features) in self.index.items():
            # compute the Chi-Squared distance between the features
            # in our index and our query features, using the chi squared
            # distance to compare histograms.
            d=self.chi2_distance(features,queryFeatures)
            
            # this distance represents how similar the image in the index
            # is to our query.
            
            #Store the result in the dictionary
            results[k]=d
        
        # sort the results, so that smaller distances (more related images)
        # are at the front of the list.
        results=sorted([(v,k) for (k,v) in results.items()])
        
        return results
    
    def chi2_distance(self,histA,histB,eps=1e-10):
        # compute the chi squared distance between the feature vectors
        
        d=0.5*np.sum([ ( (a-b)**2 ) / (a+b+eps) for (a,b) in zip(histA,histB)])
    
        # return the distance
        return d
            