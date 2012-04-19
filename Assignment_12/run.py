## 
 #          File: skeleton.py
 #          Author: Tarun Yadav
 #          Last Modified: April 18, 2012
 #          Topic: To find out skeleton of an image using morphological operators
 #          Instructor: Dr. Anil Seth
 # ----------------------------------------------------------------
 #
 #          Script to find skeleton of an image using  dilation,erosion,open,close operaotrs.
 #          Image Dimensions (WxH) - width(column) x height(row)
##

#Basic import for python imaging 
from os import *
from sys import *
from scipy import *
from numpy import *
from Image import *
from pylab import *
from time import *
import string
sys.setrecursionlimit(2000)
## import all functions of morphological operators defined in the function file
from morpho_operators import *

def init():
	global image
	global image_array
	global size
	global image_output

	image = open(sys.argv[1])
	image = image.convert('L')
	#image=image.filter(BLUR)
	image_array = array(image)
	size = image_array.shape
	image_array = array(image_array,dtype=float)
	image_output = zeros((size[0],size[1]),dtype=float)
	
#Save the output file
def SaveToFile(output_name,t_init):
	global image_output			
	global image_array
	t_end = time()
	
	file_name= sys.argv[1].split('/')
	# check if output directory exists or not. if doesn't exists then create it
	if (os.path.exists(os.path.dirname(file_name[0]+'_morpho_operators/'))==False):
	    print "\nCreating Directory "+file_name[0]+"_morpho_operators ... Done"
	    os.mkdir(file_name[0]+'_morpho_operators',0777) 
	else:
	    print "\nOutput Directory "+file_name[0]+"_morpho_operators already exist... Done"		

	#convert array from float to uint8 for image display
	image_output = image_output.astype('uint8')
					
	# convert from array to image
	image_mod=fromarray(image_output);
	print "Saving the operator applied image to output directory..."
	output_name = output_name + '_time_taken_' + str(t_end-t_init)+'_sec'
	# save the image in destination folder	
	image_mod.save(file_name[0]+'_morpho_operators/'+file_name[1].split('.')[0]+output_name+'.gif')
	print "Output image is saved in output Directory with name: "+ file_name[1].split('.')[0]+output_name+'.gif   ...Done\n'
	
	print "----------------------------------------------------------------------------------------------------------------"
	print ("\nTotal time taken to run the Pogram is : "+str(t_end-t_init)+" seconds")
	print "----------------------------------------------------------------------------------------------------------------"
	
	import matplotlib.pyplot as plt
	plt.subplot(1,3,1)
	plt.imshow(image_array)
	plt.subplot(1,3,2)
	plt.imshow(image_output)
	plt.subplot(1,3,3)
	plt.imshow(image_output-image_array)
	plt.show()
	
	#image_mod.show()

# input for neighbor approach, gaussian smoothing and tolerance value for region detection
def user_input_fun():
	operator = raw_input("\n To apply Dilation Operator Press 1:  \n To apply Erosion Operator Press 2: \n To apply Open Operator Press 3: \n To apply Close Operator Press 4: \n To find Skeleton Press 5: \n Default is Skeleton [Press Enter]: \n")

	if(operator==""):
		operator = 5
	elif(operator !="1" and operator !="2" and operator !="3" and operator !="4" and operator !="5"):
		print(" Please choose the one of the followings: ")
		user_input_function();
	N = raw_input("\n How many times you want to apply operator [Default is 1[Press Enter]]: ")
	if(N==""):
		N = 1
	return int(operator),int(N)
			
				
#main function which will be run 
def main():		
	t_init= time()
	# Calling the user input function to get maximum no. of regions and tolerance
	(operator,N) = user_input_fun()
	# initialization of all variables and arrays
	init()
	global image_array
	global image_output
	#image_array[image_array==255]=1
	St_element = zeros((3,3),dtype=float)
	St_element[0]= [0,1,0]
	St_element[1]= [1,1,1]
	St_element[2]= [0,1,0]
	image_output=image_array
	for i in range(0,N):
		if (operator==1):
			image_output=Dilation(image_output,St_element)
			output_name = '_Dilated_'
		elif (operator==2):
			image_output=Erosion(image_output,St_element)
			output_name = '_Eroded_'
		elif (operator==3):
			image_output=Open(image_output,St_element)
			output_name = '_Opened_'
		elif (operator==4):	
			image_output=Close(image_output,St_element)
			output_name = '_Closed_'
		elif (operator==5):
			image_output=Skeleton(image_output,St_element)
			output_name = '_Skeleton_'
	
	SaveToFile(output_name,t_init)
	# in case to rerun the program		
	rerun = raw_input("\nPress 'q' to quit  : \n"+"Press Enter to run again: \n")
	if(rerun==""):
		main()
		
main()
	
