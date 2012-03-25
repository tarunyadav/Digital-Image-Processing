## 
 #          File: region_growing.py
 #          Author: Tarun Yadav
 #          Last Modified: March 19, 2012
 #          Topic: Region growing to find segments in a gray scale image
 #          Instructor: Dr. Anil Seth
 # ----------------------------------------------------------------
 #
 #          Script to find segments in a gray-scale image using region growing with seed points
 #          Image Dimensions (WxH) - width(column) x height(row)
##
  
# Basic import for python imaging 
from os import *
from sys import *
from scipy import *
from numpy import *
from Image import *
from pylab import *
import numpy

# open the image which is passed in argument
def init():
	global image
	global image_array
	global size
	global image_output
	global region_array
	
	image = open(sys.argv[1])
	image = image.convert('L')
	image_array = array(image);
	size = image_array.shape
	image_array = array(image_array,dtype=float)
	image_output = zeros((size[0],size[1]),dtype=float)
	#region_array to mark region # in for each pixel
	region_array = zeros((size[0],size[1]),dtype=float)

#Save the output file
def SaveToFile(output_name):
	global image_output			
	# writing distance matrix to the output folder with _output.txt extension
	file_name= sys.argv[1].split('/')

	# check if output directory exists or not. if doesn't exists then create it
	if (os.path.exists(os.path.dirname(file_name[0]+'_Frequncy_Filters/'))==False):
	    print "\nCreating Directory "+file_name[0]+"_Frequncy_Filters ... Done"
	    os.mkdir(file_name[0]+'_Frequncy_Filters',0777) 
	else:
	    print "\nOutput Directory "+file_name[0]+"_Frequncy_Filters already exist... Done"		

	#convert array from float to uint8 for image display
	image_output = image_output.astype('uint8')
	
	arr_min=image_output.min()
	arr_max=image_output.max()
	if(arr_min != arr_max):
		contrast_factor = 255.0/(arr_max-arr_min)
		for i in range(0,256):
			for j in range(0,256):
					image_output[i][j] =contrast_factor*(image_output[i][j]-arr_min)
			
	# convert from array to image
	image_mod=fromarray(image_output);
	print "Saving the filter applied image to output directory..."
	# save the image in destination folder	
	image_mod.save(file_name[0]+'_Frequncy_Filters/'+file_name[1].split('.')[0]+output_name+'.gif')
	print "Frequncy Filters appled  image is saved in output Directory with name: "+ file_name[1].split('.')[0]+output_name+'.gif   ...Done\n'
	#image.show()
	image_mod.show()
	

#Function to get segments for single spectral image
#@variable: image array to work with and for local maxima detection and 
#@return: threshold using iterative thresholding selction algorithm
	
#Function to apply Band Pass Filter image array
def BandPass(cutoff_freq_lower,cutoff_freq_upper):
	global image_output
	global FFT_image
	global Filtered_FFT
	global Filter

	for i in range(0,size[0],1):
		 for j in range(0,size[1],1):
	 		if (cutoff_freq_lower<=sqrt((i-size[0]/2)*(i-size[0]/2)+(j-size[1]/2)*(j-size[1]/2))<=cutoff_freq_upper):
				Filtered_FFT[i][j]=FFT_image[i][j]

	image_output = ifft2(ifftshift(Filtered_FFT)).real
	
	#image_output = odd_sign_change(image_output,size)
	image_output = image_output.clip(0,255)							
	print "\nApplying Band Pass frequency Filter   "+" ...Done\n"
	output_name = '_Band_Pass_Lower_'+str(cutoff_freq_lower)+"_Upper_"+str(cutoff_freq_upper)
	SaveToFile(output_name)	
	

# input for type of edge that user wants to detect
def user_input_fun():
	max_regions = raw_input("\n Type maximum no. of significant regions(int), you want to see [press Enter for default(all regions)]: \n")
	tolerance = raw_input("\n Type tolerance for region sperating intensity(int) criteria[press Enter for Default (Default is 10)]: \n")
		
	return int(max_regions),int(tolerance) 
			

#main function which will be run 
def main():		

	# initialization of all variables and arrays
	init()
	# Calling the user input function to get maximum no. of regions and tolerance
	(max_regions,tolerance) = user_input_fun()
	
		
		
	rerun = raw_input("\nPress 'q' to quit  : \n"+"Press Enter to run again: \n")
	if(rerun==""):
		main()
		
main()
	
