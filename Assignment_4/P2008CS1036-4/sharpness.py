## 
 #          File: sharpness.py
 #          Author: Tarun Yadav
 #          Last Modified: Feburary 13, 2012
 #          Topic: applying sharening to images
 #          Instructor: Dr. Anil Seth
 # ----------------------------------------------------------------
 #
 #          Script to apply sharping to the images
 #          Image Dimensions (WxH) - width(column) x height(row)
##
  
# Basic import for python imaging 
from os import *
from sys import *
from scipy import *
from numpy import *
from Image import *
from ImageFilter import *
from pylab import *
from ImageOps import *
import numpy

# open the image which is passed in argument
image = open(sys.argv[1])  
image = image.convert('L')
image_array = array(image);
size = image_array.shape
image_array = array(image_array,dtype=float)
image_arr = zeros((size[0],size[1]),dtype=float)
#Save the output file
def SaveToFile(output_name):
	global image_arr				
	file_name= sys.argv[1].split('/')

	# check if output directory exists or not. if doesn't exists then create it
	if (os.path.exists(os.path.dirname(file_name[0]+'_Sharpening/'))==False):
	    print "\nCreating Directory "+file_name[0]+"_Sharpening ... Done"
	    os.mkdir(file_name[0]+'_Sharpening',0777) 
	else:
	    print "\nOutput Directory "+file_name[0]+"_Sharpening already exist... Done"		

	#convert array from float to uint8 for image display
	image_arr = image_arr.astype('uint8')

	# convert from array to image
	image_mod=fromarray(image_arr);
	print "Saving the Sharpened image to output directory..."
	# save the image in destination folder	
	image_mod.save(file_name[0]+'_Sharpening/'+file_name[1].split('.')[0]+output_name+'.gif')
	print "Sharpened image is saved in output Directory with name: "+ file_name[1].split('.')[0]+output_name+'.gif ...Done\n'
	image_mod.show()


#Function to sharpen image by unsharp masking
def unsharp_masking(C):
	global image_arr
		
	Blurred_image = image.filter(BLUR)								
	Blurred_image_array = array(Blurred_image)	
	edge_array = image_array - Blurred_image_array

# if want to do normalization 
	
#	factor = 255.0/(numpy.max(edge_array)-numpy.min(edge_array))
#	P_i = numpy.min(edge_array)
#	for i in range(0,size[0],1):
#		for j in range(0,size[1],1):
#			edge_array[i][j] = factor*(edge_array[i][j]-P_i)
			
	edge_array = edge_array.clip(0,255)

	image_arr = image_array +  C*edge_array
	image_arr = image_arr.clip(0,255)							
	print "\nApplying unsharp masking with constant "+str(C)+" ...Done\n"
	output_name = '_unsharp_masking_'+str(C)
	SaveToFile(output_name)			
			    		
#Function to sharpen image by Laplace Sharpening
def laplace_sharpening(method_used,C):
	global image_arr
	if(method_used==1):
		a_1_1= 0;	a_1_2=1	;	a_1_3=0
		a_2_1= 1;	a_2_2=-4	;	a_2_3=1
		a_3_1= 0;	a_3_2=1	;	a_3_3=0
		method_used = '4_neighbors'
	elif(method_used==2):
		a_1_1= 1;	a_1_2=1	;	a_1_3=1
		a_2_1= 1;	a_2_2=-8	;	a_2_3=1
		a_3_1= 1;	a_3_2=1	;	a_3_3=1	
		method_used = '8_neighbors'
	for i in range(1,size[0]-1,1):
		 for j in range(1,size[1]-1,1):
				image_arr[i][j] = (a_1_1*image_array[i-1][j-1] + a_1_2*image_array[i-1][j] + a_1_3*image_array[i-1][j+1]+						     a_2_1*image_array[i][j-1] + a_2_2*image_array[i][j] + a_2_3*image_array[i][j+1]+ a_3_1*image_array[i+1][j-1] + a_3_2*image_array[i+1][j] + a_3_3*image_array[i+1][j+1]) 

										
	image_arr = image_arr.clip(0,255)							
	print "\nApplying Laplace Operator with "+method_used+" approach...Done\n"	
	image_arr = image_array - C*image_arr
	image_arr = image_arr.clip(0,255)		
	print "\nApplying Laplace sharpening with constant "+str(C) +" ...Done\n"
	output_name = '_Laplace_sharpening_'+method_used +'_'+str(C)
	SaveToFile(output_name)	
	
# input for type of sharpening that user wants to do
def user_input_fun():
	sharpening_type = raw_input("\nPress 1 to apply unsharp masking to image : "+"\nPress 2 to apply laplace sharpening to image :"+"\nPress Enter to exit: \n")
	# Wrong input case	
	if(sharpening_type==""):
		exit()
	elif(sharpening_type != "1" and sharpening_type != "2" ):
		print "\nWrong Input, Please type the correct one"
		return user_input_fun()
	else:
		return int(sharpening_type)

# Calling the user input function for type of sharpening
sharpening_type = user_input_fun();		

##unsharp masking 
if (sharpening_type==1):
	C = float(raw_input("Type the constant C for sharpening(between 0.2-0.7) (Original + C*edge_image) :\n"))
	unsharp_masking(C)
	
##Laplace sharpening
elif(sharpening_type==2):
	method_used = int(raw_input("\nPress 1 for sharpening using 4 neighbor approach : "+"\nPress 2 for edge sharpening using 8 neighbor approach : \n"))
	C = float(raw_input("Type the constant C for sharpening(between 0.2-0.7) (Original - C*Laplacian) :\n"))
	laplace_sharpening(method_used,C)
	

	
