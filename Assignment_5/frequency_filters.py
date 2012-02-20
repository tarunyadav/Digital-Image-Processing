## 
 #          File: frequency_filters.py
 #          Author: Tarun Yadav
 #          Last Modified: Feburary 19, 2012
 #          Topic: applying Low pass, High pass and band pass frequency filters to the image
 #          Instructor: Dr. Anil Seth
 # ----------------------------------------------------------------
 #
 #          Script to apply various Frequncy Filters on an input image using fourier transforma 
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


# To change the sign of odd  i+j in matrix
def odd_sign_change(matrix,size):
	for i in range(0,size[0]):
		for j in range(0,size[1]):
			matrix[i][j] = ((-1)**(i+j))*matrix[i][j]
	return matrix
	
# open the image which is passed in argument
def init():
	global  MAX_FREQUENCY
	global image_array
	global FFT_image
	global Filtered_FFT
	global Filter
	global image_output
	global Default
	global Default_Lower
	global Default_Upper
	global cutoff_freq
	global size
	
	image = open(sys.argv[1])  
	image = image.convert('L')
	image_array = array(image);
	size = image_array.shape
	image_array = array(image_array,dtype=float)
	image_output = zeros((size[0],size[1]),dtype=complex)
	FFT_image = zeros((size[0],size[1]),dtype=complex)
	Filtered_FFT = zeros((size[0],size[1]),dtype=complex)
	Filter = zeros((size[0],size[1]),dtype=float)
	
	#image_array= odd_sign_change(image_array,size)
	FFT_image= fftshift(fft2(image_array))
	#MAX_FREQUENCY = image_array.max()
	MAX_FREQUENCY = max(size[0],size[1])/2

	print "Maximum Frequency is: "+str(MAX_FREQUENCY)
	
	#Default cutoff frequencies
	Default = .707*MAX_FREQUENCY;
	Default_Lower =  .293*MAX_FREQUENCY;
	Default_Upper =  .707*MAX_FREQUENCY;
	
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
	

#Function to apply Low Pass Filter image array
def LowPass(cutoff_freq):
	global image_output
	global FFT_image
	global Filtered_FFT
	global Filter

	for i in range(0,size[0],1):
		 for j in range(0,size[1],1):
		 		if (sqrt((i-size[0]/2)*(i-size[0]/2)+(j-size[1]/2)*(j-size[1]/2))<=cutoff_freq):
					Filtered_FFT[i][j]=FFT_image[i][j]
	image_output = ifft2(ifftshift(Filtered_FFT)).real
	
	#image_output = odd_sign_change(image_output,size)							
	image_output = image_output.clip(0,255)							
	print "\nApplying Low Pass Frequncy Filter  "+"...Done\n"
	output_name = '_Low_Pass_'+str(cutoff_freq)
	SaveToFile(output_name)			
			    		
#Function to apply High Pass Filter image array
def HighPass(cutoff_freq):
	global image_output
	global FFT_image
	global Filtered_FFT
	global Filter

	for i in range(0,size[0],1):
		for j in range(0,size[1],1):
		 		if (sqrt((i-size[0]/2)*(i-size[0]/2)+(j-size[1]/2)*(j-size[1]/2))>=cutoff_freq):
					Filtered_FFT[i][j]=FFT_image[i][j]

	image_output = ifft2(ifftshift(Filtered_FFT)).real			
	#image_output = odd_sign_change(image_output,size)
	image_output = image_output.clip(0,255)							
	print "\nApplying High Pass Frequncy Filter   "+"...Done\n"
	output_name = '_High_Pass_'+str(cutoff_freq)
	SaveToFile(output_name)
	
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
	filter_type = raw_input("\nPress 1 to apply Low Pass filter to the image : "+"\nPress 2 to apply High Pass Filter to the image :"+"\nPress 3 to apply Band Pass to the  image :"+"\nPress Enter to exit: \n")
	# Wrong input case	
	if(filter_type==""):
		exit()
	elif(filter_type != "1" and filter_type != "2" and filter_type != "3"):
		print "\nWrong Input, Please Press the correct one"
		return user_input_fun()
	else:
		return int(filter_type)

#function for taking cutoff frequency as input (supposed to be call in all filters)
def cutoff_freq_input():
	global cutoff_freq
	global MAX_FREQUENCY
	global Default
	global Default_Lower
	global Default_Upper
	cutoff_freq = raw_input("\nPress Enter for default cutoff frequency fraction [3dB(.707 of maximum)]: "+"\nType cutoff frequency fraction, if not default  : \n" )
	if(cutoff_freq==""):
		return Default
	else:
		return float(cutoff_freq)*MAX_FREQUENCY
		
#main function which will be run 
def main():		

	# initialization of all variables and arrays
	init()
	# Calling the user input function for type of image
	filter_type = user_input_fun()
	##LowPass Operator
	if (filter_type==1):
		LowPass(cutoff_freq_input())
		
	##HighPass Operator	
	elif (filter_type==2):	
		HighPass(cutoff_freq_input())

	##BandPass Operator
	elif(filter_type==3):
		print "Default cutoff frequency is [3dB(.707 of maximum)]:"
		cutoff_freq_lower = raw_input("\nType lower cutoff frequency fraction, if not default  : \n")
		cutoff_freq_upper = raw_input("\nType upper cutoff frequency fraction, if not default  : \n")
		if (cutoff_freq_lower==""):
			cutoff_freq_lower = Default_Lower
		if(cutoff_freq_upper==""):
			cutoff_freq_upper = Default_Upper

		BandPass(float(cutoff_freq_lower)*MAX_FREQUENCY,float(cutoff_freq_upper)*MAX_FREQUENCY)
	
	rerun = raw_input("\nPress 'q' to quit  : \n"+"Press Enter to run again: \n")
	if(rerun==""):
		main()
		
main()
	
