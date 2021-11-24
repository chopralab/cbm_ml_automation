#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 12:20:27 2021

@author: prageeth_wijewardhane
"""

import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

directory = 'tdmab_frags' ## Change the directory here

os.mkdir(directory + "_jpgs")

def svg_to_jpg(directory):
    for i in os.listdir(directory):
        drawing = svg2rlg(directory + "/" + i)
        renderPM.drawToFile(drawing, directory + "_jpgs" + "/" + i + ".jpg", fmt = "JPG")
        
svg_to_jpg(directory)
