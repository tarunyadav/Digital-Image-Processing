## 
 #          File: Image_Operations_Ass2.py
 #          Author: Tarun Yadav
 #          Last Modified: January 31, 2012
 #          Topic: Some Basic operations on a image
 #          Instructor: Dr. Anil Seth
 # ----------------------------------------------------------------
 #
 #          Script to run algorithm on an input images.
 #          Image Dimensions (WxH) - width(column) x height(row)
##
  
# Basic import for python imaging 
from os import *
from sys import *
from scipy import *
from numpy import *
from Image import *
from pylab import *


# open the image which is passed in argument
image = open(sys.argv[1])  
image_array = array(image);
size = image_array.shape


# function for taking input from user
def user_input_fun():
	# User input for one of five parts of assignment
	user_input = raw_input("\n\tPress 1 to convert image to Binary\n"+"\tPress 2 to change the image pixels by a fix value\n"+"\tPress 3 to change the image by a fix factor\n"+"\tPress 4 to stretch the image from (Pi,Pf) to (0,255)\n" + "\tPress 5 to do histogram equalization\n"+"\tPress Enter to exit\n")

	## Wrong input	case	
	if(user_input==""):
		exit();
	elif(user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4" and user_input != "5"):
		print "Wrong Input, Please type the correct one";
		return user_input_fun();
	else:
		return int(user_input);

user_input = user_input_fun();

# Result matrix initialization according to user input
### IF user input is one means want to convert an image to binary then first convert the image to gray scale and then work
if(user_input==1):
		if (image.mode == 'RGB'):
			image_gray = image.convert('L');
			image_array = array(image_gray);
		image_arr = ones((size[0],size[1]),dtype=float);
		size = image_array.shape;
elif (len(size)==2):
	image_arr = ones((size[0],size[1]),dtype=float)
elif(len(size)==3):
	image_arr = ones((size[0],size[1],size[2]),dtype=float)
	
# PART -1 
##Image to Binary Conversion	
if (user_input==1):
		
		THRESHOLD = raw_input("Type the THRESHOLD value to change the image to binary [Default is mean(Press Enter)]]: ")

		if (THRESHOLD == ''):
			THRESHOLD = mean(image_array)
				
		for i in range(0,size[0],1):
		    for j in range(0,size[1],1):
		   		if image_array[i][j] > float(THRESHOLD):
		   			image_arr[i][j] = 255
				else:
					image_arr[i][j] = 0
	
		output_name = "_IM_to_BIN_TH_"+ str(THRESHOLD)

# PART-2
##Increment in intensity by a value		
elif(user_input==2):
		
		change_value = float(raw_input("Type the value by which you want to change the pixels intensity: "))
		image_arr = (change_value*image_arr) + image_array
		output_name = "_CHG_by_VAL_"+str(change_value)

#PART-3
##Increment in intensity by a factor
elif(user_input==3):
		change_factor = float(raw_input("Type the factor by which you want to change the pixels intensity: "))
		image_arr = change_factor*image_array
		output_name = "_CHG_by_FAC_"+str(change_factor)
		
#PART-4
## Contrast stretching from (Pi,Pf) to (0,255)		
elif(user_input==4):
		Pi = float(raw_input("\nType Pi here : "))
		Pf = float(raw_input("\nType Pf here : "))		
		
		
		P = 255.0/(Pf-Pi);		
		for i in range(0,size[0],1):
			    for j in range(0,size[1],1):
			    	if (len(size)==2):
			    		if(image_array[i][j]<Pi):
			    			image_arr[i][j]=0;
			    		elif(image_array[i][j]>Pf):
			    			image_arr[i][j] = 255;
			    		else:
				    		image_arr[i][j]= P*(image_array[i][j]-Pi);
				elif(len(size)==3):
					for k in range(0,size[2],1):
				    		if(image_array[i][j][k]<Pi):
				    			image_arr[i][j][k]=0;
				    		elif(image_array[i][j][k]>Pf):
				    			image_arr[i][j][k] = 255;
				    		else:
					    		image_arr[i][j][k]= P*(image_array[i][j][k]-Pi);
		output_name = "_("+str(Pi)+"_"+str(Pf)+")"+"_to_(0_255)"
		
#PART-5		
## Histogram Equalization
elif(user_input==5):
		comm_histogram = image.histogram();
		RGB_factor = 1;
		for i in range(0,len(comm_histogram),1):
			if(i/256.0 ==0 or i/256.0 ==1 or i/256.0 ==2 ):
				RGB_factor=0;
			else:
				RGB_factor=1;
			comm_histogram[i] = (RGB_factor*comm_histogram[i-1])+comm_histogram[i];
	
		factor = (255.0/(size[0]*size[1]));
		for i in range(0,size[0],1):
			    for j in range(0,size[1],1):
			    	if (len(size)==2):
				    		image_arr[i][j]= factor*comm_histogram[image_array[i][j]];
				elif(len(size)==3):
					for k in range(0,size[2],1):
				    		image_arr[i][j][k]= factor*comm_histogram[(k*256)+image_array[i][j][k]];
		output_name = "_histogram_equalization"


# in case of 1 and 4 we will not go beyond 255		
if (user_input==2 or user_input==3 or user_input==5):
		for i in range(0,size[0],1):
			    for j in range(0,size[1],1):
			    	if (len(size)==2):
				    	if (image_arr[i][j]>255):
				    		image_arr[i][j]=255
				elif(len(size)==3):
					for k in range(0,size[2],1):
				    		if (image_arr[i][j][k]>255):
				    			image_arr[i][j][k]=255

			    		
# writing distance matrix to the output folder with _output.txt extension
file_name= sys.argv[1].split('/')

# check if output directory exists or not. if doesn't exists then create it
if (os.path.exists(os.path.dirname(file_name[0]+'_Output/'))==False):
    os.mkdir(file_name[0]+'_Output',0777) 


#convert array from float to uint8 for image display
image_arr = image_arr.astype('uint8')

# convert from array to image
image_mod=fromarray(image_arr);


# save the image in destination folder	
image_mod.save(file_name[0]+'_Output/'+file_name[1].split('.')[0]+output_name+'_output.gif')
image_mod.show()


#------------------START-------------------------Histogram function by prev assignment----------------START-----------------------
#def histogram(image):
#	size = image.size
#	image_arr = array(image);

#	#initialization of histogram matrix
#	# Y axis in histogram
#	Frequency = zeros(256,dtype=int32)
#	# X axis is Intensity
#	Intensity = range(0,256)

#	# calculate # of pixel for a particular intensity
#	if (len(size)==2):
#	    for i in range(0,size[1],1):
#	        for j in range(0,size[0],1):
#	            intensity_val = image_arr[i][j]
#	            Frequency[intensity_val]= Frequency[intensity_val]+1
#	elif(len(size)==2):
#	    for i in range(0,size[1],1):
#        	for j in range(0,size[0],1):
#	            for k in range(0,size[2],1):
#        	        intensity_val = image_arr[i][j][k]
#        	        Frequency[intensity_val]= Frequency[intensity_val]+1
#	return Frequency

#----------------END---------------------------Histogram function by prev assignment-----------------END----------------------


