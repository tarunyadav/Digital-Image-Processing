## 
 #          File: edge_detection.py
 #          Author: Tarun Yadav
 #          Last Modified: Feburary 13, 2012
 #          Topic: applying robert,sobel and laplace operators on the image with sharp and unsharp mask
 #          Instructor: Dr. Anil Seth
 # ----------------------------------------------------------------
 #
 #          Script to apply various operators for edge detectionand sharping
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
image_array = array(image_array,dtype=float)
image_arr = zeros((size[0],size[1]),dtype=float)
#Save the output file
def SaveToFile(output_name):
	global image_arr				
	# writing distance matrix to the output folder with _output.txt extension
	file_name= sys.argv[1].split('/')

	# check if output directory exists or not. if doesn't exists then create it
	if (os.path.exists(os.path.dirname(file_name[0]+'_Edge/'))==False):
	    print "\nCreating Directory "+file_name[0]+"_Edge ... Done"
	    os.mkdir(file_name[0]+'_Edge',0777) 
	else:
	    print "\nOutput Directory "+file_name[0]+"_Edge already exist... Done"		

	#convert array from float to uint8 for image display
	image_arr = image_arr.astype('uint8')

	# convert from array to image
	image_mod=fromarray(image_arr);
	print "Saving the Edge converted image to output directory..."
	# save the image in destination folder	
	image_mod.save(file_name[0]+'_Edge/'+file_name[1].split('.')[0]+output_name+'.gif')
	print "Edge converted image is saved in output Directory with name: "+ file_name[1].split('.')[0]+output_name+'.gif ...Done\n'
	image_mod.show()


#Function to robert operator to image array
def robert():
	global image_arr
	for i in range(0,size[0]-1,1):
		 for j in range(0,size[1]-1,1):
				image_arr[i][j] =  abs(image_array[i][j]-image_array[i+1][j+1])+abs(image_array[i][j+1]-image_array[i+1][j])
										
	image_arr = image_arr.clip(0,255)							
	print "\nApplying Robert Operator: "+"...Done\n"
	output_name = '_Robert_operator_'
	SaveToFile(output_name)			
			    		
#Function to sobel operator to image array
def sobel(edge_type):
	global image_arr
	if(edge_type=='h'):
			a_1_1= 1;	a_1_2=2	;	a_1_3=1
			a_2_1= 0;	a_2_2=0	;	a_2_3=0
			a_3_1=-1;	a_3_2=-2	;	a_3_3=-1
			edge_type = 'horizontal'
	elif(edge_type=='v'):
			a_1_1=-1;	a_1_2=0	;	a_1_3=1
			a_2_1=-2;	a_2_2=0	;	a_2_3=2
			a_3_1=-1;	a_3_2=0	;	a_3_3=1	
			edge_type = 'vertical'
	elif(edge_type=='d1'):
			a_1_1= 0;	a_1_2=1	;	a_1_3=2
			a_2_1=-1;	a_2_2=0	;	a_2_3=1
			a_3_1=-2;	a_3_2=-1	;	a_3_3=0	
			edge_type = 'diagonal_-45_deg'
	elif(edge_type=='d2'):
			a_1_1= 2;	a_1_2=1	;	a_1_3=0
			a_2_1= 1;	a_2_2=0	;	a_2_3=-1
			a_3_1= 0;	a_3_2=-1	;	a_3_3=-2	
			edge_type = 'diagonal_+45_deg'

	for i in range(1,size[0]-1,1):
			 for j in range(1,size[1]-1,1):
						image_arr[i][j] = (a_1_1*image_array[i-1][j-1] + a_1_2*image_array[i-1][j] + a_1_3*image_array[i-1][j+1]+						     a_2_1*image_array[i][j-1] + a_2_2*image_array[i][j] + a_2_3*image_array[i][j+1]+ a_3_1*image_array[i+1][j-1] + a_3_2*image_array[i+1][j] + a_3_3*image_array[i+1][j+1])
										     
	image_arr = image_arr.clip(0,255)																	     
	print "Applying edge detection with "+edge_type+"filter ...Done\n"
	output_name = '_sobel_'+edge_type
	SaveToFile(output_name)
	

#Function to robert operator to image array
def laplace(method_used):
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
				#print image_array[i][j]
										
	image_arr = image_arr.clip(0,255)							
	print "\nApplying Laplace Operator with "+method_used+" approach ...Done\n"
	output_name = '_Laplace_operator_'+method_used
	SaveToFile(output_name)	
	
# input for type of noise that user want to add
def user_input_fun():
	operator_type = raw_input("\nPress 1 to apply Robert operator to image : "+"\nPress 2 to apply Sobel operator to image :"+"\nPress 3 to apply Laplace operator to image :"+"\nPress Enter to exit: \n")
	# Wrong input case	
	if(operator_type==""):
		exit()
	elif(operator_type != "1" and operator_type != "2" and operator_type != "3"):
		print "\nWrong Input, Please type the correct one"
		return user_input_fun()
	else:
		return int(operator_type)

# Calling the user input function for noise type input
operator_type = user_input_fun();		
##Robert Operator
if (operator_type==1):
	robert();
	
##Sobel Operator	
elif (operator_type==2):	
	edge_type = raw_input("\nPress h for horizontal edge detection : "+"\nPress v for vertical edge detection: "+"\nPress d1 for -45 deg. diagonal edge detection:  "+"\nPress d2 for +45 deg. diagonal edge detection: \n")
	sobel(edge_type);
	
##Laplace Operator
elif(operator_type==3):
	method_used = int(raw_input("\nPress 1 for edge detection using 4 neightbor approach : "+"\nPress 2 for edge detection using 8 neightbor approach : \n"))
	laplace(method_used);
	

	
