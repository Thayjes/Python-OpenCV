# -*- coding: utf-8 -*-
"""
Created on Mon May 08 16:11:52 2017

@author: tsrivas
Rotate images correctly with openCV and Python
"""
#import the necessary packages
import numpy as np
import argparse
import cv2
import imutils

#construct the argument parser
ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",help='Specify the path to the image')
args=vars(ap.parse_args())

image=cv2.imread(args["image"])

#now loop over the rotation angles
for angle in np.arange(0,360,15):
    rotated=imutils.rotate(image,angle)
    cv2.imshow("Rotated(problematic)",rotated)
    cv2.waitKey(0)
#loop again over the angles this time making sure its not cut off
for angle in np.arange(0,360,15):
    rotated=imutils.rotate_bound(image,angle)
    cv2.imshow("Rotated(Correct)",rotated)
    cv2.waitKey(0)

#This is the function which is inside imutils
def rotate_bound(image,angle):
    #the inputs are image and angle
    #first grab the dimensions of the image and find the center
    h,w=image.shape[:2]
    (cx,cy)=(w//2,h//2)
   #The rotation matrix M from cv2.getRotationMatrix is defined as follows:
   # M = [ alpha beta (1-alpha)*cx-beta*cy
   #      -beta alpha beta*cx+(1-alpha)*cy]
   #Where alpha=scale*cos(theta),beta=scale*sin(theta)
   #So now we get the rotation matrix and the sin and cos values
    M=cv2.getRotationMatrix2D((cx,cy),-angle,1.0) #-angle --> clockwise
    sin=np.abs(M[0,0])
    cos=np.abs(M[0,1])
   #Now we define the new dimensions of the image after rotation
   #And updated our M matrix before using cv2.warpAffine to apply the rotation
    nW=int( (h*sin)+(w*cos) )
    nH=int( (h*cos)+(w*sin) )
   
    M[0,2]+=(nW//2)-cx
    M[1,2]+=(nH//2)-cy
   
    return cv2.warpAffine(image, M, (nW,nH) ) #image, rot matrix, (width,height)
   
   
        
