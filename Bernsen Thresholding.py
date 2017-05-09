# Bernsen Algorithm :
# local contrast = max - min (local window)
# contrast threshold = user defined value
# mid_gray = (max+min)/2
# if (local contrast < contrast threshold)
    # if (mid_gray >=128):
        # pixel = object
    # else:
        # pixel = background
# else:
    # if (pixel>=mid_gray):
        # pixel = object
    # else:
        # pixel = background
        
#finding the max and min pixel intensity in a local window.

#Bernsen Thresholding
from operator import *
import numpy as np
import cv2
#image=np.arange(9,dtype='uint8').reshape(3,3)
kernel=np.ones( (7,7),dtype='float32')
(iH,iW)=image.shape[:2]
(kH,kW)=kernel.shape[:2]
contrast_threshold=50
#max=np.zeros(iH*iW,dtype='uint8')
#min=np.zeros(iH*iW,dtype='uint8')

pad=(kW-1)/2
imagep=cv2.copyMakeBorder(image,pad,pad,pad,pad,cv2.BORDER_REPLICATE)
Out=np.zeros((iH,iW),dtype='uint8')
print imagep
for y in np.arange(pad,iH+pad):
    for x in np.arange(pad,iW+pad):
        roi=imagep[y-pad:y+pad+1,x-pad:x+pad+1]
        #print roi
        max=roi.max()
        min=roi.min()
        local_contrast=max-min
        #print local_contrast
        mid_gray=(max+min)/2
        #print mid_gray
        if local_contrast<contrast_threshold:
            if (mid_gray>=158):
                Out[y-pad,x-pad]=255
            else:
                Out[y-pad,x-pad]=0
        else:
            if image[y-pad,x-pad]>=mid_gray:
                Out[y-pad,x-pad]=255
            else:
                Out[y-pad,x-pad]=0
        
        
        #local contrast = max-min
        #mid_gray = (max+min)/2
plt.imshow(Out,'gray'),plt.show()
