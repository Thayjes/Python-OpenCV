import numpy as np
import cv2
from math import sqrt
from matplotlib import pyplot as plt
from image import *
def Niblack(image):
	n1,n2=image.shape
	#k=0.4 #Niblack
	k=0.1 #Sauvola
	w=31 #Both so far
	R=128
	#image_padded=np.pad(image,(w-1)/2,'edge')
	Out=np.zeros(image.shape,dtype=np.uint8)
	image=cv2.GaussianBlur(image, (7,7), 0)
	m=np.zeros(image.shape)
	kernelmean=np.ones((w,w),dtype="float")*(1.0/(w*w))
	m=cv2.filter2D(image,-1,kernelmean,borderType=cv2.BORDER_REPLICATE)
	meansquare=cv2.filter2D(image**2,-1,kernelmean,borderType=cv2.BORDER_REPLICATE)
	stddev=(meansquare-m**2)**(0.5)
	#Out[image>m+ k*stddev-25]=255 #This is Niblack's method
	Out[image> m*(1+k*( (stddev/R)-1 ) )]=255 #This is Sauvola's method
	bmask=255-Out
	#plt.figure(0),plt.imshow(bmask,'gray'),plt.show()
	median=cv2.medianBlur(bmask,7)
	#median=bmask
	#plt.figure(1),plt.imshow(median,'gray'),plt.show()
	erosion_kernel=np.ones( (3,3) )
	dilation_kernel=np.ones( (3,3) ) 
	median=cv2.erode(median,erosion_kernel,0) #Erode then Dilate to remove the specks of noise!!!
	#plt.figure(2),plt.imshow(median,'gray'),plt.show()
	median=cv2.dilate(median,dilation_kernel,1) 
	output=median
	vprofile=np.divide(np.sum(median,axis=0,dtype=np.float32),bmask.shape[0])
	hprofile=np.divide(np.sum(median,axis=1,dtype=np.float32),bmask.shape[1])
	plt.figure(0),plt.imshow(median,'gray'), plt.show()#plt.figure(1),plt.imshow(image,'gray'), plt.show()
	plt.figure(1),plt.subplot(2,1,1),plt.imshow(median,'gray'),plt.subplot(2,1,2),plt.plot(vprofile), plt.show()
	plt.figure(2),plt.subplot(2,1,1),plt.imshow(median,'gray'),plt.subplot(2,1,2),plt.plot(hprofile),plt.show()
	return output

    