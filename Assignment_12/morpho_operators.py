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
	Image_dilated= zeros((size[0],size[1]),dtype=int);
	mask = (St_element==1)
	window=zeros((N,M),dtype=float)
	for i in range(0,size[0],1):
			 for j in range(0,size[1],1):
			 		if(Image[i][j]==255 ):
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
							origin = Image[i][j]		
							Image[i][j]=0
							for m in range(start_row,end_row+1):
								for n in range(start_column,end_column+1):
										window[m+1][n+1]=Image[i+m][j+n]
							#window=Image[(i+start_row):(i+end_row)][(j+start_column):(j+end_column)]
							Image[i][j]=origin
							window[mask]=255
							#Image_dilated[i+start_row:i+end_row][j+start_column:j+end_column] = window
							for m in range(start_row,end_row+1):
								for n in range(start_column,end_column+1):
										Image_dilated[i+m][j+n]=window[m+1][n+1]
										
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
	window=zeros((N,M),dtype=float)
	for i in range(0,size[0],1):
			 for j in range(0,size[1],1):
			 		if((St_element[N/2][M/2]==1 and Image[i][j]==255 )or St_element[N/2][M/2]==0):
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
									
							#window=Image[i+start_row:i+end_row][j+start_column:j+end_column]
							for m in range(start_row,end_row+1):
								for n in range(start_column,end_column+1):
										window[m+1][n+1]=Image[i+m][j+n]
								
							window_mask = (window==255)
							if (all(mask==window_mask)):
								Image_eroded[i][j] = 255
							else:
								Image_eroded[i][j] = 0
										
	return Image_eroded

#Function to apply open on a given image
#@parameters: image and structure element
#@return: image after applying open to it	
def Open(Image, St_element):
	Image_eroded=Erosion(Image,St_element)
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
def Skeleton(Image, St_element):
	Image_dilated=Dilation(Image,St_element)
	Image_closed=Erosion(Image_dilated,St_element)
	return Image_Skeleton
