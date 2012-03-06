## 
 #          File: frequency_filters.py
 #          Author: Tarun Yadav
 #          Last Modified: March 05, 2012
 #          Topic: Segmentation of Multispectral Image using Thresholding for each band spectrum
 #          Instructor: Dr. Anil Seth
 # ----------------------------------------------------------------
 #
 #          Script to find segments in a multispectral(colored) image, using thresholding technique
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
	global image_output_r	
	global image_output_g
	global image_output_b
	
	image = open(sys.argv[1])
	image_array = array(image);
	size = image_array.shape
	image_array = array(image_array,dtype=float)
	image_output = zeros((size[0],size[1]),dtype=float)
	image_output_r= zeros((size[0],size[1]),dtype=float)
	image_output_g= zeros((size[0],size[1]),dtype=float)
	image_output_b= zeros((size[0],size[1]),dtype=float)

def robert(image_array):
	image_arr = zeros((size[0],size[1]),dtype=float)
	for i in range(0,size[0]-1,1):
		 for j in range(0,size[1]-1,1):
				image_arr[i][j] =  abs(image_array[i][j]-image_array[i+1][j+1])+abs(image_array[i][j+1]-image_array[i+1][j])
										
	image_arr = image_arr.clip(0,255)							
	return image_arr
			    			
#Save the output file
def SaveToFile():
	global image_array
	global image_output			
	global image_output_r
	global image_output_g
	global image_output_b
	
	file_name= sys.argv[1].split('/')

	# check if output directory exists or not. if doesn't exists then create it
	if (os.path.exists(os.path.dirname(file_name[0]+'_Segmented/'))==False):
		    print "\nCreating Directory "+file_name[0]+"_Segmented ... Done"
		    os.mkdir(file_name[0]+'_Segmented',0777) 
	else:
		    print "\nOutput Directory "+file_name[0]+"_Segmented already exist... Done"
	    		
	if (os.path.exists(os.path.dirname(file_name[0]+'_Segmented/'+file_name[1].split('.')[0]+'_Segmented/'))==False):
		    print "\nCreating Directory "+file_name[0]+"_Segmented/"+file_name[1].split('.')[0]+"_Segmented ... Done"
		    os.mkdir(file_name[0]+"_Segmented/"+file_name[1].split('.')[0]+"_Segmented",0777) 
	else:
		    print "\nOutput Directory "+file_name[0]+"_Segmented/"+file_name[1].split('.')[0]+"_Segmented already exist... Done"		
		    

	if(image.mode =='L'):
		#convert array from float to uint8 for image display
		image_output = image_output.astype('uint8')
		# convert from array to image
		image_mod=fromarray(image_output);
		print "Saving the segmentation applied image to output directory..."
		# save the image in destination folder	
		image_mod.save(file_name[0]+'_Segmented/'+file_name[1].split('.')[0]+'_Segmented/'+file_name[1].split('.')[0]+'_Segmented.gif')
		print "Segmentation appled  image is saved in output Directory with name: "+ file_name[1].split('.')[0]+'_Segmented.gif   ...Done\n'
		
		image_mod.show()
	else:
				
		image_output_r_edge = robert(image_output_r)
		image_output_g_edge = robert(image_output_g)
		image_output_b_edge = robert(image_output_b)
		
		#convert array from float to uint8 for image display
		image_array = image_array.astype('uint8')
		image_output_r = image_output_r.astype('uint8')
		image_output_g = image_output_g.astype('uint8')
		image_output_b = image_output_b.astype('uint8')
		
		image_output_r_edge = image_output_r_edge.astype('uint8')
		image_output_g_edge = image_output_g_edge.astype('uint8')
		image_output_b_edge = image_output_b_edge.astype('uint8')
		
		for i in range(0,size[0]):
			for j in range(0,size[1]):
				image_output[i][j] = image_output_r_edge[i][j] or image_output_g_edge[i][j] or image_output_b_edge[i][j]
		# convert from array to image
		image_mod_r=fromarray(image_output_r);
		image_mod_g=fromarray(image_output_g);
		image_mod_b=fromarray(image_output_b);
		image_mod= fromarray(image_output);
		print "Saving the segmentation applied image to output directory..."
		# save the image in destination folder	
		image_mod_r.save(file_name[0]+'_Segmented/'+file_name[1].split('.')[0]+'_Segmented/'+file_name[1].split('.')[0]+'_Segmented_red.gif')
		print "Segmentation appled  image is saved in output Directory with name: "+ file_name[1].split('.')[0]+'_Segmented_red.gif   ...Done\n'
		image_mod_g.save(file_name[0]+'_Segmented/'+file_name[1].split('.')[0]+'_Segmented/'+file_name[1].split('.')[0]+'_Segmented_green.gif')
		print "Segmentation appled  image is saved in output Directory with name: "+ file_name[1].split('.')[0]+'_Segmented_green.gif   ...Done\n'
		image_mod_b.save(file_name[0]+'_Segmented/'+file_name[1].split('.')[0]+'_Segmented/'+file_name[1].split('.')[0]+'_Segmented_blue.gif')
		print "Segmentation appled  image is saved in output Directory with name: "+ file_name[1].split('.')[0]+'_Segmented_blue.gif   ...Done\n'
		image_mod.save(file_name[0]+'_Segmented/'+file_name[1].split('.')[0]+'_Segmented/'+file_name[1].split('.')[0]+'_Segmented_rgb.gif')
		print "Segmentation appled  image is saved in output Directory with name: "+ file_name[1].split('.')[0]+'_Segmented_rgb.gif   ...Done\n'
		
		import matplotlib.pyplot 
		plt.subplot(3,2,1)
		title('Original')
		plt.imshow(image_array)
		plt.subplot(3,2,3)
		title('RED component')
		plt.imshow(image_output_r,cmap=plt.cm.gray)
		plt.subplot(3,2,4)
		title('GREEN component')
		plt.imshow(image_output_g,cmap=plt.cm.gray)
		plt.subplot(3,2,5)
		title('BLUE component')
		plt.imshow(image_output_b,cmap=plt.cm.gray)
		plt.subplot(3,2,6)
		title('RED +GREEN+BLUE')
		plt.imshow(image_output,cmap=plt.cm.gray)
		plt.show()
		savefig(file_name[0]+'_Segmented/'+file_name[1].split('.')[0]+'_Segmented/'+file_name[1].split('.')[0]+'_Segmented_all')		

	
