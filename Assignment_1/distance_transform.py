## 
 #          File: distance_transform.py
 #          Author: Tarun Yadav
 #          Last Modified: January 24, 2012
 #          Topic: Distance Transform Algorithm for city block distance measurement
 #          Instructor: Dr. Anil Seth
 # ----------------------------------------------------------------
 #
 #          Script to run algorithm on an input images.
 #          Image Dimensions (WxH) - width(column) x height(row)
##


from os import *
from sys import *
from scipy import *
from numpy import *
from Image import *
from pylab import *

# open the image passed in argument
image = open(sys.argv[1])
size = image.size
image_array = array(image);
image_arr = ones((size[1],size[0]),dtype=int32)
MAX = size[0]+ size[1]

#define backgound intensity. Handle both type of images where max intensity is 1 or 255
if int(sys.argv[2])==1:
    BACKGROUND_0 = 0
    BACKGROUND_1 = 0
else:
    BACKGROUND_0 = 1
    BACKGROUND_1 = 255

#Initialization of distace matrix, all image points are set to 0 and other are set to greater than the distance that could be between two pixels
if (len(image_array.shape)==2):
	for i in range(0,size[1],1):
	    for j in range(0,size[0],1):
	   		if image_array[i][j]== BACKGROUND_0 or image_array[i][j]== BACKGROUND_1:
	   			image_arr[i][j] = MAX
    	    else:
	            image_arr[i][j] = 0
else:
	for i in range(0,size[1],1):
	    for j in range(0,size[0],1):
	   	    if image_array[i][j][0]== BACKGROUND_0 or image_array[i][j][0]== BACKGROUND_1:
	   	    	image_arr[i][j] = MAX
	   	    else:
	   	    	image_arr[i][j] = 0		            	

# Top to Bottom and Left to Right Movement
for i in range(0,size[1],1):
    for j in range(0,size[0],1):
        
        if image_arr[i][j] != 0:
            self=image_arr[i][j]
            if i-1 <0 and j-1 < 0:
                prev_row= image_arr[i][j]
                prev_column= image_arr[i][j]
                
            if i-1<0 and j-1>=0:
                prev_row= image_arr[i][j]
                prev_column= image_arr[i][j-1]+1

            if i-1>=0 and j-1<0:
                prev_row= image_arr[i-1][j]+1
                prev_column= image_arr[i][j]
                
            if i-1>=0 and j-1>=0:
                prev_row= image_arr[i-1][j]+1
                prev_column= image_arr[i][j-1]+1
                
            image_arr[i][j] = min(self,prev_row,prev_column)

# Bottom to Up and Right to Left  Movement           
for i in range(size[1]-1,-1,-1):
    for j in range(size[0]-1,-1,-1):
        
        if image_arr[i][j] != 0:
            self=image_arr[i][j]
            if i+1 > size[1]-1 and j+1 > size[0]-1:
                prev_row= image_arr[i][j]
                prev_column= image_arr[i][j]
                
            if i+1 > size[1]-1 and j+1 <= size[0]-1:
                prev_row= image_arr[i][j]
                prev_column= image_arr[i][j+1]+1

            if i+1 <= size[1]-1 and j+1 > size[0]-1:
                prev_row= image_arr[i+1][j]+1
                prev_column= image_arr[i][j]
                
            if i+1 <= size[1]-1 and j+1 <= size[0]-1:
                prev_row= image_arr[i+1][j]+1
                prev_column= image_arr[i][j+1]+1
                
            image_arr[i][j] = min(self,prev_row,prev_column)            

# writing distace martrix to the output folder with _output.txt extension
file_name= sys.argv[1].split('/')

# check if output directory exists or not. if doesn't exists then create it
if (os.path.exists(os.path.dirname(file_name[0]+'_Output/'))==False):
    os.mkdir(file_name[0]+'_Output',0777)

#if output file exists then delete it
output_file_name = file_name[0]+'_Output/'+file_name[1].split('.')[0]+'_output.txt'
if (os.path.exists(output_file_name)==True):
    os.remove(output_file_name)

# writing distance matix to output file    
fd = os.open(output_file_name ,os.O_EXCL|os.O_RDWR|os.O_CREAT,0777)
for i in range(0,size[1],1):
        os.write(fd,str(image_arr[i])+'\n')
os.close(fd)

# Image formed based on distace from original image pixels. Images points are shown in black and affinity toward white as distance increases from the iamge.
image_mod=fromarray(image_arr)
image_mod.save(file_name[0]+'_Output/'+file_name[1].split('.')[0]+'_output.gif')
image_mod.show()


