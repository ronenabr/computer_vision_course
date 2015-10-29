# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 17:16:26 2015

@author: ronen
"""


from pylab import *
import itertools
gray()
from scipy.signal import convolve2d

def gauss_filter(size, sigma):
    gauss = lambda (x,y) : exp(-(x**2+y**2)/(2*sigma**2))
    X,Y = meshgrid(arange(-(size/2),size/2+1),arange(-(size/2),size/2+1))
    return  gauss((X,Y))

refImage = imread("klt/seq1_corners.jpg")

#imshow(refImage)


m_x  = array([[-1,0,1]]*3)  * (1/3.)
m_y = m_x.T 

ker_g = gauss_filter(4, 1.5)
#ker_g = ones((3,3))
#imshow(ker_g); colorbar();
def dx_image(I):
    return  convolve2d(I, m_x)

def dy_image(I):
    return  convolve2d(I, m_y)

def GetHarrisCorrners(image, k=0.06):
    image = image.astype("float64")
    Ix = dx_image(image)
    Iy = dy_image(image)
    a = convolve2d(Ix**2,ker_g)
    c = convolve2d(Iy**2,ker_g)
    b = convolve2d(Ix*Iy,ker_g)
    raw_Image = a*c - b*b - k*(a + c)*(a + c);
    margin = (ker_g.shape[0] ) / 2 +1
    croped = raw_Image[margin:-margin,margin:-margin]
    
    return croped, a, b, c

epsilon=1e-10;
def GetHarrisCorrners2(image, k=0.06):
    Ix = dx_image(image)
    Iy = dy_image(image)
    a = convolve2d(Ix**2,ker_g)
    c = convolve2d(Iy**2,ker_g)
    b2 = convolve2d(Ix*Iy,ker_g)**2

    return (a*c-b2)/(a+c+epsilon)
    
    
def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    gray = gray.astype(int)
    #gray = rgb[:,:,0]
    
    return gray
    

def GetHarrisTrackPoints(R,threshold=20000):
    trackPoints = []    
    window_size = 5
    count = 0;
    for i,j in itertools.product(xrange(window_size,R.shape[0]-window_size),xrange(window_size,R.shape[1]-window_size)) :
        if(R[i,j] < threshold ):
            continue
        isMaxima = True
        for k,l in itertools.product(range(-window_size, window_size+1),range(-window_size, window_size+1)):
            if (R[i+k,j+l] - R[i,j]) > 1e-3:
                isMaxima = False
                break
        if isMaxima:
            trackPoints.append((i,j))
            count += 1
    print "count", count
    return trackPoints

def GetImageTrackPoints(image, threshold=10, k=0.06):    
    R = GetHarrisCorrners(image, k)
    #imshow(R)
    #colorbar()
    threshold = R.max()*0.01
    return GetHarrisTrackPoints(R, threshold), R
    
def printOurCorrners(image1):
    #image1 = imread(r"chessboard.png")

    
    trackPoints, R = GetImageTrackPoints(image1, 1 ,0.04)
    trackPoints = array(trackPoints).T
    
    #figure(figsize=(10,10))
    imshow(image1)
    scatter(trackPoints[1], trackPoints[0], s=40, facecolors='none', edgecolor='r')

#
#    figure(figsize=(10,10));
#    trs = 500
#    R[R>trs ] = trs 
#    imshow(R); title("R")
#    #colorbar()
#    scatter(trackPoints[1], trackPoints[0], s=40, facecolors='none', edgecolor='r')
    
    return R



if __name__ == "__main__":    
    image1 = imread(r"klt/Seq1/0135.jpeg")
    image2 = image1[:,:,1]
    R = printOurCorrners(image2)

