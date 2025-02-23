# -*- coding: utf-8 -*-
"""
Created on Thu May 11 09:02:21 2017

@author: tsrivas
"""

# import the necessary packages
import numpy as np
import argparse
import cv2

# initialize the current frame of the video, along with list of
# ROI points along with whether or not this is input mode
frame = None
roiPts=[]
inputMode= False

def selectROI(event, x, y, flags, param):
    # grab the reference to the current frame, list of ROI
    # points and whether or not it is ROI selection mode
    global frame, roiPts, inputMode
    
    # if we are in ROI selection mode, the mouse was clicked,
    # and we do not already have 4 points, then update the
    # list of ROI points with the (x,y) location of the click
    # and draw the circle
    if inputMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPts)<4:
        roiPts.append((x,y))
        cv2.circle(frame,(x,y),4,(0,255,0),2)
        cv2.imshow("frame",frame)

def main():
    # construct the argument parser
    ap=argparse.ArgumentParser()
    ap.add_argument("-v","--video",help='Path to the optional video file')
    args=vars(ap.parse_args())
    
    # grab the reference to the current frame, list of ROI points
    # and whether or not it is in ROI selection mode
    global frame, roiPts, inputMode
    
    # if the video path was not supplied, grab the reference to the camera
    if not args.get("video",False):
        camera=cv2.VideoCapture(0)
    else:
        camera=cv2.VideoCapture(args["video"])
        
    # setup the mouse caLLBACK
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame",selectROI)
    
    # initialize the termination criteria for cam shift, indicating
    # a max of 10 iterations or movement by atleast one pixel
    # along with the bounding box of the ROI
    
    termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10,1)
    roiBox=None
    
    # keep looping over the frames
    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()
        
        if not grabbed:
            break
        
        # See if the ROI has been computed
        if roiBox is not None:
            # convert the current frame to the HSV color space
            # and perform mean shift
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            backProj = cv2.calcBackProject([hsv],[0],roiHist,[0,180],1)
            
            # apply cam shift to the back projection, convert the
            # points to a bounding box, and then draw them
            (r, roiBox) = cv2.CamShift(backProj, roiBox, termination)
            pts=np.int0(cv2.boxPoints(r))
            cv2.polylines(frame, [pts], True, (0,255,0), 2)

        # show the frame and record if the user presses a key
        cv2.imshow("Frame",frame)
        key=cv2.waitKey(1) & 0xFF

        # handle if the 'i' key is pressed, then go into ROI
        # selection mode
        if key == ord("i") and len(roiPts)<4:
            # indicate that we are on onput mode and clone the frame
            inputMode = True
            orig = frame.copy()
    
        # keep looping until 4 reference ROI points have been 
        # selected; press any key to exit ROI selection
        # mode once 4 points have been selected
            while len(roiPts)<4:
                cv2.imshow("frame",frame)
                cv2.waitKey(0)
        
            # determine the top-left and bottom-right points
            roiPts = np.array(roiPts)
            s = roiPts.sum(axis=1)
            tl = roiPts[np.argmin(s)]
            br = roiPts[np.argmax(s)]
        
            # grab the ROI for the bounding box and convert it to the 
            # HSV color space
            roi = orig[tl[1]:br[1], tl[0]:br[0] ]
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
            # compute a HSV histogram for the ROI and store the
            # bounding box
            roiHist = cv2.calcHist([roi], [0], None, [16], [0,180])
            roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
            roiBox = (tl[0], tl[1], br[0], br[1])
        
        # if the 'q' key is pressed, stop the loop
        elif key == ord("q"):
            break
    # Cleanup the camera
    camera.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()