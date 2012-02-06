## 
 #          File: add_noise.py
 #          Author: Tarun Yadav
 #          Last Modified: Feburary 05, 2012
 #          Topic: Rotating mask filter and Efficient median filter
 #          Instructor: Dr. Anil Seth
 # ----------------------------------------------------------------
 #
 #          Script to filter images based on Rotating mask filter and Efficient median filter.
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

#Save the output file
def SaveToFile(output_name):
				    		
	# writing distance matrix to the output folder with _output.txt extension
	file_name= sys.argv[1].split('/')

	# check if output directory exists or not. if doesn't exists then create it
	if (os.path.exists(os.path.dirname(file_name[0]+'_Output/'))==False):
	    print "\nCreating Directory "+file_name[0]+"_Output ... Done"
	    os.mkdir(file_name[0]+'_Output',0777) 
	else:
	    print "\nOutput Directory "+file_name[0]+"_Output already exist... Done"		

	#convert array from float to uint8 for image display
	image_arr = image_array.astype('uint8')

	# convert from array to image
	image_mod=fromarray(image_array);
	print "Saving the Noise removed image to output directory..."
	# save the image in destination folder	
	image_mod.save(file_name[0]+'_Output/'+file_name[1].split('.')[0]+output_name+'.gif')
	print "Noise removed image is saved in output Directory with name: "+ file_name[1].split('.')[0]+output_name+'.gif ...Done\n'
	image_mod.show()

#Function to find median
def FindMedian(H,Median,pixel_less_med,half)
	if (pixel_less_med == half):
		return Median
	elif (pixel_less_med < half):
		Median = Median+1
		pixel_less_med = pixel_less_med + H[Median]
		return FindMedian(H,Median,pixel_less_med,half)
	elif(pixel_less_med>half):
		pixel_less_med = pixel_less_med - H[Median]
		Median = Median -1;
		return FindMedian(H,Median,pixel_less_med,half)
			
#Function to add gaussain noise to image array
def RotatingAverageMask():

	#Applying Gaussian noise to image array
	for i in range(0,size[0],1):
			    for j in range(0,size[1],2):
	    			U1 = rand();
	    			U2 = rand();
	    			factor = sqrt(-2.0*variance*log(U1))
			    	if (len(size)==2):
			    	    		image_array[i][j]=image_array[i][j] + int((factor*cos(2*pi*U2)) +mean)	
				    		if (j != size[1]-1 ):	
				    	    		image_array[i][j+1]=image_array[i][j+1] + int((factor*sin(2*pi*U2)) +mean)	
				if (len(size)==3):
						for k in range(0,size[2],1):
				    	    		image_array[i][j][k]=image_array[i][j][k] + int((factor*cos(2*pi*U2)) +mean)	
					    		if (j != size[1]-1 ):			    	    		
					    	    		image_array[i][j+1][k]=image_array[i][j+1][k] + int((factor*sin(2*pi*U2)) +mean)	
					    	    		
	# Changing >255 to 255 and <0 to 0					    	    		
	for i in range(0,size[0],1):
			    for j in range(0,size[1],1):
			    	if (len(size)==2):
				    	if (image_array[i][j]>255):
				    		image_array[i][j]=255
				    	if (image_array[i][j]<0):
				    		image_array[i][j]=0			
				elif(len(size)==3):
					for k in range(0,size[2],1):
				    		if (image_array[i][j][k]>255):
				    			image_array[i][j][k]=255
					    	if (image_array[i][j][k]<0):
					    		image_array[i][j][k]=0				    			
	
	print "\nGaussian noise is added with  mean: "+str(mean)+"and variance: "+str(variance)+"...Done\n"
	output_name = '_GaussainNoise_mean_'+str(mean)+'_variance_'+str(variance)+'_percent'
	SaveToFile(output_name)			
			    		
#Function to add Salt and pepper noise to image array
def EfficientMedianMask(N,M):
	
	for i in range(0,size[0],1):
			    Histogram = zeros(256,dtype=int)
			    pixel_less_med = 0		
			    Median=0
			    start_row=0
			    end_row=0
			    start_column=0
			    end_column=0
			    for j in range(0,size[1],1):

			    		if(i in range(0,(N/2)) or  i in range (size[0]-(N/2), size[0]-1) or j in range(0,(M/2) or j in range(size[1]-(M/2),size[1]-2))):
			    				start_row = min(-(N/2),0-i)
			    				end_row = min((N/2),size[0]-1-i)
			    				start_column = min(-(M/2),0-j)
			    				end_column = min((M/2),size[1]-1-j)
			    		else : 
							start_row=-(N/2)
							end_row=(N/2)+1
							start_column=-(M/2)
							end_column=(M/2)+1
							
					if (j!=0):
		    					for k in range(start_row,end_row+1,1):
		    						H[image_array[i+k][j+end_column]] = H[image_array[i+k][j+end_column]] + 1
		    						if (H[image_array[i+k][j+end_column]] < Median):
									pixel_less_med = pixel_less_med+1				
											
					Median = FindMedian(H,Median,pixel_less_med,N*M/2)
					H[image_array[i][j]] = Median
					
	    				if (j!=M-1):
		    					for k in range(start_row,end_row+1,1):
		    						H[image_array[i+k][j+start_column]] = H[image_array[i+k][j+start_column]] -1			    				
		    						if (H[image_array[i+k][j+end_column]] < Median):
									pixel_less_med = pixel_less_med -1 		
	
   	
	print "\nSalt and Pepper noise is added with "+str(int(actual_percent)) +" % ...Done\n"
	output_name = '_SaltAndPepperNoise_'+str(int(actual_percent))+'_percent'
	SaveToFile(output_name)
	

# input for type of noise that user want to add
def user_input_fun():
	filter_type = raw_input("\nPress 1 to apply Rotating Average Mask Filter on the image : "+"\nPress 2 to apply Efficient Median Filter on the image:"+"\nPress Enter to exit: \n")
	# Wrong input case	
	if(filter_type==""):
		exit()
	elif(filter_type != "1" and filter_type != "2"):
		print "\nWrong Input, Please type the correct one"
		return user_input_fun()
	else:
		return int(filter_type)

# Calling the user input function for noise type input
filter_type = user_input_fun();		

## Rotating Average Mask case	
if (filter_type==1):
	RotatingAverageMask()
##Efficient Median Mask case
elif(filter_type==2):
	EfficientMedianMask()


	
