# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 17:45:27 2015

@author: ronen
"""

import cv2
import numpy as np
import harris
 
filename = 'klt/1.tif'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)

#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)
trackPoints = harris.GetHarrisTrackPoints(dst,0.01*dst.max())

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]
cv2.imshow('dst',img)

import pylab
pylab.figure(figsize=(10,10));
pylab.imshow(img)
trackPoints = np.array(trackPoints).T
pylab.scatter(trackPoints[1], trackPoints[0], s=80, facecolors='none', edgecolor='g')


R = harris.printOurCorrners(gray);


