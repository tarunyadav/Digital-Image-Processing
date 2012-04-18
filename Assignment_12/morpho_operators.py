## 
 #          File: morpho_operators.py
 #          Author: Tarun Yadav
 #          Last Modified: April 18, 2012
 #          Topic:  Morphological operators dilation, erosion, open and close
 #          Instructor: Dr. Anil Seth
 # ----------------------------------------------------------------
 #
 #          Script containing functions for the operators dilation,erosion,open and close 
 #          Image Dimensions (WxH) - width(column) x height(row)
##

#Basic import for python imaging 
from os import *
from sys import *
from scipy import *
from numpy import *
from Image import *
from pylab import *

#Function to apply dilation on a given image
#@parameters: image and structure element
#@return: image after applying dialtion to it
def Dilation(Image, St_element,origin):
	size= Image.shape;
	
	return Image
		
#Function to apply erosion on a given image
#@parameters: image and structure element
#@return: image after applying erosion to it		
def Erosion(Image, St_element):

	return Image

#Function to apply open on a given image
#@parameters: image and structure element
#@return: image after applying open to it	
def Open(Image, St_element):

	return Image

#Function to apply close on a given image
#@parameters: image and structure element
#@return: image after applying close to it	
def Close(Image, St_element):

	return Image
