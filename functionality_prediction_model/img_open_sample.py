#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 15:44:53 2021

@author: prageeth_wijewardhane
"""

#from PIL import Image
#  
## open method used to open different extension image file
#im = Image.open("tdmab_frags_jpgs/2_19.svg.jpg") 
#  
## This method will show image in any image viewer 
#im.show() 

import glob
import cv2 as cv
from PIL import Image

#path = glob.glob("tdmab_frags_jpgs/*.jpg")
#cv_img = []
#for img in path:
#    n = cv.imread(img)
#    cv_img.append(n)
#    
#print(cv_img)

im = Image.open("tdmab_frags_jpgs/2_15.svg.jpg")
im.show()