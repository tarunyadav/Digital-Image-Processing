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
from ImageFilter import *
import scipy.ndimage.filters as filters
from time import *

# open the image which is passed in argument
def init(gaussian_smoothing):
	global image
	global image_array
	global size
	global image_output
	global region_array
	global seed_array
	global region_no
	
	image = open(sys.argv[1])
	image = image.convert('L')
	
	#image.show()
	#image=image.filter(BLUR)
	image_array = array(image)
	size = image_array.shape
	if(gaussian_smoothing ==1):
		image_array=filters.gaussian_filter(image_array,3)	
	image_array = array(image_array,dtype=float)
	image_output = zeros((size[0],size[1]),dtype=float)
	#region_array to mark region # in for each pixel
	region_array = zeros((size[0],size[1]),dtype=float)
	#seed_array to mark  seed points for the image, initially all are 0 means no seed is there
	seed_array = zeros((size[0],size[1]),dtype=float)
	#to keep count for region no.
	region_no=1
	
#Save the output file
def SaveToFile(output_name,t_init,region_no):
	global image_output			
	
	t_end = time()
	
	file_name= sys.argv[1].split('/')
	# check if output directory exists or not. if doesn't exists then create it
	if (os.path.exists(os.path.dirname(file_name[0]+'_region_growing/'))==False):
	    print "\nCreating Directory "+file_name[0]+"_region_growing ... Done"
	    os.mkdir(file_name[0]+'_region_growing',0777) 
	else:
	    print "\nOutput Directory "+file_name[0]+"_region_growing already exist... Done"		

	#convert array from float to uint8 for image display
	image_output = image_output.astype('uint8')
	
				
	# convert from array to image
	image_mod=fromarray(image_output);
	print "Saving the region growing applied image to output directory..."
	output_name = output_name + '_total_regions_'+str(region_no)+'_time_taken_' + str(t_end-t_init)+'_sec'
	# save the image in destination folder	
	image_mod.save(file_name[0]+'_region_growing/'+file_name[1].split('.')[0]+output_name+'.gif')
	print "Output image is saved in output Directory with name: "+ file_name[1].split('.')[0]+output_name+'.gif   ...Done\n'
	print "----------------------------------------------------------------------------------------------------------------"
	print ("\nTotal no. of regions are  : "+ str(region_no))	
	print ("\nTotal time taken to run the Pogram is : "+str(t_end-t_init)+" seconds")
	print "----------------------------------------------------------------------------------------------------------------"
	import matplotlib.pyplot as plt
	plt.imshow(image_output)
	plt.show()
	
	#image_mod.show()
	

#Function to get seed points for the image
#@parameters: array having 0 at all indices
#@return: array having 1 at seed point indices
def calculate_seed_points():
	global image
	global image_array
	global seed_array
	#TODO: Here write some good algorithm to find out seed points for the given image
	#This one is fine but no so good	

	seed_array= seed_array+1
	histogram = image.histogram()
	neighborhood_size=5
	data_max = filters.maximum_filter(histogram,neighborhood_size)
	maxima = (histogram == data_max)
	intensity = range(0,256)
	seed_list=[]
	for i in range(0,256):
		if maxima[i]==True:
			seed_list.append(i)
	mask = zeros((size[0],size[1]),dtype=bool)
	for x in iter(seed_list):
		mask=mask+(seed_array == x)
	
	seed_array[mask] = 2
	
	return seed_array
	
