# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 19:50:28 2015

@author: ronen
"""
from numpy import * 
from pylab import * 
import cv2


def smooth_corner(patchSize, angle, direction):
    feature = zeros((patchSize*2+1,patchSize*2+1))
    direction = 1.*direction / 180 * pi
    for i in range(-patchSize, patchSize+1,1):
        for j in range(-patchSize, patchSize+1,1):
            u = 1.*i*cos(direction+40) - 1.*j * sin(direction+40)
            v = 1.*i*sin(direction) + 1.*j * cos(direction)
            
            sign = 1 
            u += patchSize; 
            v += patchSize; 
            feature[i+patchSize,j+patchSize] = u #(u/ patchSize)**2 * (v/ patchSize)**2 
    return feature


def sharp_corner(patchSize, angle, direction):

    feature = zeros((patchSize*2+1,patchSize*2+1))
    direction = 1.*direction / 180 * pi
    for i in range(-patchSize, patchSize+1):
        for j in range(-patchSize, patchSize+1):
            u = 1.*i*cos(direction) - 1.*j * sin(direction)
            v = 1.*i*sin(direction) + 1.*j * cos(direction)
            if (u > 0 and v > 0):
                feature[i+patchSize,j+patchSize] = 1 
            else:
                feature[i+patchSize,j+patchSize] = 0
    return feature
#scorner = zeros((10,10))
#for i in range(10):
#    for j in range(10):
#        scorner[i,j] = i*j
#        
#corner = hstack([vstack([zeros((5,5)),ones((5,5))]),zeros((10,5))])

import harris

for angle in range(0, 180 , 15):
#    figure()
#    title("%d" % angle)
    size = 21
    k=0.04
#    imshow(smooth_corner(size ,0,angle), interpolation='none')
#    colorbar()
#    figure()
#    title("%d" % angle)
#    imshow(sharp_corner(size ,0,angle), interpolation='none')
#    figure()
#    title("hartis %d smoothe" % angle); 
    #figure()
    #smoth = smooth_corner(10,0,angle)[size-1: size+2, size-1: size+2]
    #imshow(smoth , interpolation='none')
    
    
    corner = smooth_corner(size,0,angle)
    
    corner = corner.astype('float64')
    corner = (((corner-corner.min())/  (corner.max()-corner.min()) * 255 )).astype("uint8")
    figure(); imshow(corner)
    
    croped, a, b, c = harris.GetHarrisCorrners(corner,k)
    croped = croped[3:-3,3:-3]
    a = a[3:-3,3:-3]
    b = b[3:-3,3:-3]
    c = c[3:-3,3:-3]
    center = np.where(croped==croped.max())
    center_x = center[0][0]
    center_y = center[1][0]
    print center_x, center_y
    center_x, center_y = 21,21
    a = a[center_x, center_y]
    b = b[center_x, center_y]
    c = c[center_x, center_y]
    
    croped[center_x, center_y] = croped.max()*2
    figure();imshow(croped)
    title(angle)
    croped = cv2.cornerHarris(corner ,3,3,k)
    
    
    mat = [[a, b],[ b, c]]
    U,s,V = svd(mat)
    print angle
    print s
    

    score =  abs(a*c - b*b) - k*(a + c)
    print 'Our', score
    print 'cv', croped[size+1,size+1]
    print
    

#    figure()
#    imshow(croped , interpolation='none')
#    croped = croped[size-1: size+2, size-1: size+2]
#    figure()
#    imshow(croped)
#    a = a[size-1:size+2, size-1:size+2]
#    b = b[size-1:size+2, size-1:size+2]
#    c = c[size-1:size+2, size-1:size+2]
#    print a
#    print "angle: ", angle 
#    print a[1,1]+c[1,1]
    #print b[1,1]
    #print c[1,1]
    



