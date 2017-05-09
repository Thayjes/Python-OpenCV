# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a python script for detecting skin
"""
#import the necessary packages
import imutils
import numpy as np
import cv2
import argparse

#construct the argument parse and parse the arguments
ap=argparse.ArgumentParser()
ap.add_argument("-v","--video",help="Path to the optional video file")
args=vars(ap.parse_args())

#Now we need to define what is skin, this is done in terms of HSV pixel
#intensities range of values
lower=np.array([0,48,80],dtype='uint8')
upper=np.array([20,255,255],dtype='uint8')

#if a video path was not supplied, grab the reference 
#to the gray

if not args.get("video",False):
    camera=cv2.VideoCapture()
    
else:
    camera=cv2.VideoCapture(args["video"])
#keep looping over the frames in the video
while True:
    (grabbed,frame)=camera.read()
    print frame
    
    if args.get("video") and not grabbed:
        break
    #resize the frame and convert it to HSV color space
    frame=imutils.resize(frame,width=400)
    converted=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    skinMask=cv2.inRange(converted,lower,upper) #we now have the mask to apply
    
    #apply a series of erosions and dilations to the mask
    #using an elliptical kernel    
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))
    skinMask=cv2.erode(skinMask,kernel,iterations=2)
    skinMask=cv2.dilate(skinMask,kernel,iterations=2)
    
    
    #blur the mask and apply it to the frame, to help remove noise
    skinMask=cv2.GaussianBlur(skinMask,(3,3),0)
    skin=cv2.bitwise_and(frame,frame,mask=skinMask)
    
    #show the skin in the image along with the mask
    cv2.imshow("Images",np.hstack([frame,skin]))
    
    #if the 'q' key is pressed, stop the loop
    if cv2.waitKey(1) & 0xFF==ord("q"):
        break
#cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
    
        
    