#Function to grow the region for given queue of neighbors
#@parameters: queue of neighbors, tolerance value for region merging, total intensity of region, no. of pixels in the region
#@return: recursively call itself for next neighbors
def  grow_the_region(current_nbh,tolerance,total_intensity,number):
	global region_array
	global seed_array
	global image_array
	global region_no
	
	avg_intensity = total_intensity/number
		
	until = len(current_nbh)
	if(until ==0):
		return
	for k in range(0,until):
		(i,j)=current_nbh.pop()
		#TODO:it is computation overhead just for 1 pixel wide boundary, so we can remove it.
		if(i==0 and j==0):
				p=i; q=i+1; r=j; s=j+1
		elif(i==size[0]-1 and j==size[1]-1):
				p=i-1; q=i; r=j-1; s=j
		elif(i==0 and j==size[1]-1):
				p=i; q=i+1; r=j-1; s=j
		elif(i==size[0]-1 and j==0):
				p=i-1; q=i; r=j; s=j+1
		elif(i==0):
				p=i; q=i+1; r=j-1; s=j+1
		elif(i==size[0]-1):
				p=i-1; q=i; r=j-1; s=j+1
		elif(j==0):
				p=i-1; q=i+1; r=j; s=j+1
		elif(j==size[1]-1):
				p=i-1; q=i+1; r=j-1; s=j
		else:
				p=i-1; q=i+1; r=j-1; s=j+1
		
		
		for m in range(p,q+1):
			for n in range(r,s+1):
				#if(region_array[m][n]==0 and abs(image_array[i][j]-image_array[m][n]) < tolerance):				
				if(region_array[m][n]==0 and abs(avg_intensity-image_array[m][n]) < tolerance):
				 	region_array[m][n]=region_no
				 	seed_array[m][n]=0
				 	total_intensity = total_intensity+image_array[m][n]
				 	number = number +1.0
				 	current_nbh.insert(0,(m,n))
	grow_the_region(current_nbh,tolerance,total_intensity,number)
	
	
#Function to initiate region going through seed points
#@parameters: tolerance value, seed_array is global so need for this parameter
#@return: calculate regions and save in ouput folder
def region_growing(tolerance,gaussian_smoothing,t_init):
	global region_array
	global seed_array
	global image_output
	global size
	global region_no

	for i in range(0,size[0],1):
		 for j in range(0,size[1],1):
			if(seed_array[i][j]==2):
				current_nbh = []
				seed_array[i][j]=0
				region_array[i][j]=region_no
				current_nbh.insert(0,(i,j))
				grow_the_region(current_nbh,tolerance,image_array[i][j],1.0)
				#print ("region no. : "+ str(region_no)+"\n")			
				region_no=region_no+1	
				
	for i in range(0,size[0],1):
		 for j in range(0,size[1],1):
			if(seed_array[i][j]==1):
				current_nbh = []
				seed_array[i][j]=0
				region_array[i][j]=region_no
				current_nbh.insert(0,(i,j))
				grow_the_region(current_nbh,tolerance,image_array[i][j],1.0)
				#print ("region no. : "+ str(region_no)+"\n")			
				region_no=region_no+1
			
	
	image_output=region_array
	image_output = image_output.clip(0,255)	
	print "Applying region growing to the image   "+" ...Done"
	output_name = '_tolerance_'+str(tolerance)
	if (gaussian_smoothing==1):
		output_name = '_gaussian_smoothing'+'_tolerance_'+str(tolerance)
	
	SaveToFile(output_name,t_init,region_no)	
	

# input for maximum region showing and tolerance value
def user_input_fun():
	gaussian_smoothing = raw_input("\n Want to apply gaussian smoothing, type 1 for yes or 0 for no[Default YES(press Enter)]:  \n")
	#max_regions = raw_input("\n Type maximum no. of significant regions(int), you want to see [press Enter for default(all regions)]: \n")
	tolerance = raw_input("\n Type tolerance for region sperating intensity(int) criteria[press Enter for Default (Default is 10)]: \n")
	if (tolerance==""):
		tolerance=10
	if(gaussian_smoothing=="" ):
		gaussian_smoothing = 1
			
	return float(gaussian_smoothing ),float(tolerance)
			

#main function which will be run 
def main():		
	t_init= time()
	# Calling the user input function to get maximum no. of regions and tolerance
	(gaussian_smoothing,tolerance) = user_input_fun()
	# initialization of all variables and arrays
	init(gaussian_smoothing)
	#calculation of seed points 
	calculate_seed_points()
	# call to region growing
	region_growing(tolerance,gaussian_smoothing,t_init)
	
	# in case to rerun the program		
	rerun = raw_input("\nPress 'q' to quit  : \n"+"Press Enter to run again: \n")
	if(rerun==""):
		main()
		
main()
	
