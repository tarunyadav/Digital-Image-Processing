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
	global seed_array
	global region_no
	global count
	count =0
	image = open(sys.argv[1])
	image = image.convert('L')
	image.show()
	image_array = array(image);
	size = image_array.shape
	image_array = array(image_array,dtype=float)
	image_output = zeros((size[0],size[1]),dtype=float)
	#region_array to mark region # in for each pixel
	region_array = zeros((size[0],size[1]),dtype=float)
	#seed_array to mark  seed points for the image, initially all are 0 means no seed is there
	seed_array = zeros((size[0],size[1]),dtype=float)
	#to keep count for region no.
	region_no=1
	
#Save the output file
def SaveToFile(output_name):
	global image_output			
	
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
	# save the image in destination folder	
	image_mod.save(file_name[0]+'_region_growing/'+file_name[1].split('.')[0]+output_name+'.gif')
	print "Region Growing applied  image is saved in output Directory with name: "+ file_name[1].split('.')[0]+output_name+'.gif   ...Done\n'
	import matplotlib.pyplot as plt
	plt.imshow(image_output)
	plt.show()
	#image_mod.show()
	

#Function to get seed points for the image
#@parameters: array having 0 at all indices
#@return: array having 1 at seed point indices
def calculate_seed_points():
	global image_array
	global seed_array
	#TODO: Here write some good algorithm to find out seed points for the given image	

	seed_array= seed_array+1
	return seed_array
	
def  grow_the_region(current_nbh,tolerance,total_intensity,number):
	global region_array
	global seed_array
	global image_array
	global region_no
	#global count
	#count = count +1 
	#print count
	#mask = (region_array==region_no)
	#avg_intensity = sum(region_array[mask])/sum(mask)
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
	
	
def region_growing(tolerance):
	global region_array
	global seed_array
	global image_output
	global size
	global region_no
	
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
			
	print ("Total no. of regions are  : "+ str(region_no)+"\n")	
	image_output=region_array
	image_output = image_output.clip(0,255)	
	print "\nApplying region growing to the image   "+" ...Done\n"
	output_name = '_tolerance_'+str(tolerance)
	SaveToFile(output_name)	
	

# input for type of edge that user wants to detect
def user_input_fun():
	max_regions = raw_input("\n Type maximum no. of significant regions(int), you want to see [press Enter for default(all regions)]: \n")
	tolerance = raw_input("\n Type tolerance for region sperating intensity(int) criteria[press Enter for Default (Default is 10)]: \n")
	if (tolerance==""):
		tolerance=10	
	return float(max_regions),float(tolerance) 
			

#main function which will be run 
def main():		

	# initialization of all variables and arrays
	init()
	# Calling the user input function to get maximum no. of regions and tolerance
	(max_regions,tolerance) = user_input_fun()
	calculate_seed_points()
	region_growing(tolerance)
			
	rerun = raw_input("\nPress 'q' to quit  : \n"+"Press Enter to run again: \n")
	if(rerun==""):
		main()
		
main()
	
