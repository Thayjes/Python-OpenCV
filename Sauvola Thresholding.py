import numpy as np
import cv2
from math import sqrt
from matplotlib import pyplot as plt
from image import *
n1,n2=image.shape
k=0.6
w=31
R=128
image_padded=np.pad(image,(w-1)/2,'edge')
Out=np.zeros(image.shape,dtype=np.uint8)
image=cv2.GaussianBlur(image, (7,7), 0)
m=np.zeros(image.shape)
kernelmean=np.ones((w,w),dtype="float")*(1.0/(w*w))
m=cv2.filter2D(image,-1,kernelmean)
meansquare=cv2.filter2D(image**2,-1,kernelmean)
stddev=(meansquare-m**2)**(0.5)
Out[image>m+ k*stddev-25]=255 #This is Niblack's method
#Out[image> m*(1+k*( (stddev/R)-1 ) )]=255 #This is Sauvola's method
bmask=255-Out
plt.figure(0),plt.imshow(bmask,'gray'),plt.show()
median=cv2.medianBlur(bmask,5)
#median=bmask
plt.figure(1),plt.imshow(median,'gray'),plt.show()
erosion_kernel=np.ones( (5,5) )
dilation_kernel=np.ones( (5,5) ) 
median=cv2.erode(median,erosion_kernel,1) #Erode then Dilate to remove the specks of noise!!!
plt.figure(2),plt.imshow(median,'gray'),plt.show()
median=cv2.dilate(median,dilation_kernel,1)
vprofile=np.divide(np.sum(median,axis=0,dtype=np.float32),bmask.shape[0])
plt.figure(3),plt.subplot(2,1,1),plt.imshow(median,'gray'),plt.subplot(2,1,2),plt.imshow(image,'gray'),plt.show()
plt.figure(4),plt.subplot(2,1,1),plt.imshow(median,'gray'),plt.subplot(2,1,2),plt.plot(vprofile), plt.show()
