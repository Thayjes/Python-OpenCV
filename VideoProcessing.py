
# coding: utf-8

# In[ ]:

import numpy as np
from imutils.video import FPS
import imutils
import cv2
import argparse

#We can convert .ipynb to .py using the command : ipython nbconvert --to python Name.ipynb
ap=argparse.ArgumentParser()
#Format (shortname,actualname,..,help message)
ap.add_argument("-v","--video",required=True,help="Specify the path to the input video file")
arg=vars(ap.parse_args())

#Open a pointer to the video stream and start FPS timer
stream=cv2.VideoCapture(arg["video"])
#Start a time to measure fps
fps=FPS().start()

#loop over the frames from the video stream
while True:
    #grab the frame from the threaded video stream using the .read() function
    (grabbed,frame)=stream.read()
    
    #if the frame was not grabbed, then we have reached the end of the stream
    if not grabbed:
        break
    
    #resize the frame and convert to grayscale(while still retaining 3 channels)
    frame=imutils.resize(frame,width=450)
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame=np.dstack([frame,frame,frame])
    
    #display a piece of text to the frame(so we can compare to the fast method)
    #cv2.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]) 
    cv2.putText(frame,"Slow Method", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    
    #show the frame and update the counter
    cv2.imshow("Frame",frame)
    cv2.waitKey(1)
    fps.update()
    
#stop the timer and display fps information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}:".format(fps.fps()))

#cleanup
stream.release()
cv2.destroyAllWindows()

    