#Function to get segments for single spectral image
#@variable: image array to work with and for local maxima detection and 
#@return: threshold using iterative thresholding selction algorithm
def single_spectral_thresholding(image_array):
	T_prev=0
	u_b = (image_array[0][0]+image_array[0][size[1]-1]+image_array[size[0]-1][0]+image_array[size[0]-1][size[1]-1])
	u_o = (sum(image_array)-u_b)/((size[0]*size[1])-4)
	u_b = u_b/4.0
	T = (u_o + u_b)/2.0
	while(T!=T_prev):
			T_prev = T
			b=zeros((size[0],size[1]),dtype=float)
			c=zeros((size[0],size[1]),dtype=float)
			mask = (image_array>T_prev)
			b[mask]=1
			mask_neg= -mask
			c[mask_neg] =1
			u_o= sum(image_array*b)/sum(b)
			u_b = sum(image_array*c)/sum(c)
			T = (u_o+u_b)/2
	return T		  
	  		
#Function to get segments for multispectral image
def multi_spectral_thresholding():
	global image_output_r
	global image_output_g
	global image_output_b
	
	image_array_r = zeros((size[0],size[1]),dtype=float)
	image_array_g= zeros((size[0],size[1]),dtype=float)
	image_array_b = zeros((size[0],size[1]),dtype=float)

	for i in range(0,size[0]):
		for j in range(0,size[1]):
			image_array_r[i][j] = image_array[i][j][0]
 			image_array_g[i][j]= image_array[i][j][1]
		 	image_array_b[i][j] = image_array[i][j][2]

	threshold_r = single_spectral_thresholding(image_array_r)
	threshold_g = single_spectral_thresholding(image_array_g)
	threshold_b = single_spectral_thresholding(image_array_b)
	
	mask_r=(image_array_r>threshold_r)
	image_output_r[mask_r]=255
	mask_neg_r= -mask_r
	image_output_r[mask_neg_r]=0
	
	mask_g=(image_array_g>threshold_g)
	image_output_g[mask_g]=255
	mask_neg_g= - mask_g
	image_output_g[mask_neg_g]=0
	
	mask_b=(image_array_b>threshold_b)
	image_output_b[mask_b]=255
	mask_neg_b= - mask_b
	image_output_b[mask_neg_b]=0
		
		
	print "\nApplying RGB Segmentation to the image   "+"...Done\n"
	SaveToFile()
	

#main function which will be run 
def main():		

	# initialization of all variables and arrays
	init()
	maxima_frac=.5
	#For Gray Scale Image
	if(image.mode =='L'):
		threshold= single_spectral_thresholding(image_array)
		mask=(image_array>threshold)
		image_output[mask]=255
		mask_neg= -mask
		image_output[mask_neg]=0
	
		print "\nApplying Gray Scale Segmentation to the image   "+"...Done\n"
		SaveToFile()

	else:
		multi_spectral_thresholding()	
	rerun = raw_input("\nPress 'q' to quit  : \n"+"Press Enter to run again: \n")
	if(rerun==""):
		main()
		
main()
	
