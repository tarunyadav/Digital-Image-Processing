## 
 #          File: add_noise.py
 #          Author: Tarun Yadav
 #          Last Modified: Feburary 04, 2012
 #          Topic: Adding Gaussian and salt and peeper noise to the image
 #          Instructor: Dr. Anil Seth
 # ----------------------------------------------------------------
 #
 #          Script to add gaussian and salt and pepper  noise  on an input images.
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
	if (os.path.exists(os.path.dirname(file_name[0]+'_Noise/'))==False):
	    print "\nCreating Directory "+file_name[0]+"_Noise ... Done"
	    os.mkdir(file_name[0]+'_Noise',0777) 
	else:
	    print "\nOutput Directory "+file_name[0]+"_Noise already exist... Done"		

	#convert array from float to uint8 for image display
	image_arr = image_array.astype('uint8')

	# convert from array to image
	image_mod=fromarray(image_array);
	print "Saving the Noise added image to output directory..."
	# save the image in destination folder	
	image_mod.save(file_name[0]+'_Noise/'+file_name[1].split('.')[0]+output_name+'.gif')
	print "Noisy image is saved in output Directory with name: "+ file_name[1].split('.')[0]+output_name+'.gif ...Done\n'
	image_mod.show()

#Function to add gaussain noise to image array
def GaussianNoise(mean,variance):

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
def SaltAndPepperNoise(percent_noise):
	boundary = 1.0 - (percent_noise/100.0)
	actual_percent =0;

	print "\nAdding Salt and Pepper Noise to image "+sys.argv[1]+"\nWait for some time..."
	for i in range(0,size[0],1):
			    for j in range(0,size[1],1):
			      	if (len(size)==2):
			    			random_value= 2.0*(rand()-1.0/2);
			    			if (random_value > boundary):
			    				image_array[i][j] = 255
			    				actual_percent = actual_percent+1
			    			elif(random_value<-boundary):
				    			image_array[i][j]=0
				    			actual_percent = actual_percent+1
				elif(len(size)==3):
					for k in range(0,size[2],1):
			    			random_value= 2.0*(rand()-1.0/2);					
			    			if (random_value > boundary):
			    				image_array[i][j] = 255
			    				actual_percent = actual_percent+1
			    			elif(random_value<-boundary):
				    			image_array[i][j]=0
				    			actual_percent = actual_percent+1
   	
   	actual_percent = (actual_percent*100.0)/(size[0]*size[1])
   	
	print "\nSalt and Pepper noise is added with "+str(int(actual_percent)) +" % ...Done\n"
	output_name = '_SaltAndPepperNoise_'+str(int(actual_percent))+'_percent'
	SaveToFile(output_name)
	

# input for type of noise that user want to add
def user_input_fun():
	noise_type = raw_input("\nPress 1 to add 'Gaussian' noise to image : "+"\nPress 2 to add 'salt and pepper noise' to image:"+"\nPress Enter to exit: \n")
	# Wrong input case	
	if(noise_type==""):
		exit()
	elif(noise_type != "1" and noise_type != "2"):
		print "\nWrong Input, Please type the correct one"
		return user_input_fun()
	else:
		return int(noise_type)

# Calling the user input function for noise type input
noise_type = user_input_fun();		
##Gaussian Noise case	
if (noise_type==1):
	mean = float(raw_input("\nType 'mean' for Gaussain Noise: "))
	variance = float(raw_input("\nType 'variance' for Gaussain Noise: "))	
	GaussianNoise(mean,variance)
##Salt and Pepper Noise case
elif(noise_type==2):
	percent_noise = float(raw_input("\nType percent of salt and pepper noise that you want to add: "))
	SaltAndPepperNoise(percent_noise)


	
