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
def Dilation(Image, St_element):
	size= Image.shape
	st_size=St_element.shape
	N = st_size[0]
	M=st_size[1]
	Image_dialted= zeros((size[0],size[1]),dtype=int);
	mask = (St_element==1)
	
	for i in range(0,size[0],1):
			 for j in range(0,size[1],1):
			 		if(Image[i][j]==1):
					    		if(i in range(0,(N/2)) or  i in range (size[0]-(N/2), size[0]) or j in range(0,(M/2)) or j in range(size[1]-(M/2),size[1])):
					    				start_row = max(-(N/2),0-i)
					    				end_row = min((N/2),size[0]-1-i)
					    				start_column = max(-(M/2),0-j)
					    				end_column = min((M/2),size[1]-1-j)
					    		else : 
									start_row=-(N/2)
									end_row=(N/2)
									start_column=-(M/2)
									end_column=(M/2)
									
							Window=Image[i+start_row:i+end_row][j+start_column:j+end_column]
							window[N/2][m/2]=0
							Window[mask]=1
							Image_dilated[i+start_row:i+end_row][j+start_column:j+end_column] = Window
										
	return Image_dilated
		
#Function to apply erosion on a given image
#@parameters: image and structure element
#@return: image after applying erosion to it		
def Erosion(Image, St_element):
	size= Image.shape
	st_size=St_element.shape
	N = st_size[0]
	M=st_size[1]
	Image_eroded= zeros((size[0],size[1]),dtype=int);
	mask = (St_element==1)
	
	for i in range(0,size[0],1):
			 for j in range(0,size[1],1):
			 		if(Image[i][j]==1):
					    		if(i in range(0,(N/2)) or  i in range (size[0]-(N/2), size[0]) or j in range(0,(M/2)) or j in range(size[1]-(M/2),size[1])):
					    				start_row = max(-(N/2),0-i)
					    				end_row = min((N/2),size[0]-1-i)
					    				start_column = max(-(M/2),0-j)
					    				end_column = min((M/2),size[1]-1-j)
					    		else : 
									start_row=-(N/2)
									end_row=(N/2)
									start_column=-(M/2)
									end_column=(M/2)
									
							Window=Image[i+start_row:i+end_row][j+start_column:j+end_column]
							Window_mask = (Window==1)
							
							if (all(mask==Window_mask)):
								Image_eroded[i][j] = 1
							else:
								Image_eroded[i][j] = 0
										
	return Image_dilated

#Function to apply open on a given image
#@parameters: image and structure element
#@return: image after applying open to it	
def Open(Image, St_element):
	Image_eroded=Erosion(Image_dilated,St_element)
	Image_opened=Dilation(Image_eroded,St_element)
	return Image_opened

#Function to apply close on a given image
#@parameters: image and structure element
#@return: image after applying close to it	
def Close(Image, St_element):
	Image_dilated=Dilation(Image,St_element)
	Image_closed=Erosion(Image_dilated,St_element)
	return Image_closed
	
#Function to find skeleton for a given image
#@parameters: image and structure element
#@return: Skeleton of the image
def Close(Image, St_element):
	Image_dilated=Dilation(Image,St_element)
	Image_closed=Erosion(Image_dilated,St_element)
	return Image_closed
