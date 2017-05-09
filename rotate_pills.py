# -*- coding: utf-8 -*-
"""
Created on Mon May 08 17:20:43 2017
Rotate oblong shaped pill using rotate_bound
@author: tsrivas
"""
#import the necessary packages
import numpy as np
import argparse
import cv2
import imutils
from rotate_simple import rotate_bound

ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",help='Specify path to the image')

args=vars(ap.parse_args())

image=cv2.imread(args["image"])
image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
blur=cv2.GaussianBlur(image, (3,3), 0)
edged=cv2.Canny(blur,20,100)
cv2.imshow("Edged",edged)
cv2.waitKey(0)

#find contours in the edge map
(cnts)=cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts=cnts[0] if imutils.is_cv2() else cnts[1]

if len(cnts)>0:
    c=max(cnts,key=cv2.contourArea) #find the largest contour by area
    #now draw a mask for the pill
    mask=np.zeros(blur.shape,dtype='uint8')
    cv2.drawContours(mask,[c],-1,255,-1)
    cv2.imshow("Mask",mask)
    
    #compute its bounding box of pill, then extract the ROI,
    #and apply the mask
    (x,y,w,h)=cv2.boundingRect(c)
    imageROI=image[y:y+h,x:x+w]
    maskROI=mask[y:y+h,x:x+w]
    imageROI=cv2.bitwise_and(imageROI,imageROI,mask=maskROI)
    #loop over the rotation angles
    for i in np.arange(0,360,15):
        rotated=rotate_bound(imageROI,i)
        cv2.imshow("Rotated(correct)",rotated)
        cv2.waitKey(0)
    


    