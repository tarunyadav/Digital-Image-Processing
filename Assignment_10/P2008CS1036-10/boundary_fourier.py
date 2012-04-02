## 
 #          File: region_growing.py
 #          Author: Tarun Yadav
 #          Last Modified: April 2, 2012
 #          Topic: Find fourier of boundaries and redraw the filtered border
 #          Instructor: Dr. Anil Seth
 # ----------------------------------------------------------------
 #
 #          Script to find boundaries of regions and filtering high frequencey one and redraw the boundaries
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
import re
import string
sys.setrecursionlimit(2000)

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
	
	#image=image.filter(BLUR)
	image_array = array(image)
	size = image_array.shape
	if(gaussian_smoothing ==1):
		image_array=filters.gaussian_filter(image_array,3)	
	image_array = array(image_array,dtype=float)
	image_output = zeros((size[0],size[1]),dtype=float)
	#region_array to mark region # in for each pixel
	region_array = zeros((size[0],size[1]),dtype=float)
	#all_region_array = zeros((size[0],size[1]),dtype=float)
	#seed_array to mark  seed points for the image, initially all are 0 means no seed is there
	seed_array = zeros((size[0],size[1]),dtype=float)
	#to keep count for region no.
	region_no=1
	#image1 = fromarray(image_array)
	#image1.show()	
	
#Save the output file
def SaveToFile(output_name,t_init,region_no,fraction_cut):
	global image_output			
	global region_array
	global image_array
	global all_region_array
	
	t_end = time()
	
	file_name= sys.argv[1].split('/')
	# check if output directory exists or not. if doesn't exists then create it
	if (os.path.exists(os.path.dirname(file_name[0]+'_boundary_fourier/'))==False):
	    print "\nCreating Directory "+file_name[0]+"_boundary_fourier ... Done"
	    os.mkdir(file_name[0]+'_boundary_fourier',0777) 
	else:
	    print "\nOutput Directory "+file_name[0]+"_boundary_fourier already exist... Done"		

	#convert array from float to uint8 for image display
	image_output = image_output.astype('uint8')
	region_array = region_array.astype('uint8')				
	# convert from array to image
	image_mod=fromarray(image_output);
	print "Saving the region growing and boundary fourier applied image to output directory..."
	output_name = output_name + '_total_regions_'+str(region_no)+'_time_taken_' + str(t_end-t_init)+'_sec'
	# save the image in destination folder	
	image_mod.save(file_name[0]+'_boundary_fourier/'+file_name[1].split('.')[0]+output_name+'.gif')
	print "Output image is saved in output Directory with name: "+ file_name[1].split('.')[0]+output_name+'.gif   ...Done\n'
	
	#fd= os.open(file_name[0]+'_region_boundary/'+file_name[1].split('.')[0]+output_name+'.txt',os.O_RDWR|os.O_CREAT )
	#os.write(fd,'Normalized Chain Codes: \n')
	#os.write(fd,str(normalized_chain_codes))
	#os.write(fd,str('\n\n'))
	#os.write(fd,'Derivated Chain Codes: \n')
	#os.write(fd,str(derivated_chain_codes))
	#os.close(fd)
	print "----------------------------------------------------------------------------------------------------------------"
	print ("\nTotal no. of regions are  : "+ str(region_no))	
	print ("\nTotal time taken to run the Pogram is : "+str(t_end-t_init)+" seconds")
	print "----------------------------------------------------------------------------------------------------------------"
	import matplotlib.pyplot as plt
	plt.subplot(1,3,1)
	title('Original')
	plt.imshow(image_array)
	plt.subplot(1,3,2)
	title('Boundary')
	plt.imshow(region_array)
	plt.subplot(1,3,3)
	title('Frequecny Filtered with fraction cut '+str(fraction_cut))
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
	seed_array= seed_array+1
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
	
##Function to find new direction vector for the pixel and mark this pixel as boundary
#@parameter: starting coordinates, current coordinates, current region number, array of boundaries of regions, 4/8 neighbor approach
#@return: current pixels and new directon vector
def boundary_pixels(i_init,j_init,i,j,v,current_region,dir_count,boundaries,neighbors):
	global region_array
	global size
	i_old=i
	j_old=j
	if (neighbors==4):
		if(v==0 ):
			j=j+1
		elif (v==1):
			i=i-1
		elif(v==2):
			j=j-1
		elif (v==3):
			i=i+1
	else:
		if(v==0 or  v==1 or v==7 ):
			j=j+1
		if (v==1 or v==2 or v==3):
			i=i-1
		if(v==3 or v==4 or v==5):
			j=j-1
		if (v==5 or v==6 or v==7):
			i=i+1
	#stop condition when region loop is complete
	if(i==i_init and j==j_init):	
		if (neighbors==4):
			return (0,0,4,0)
		else:
			return (0,0,8,0)
	# condition when pixel doesn't belong to same region then change the direction vector
	elif ( i<0 or i>size[0]-1 or j<0 or j>size[1]-1 or region_array[i][j]!=current_region):
			return (i_old,j_old,mod(v+1,neighbors),dir_count+1)		
			
	#mark the pixel as boundary and find new direction vector(4/8 neighbor)	
	elif(region_array[i][j]==current_region):
		region_array[i][j]=255
		boundaries[current_region]=append(boundaries[current_region],complex(i,j))
		if(neighbors==4):
			return (i,j,mod(v+3,4),0)
		else:
			if(mod(v,2)==0):
				return (i,j,mod(v+7,8),0)
			else:
				return (i,j,mod(v+6,8),0)

##Function to detect boundary of all regions
#@parameter: number of total regions and 4/8 neighbor approach
#@return: boundaries pixels in complex form
def boundary_detection(region_no,neighbors):
	global region_array
	global size
	
	#boundaries=zeros((region_no+1,size[0]*size[1]/10),dtype=complex)
	boundaries=zeros(region_no+1,dtype=list)
	boundaries[0]=[0+0j]
	regions = zeros(region_no+1,dtype=int)
	
	for i in range(0,size[0],1):
		 for j in range(0,size[1],1):
		 	# For a new region start from here
			if(region_array[i][j]!=0 and region_array[i][j]!=255 and regions[region_array[i][j]]==0 ):	
				regions[region_array[i][j]]=1
				new_i=i
				new_j=j
				new_v=neighbors-2
				current_region = region_array[i][j]
				region_array[i][j]=255
				dir_count=1
				boundaries[current_region]=complex(i,j)
				while(True):
							(new_i,new_j,new_v,dir_count)=boundary_pixels(i,j,new_i,new_j,new_v,current_region,dir_count,boundaries,neighbors)
							
							if((dir_count==5 and neighbors==4) or (dir_count==9 and neighbors==8)):
								break									
							if((new_v==4 and neighbors==4) or (new_v==8 and neighbors==8) ):
								break
	return boundaries

def fft_filtering(boundaries,fraction_cut):
	for i in range(2,len(boundaries)):
		fft_boundary =fftshift(fft(boundaries[i]))
		#Filtereing our the fraction of frequecy according to the input given by the user	
		center= len(fft_boundary)/2
		pixel_cut = fraction_cut*len(fft_boundary)
		half_cut= int(pixel_cut)/2
		fft_boundary[:center-half_cut]=0
		fft_boundary[center+half_cut:]=0
		#inverse shift and inverse fft to get filtered bundaries
		boundaries[i]=ifft(ifftshift(fft_boundary))
	return boundaries	
#Function to initiate region going through seed points
#@parameters: tolerance value, smoothing or not, initial time when program started, neighbors, fraction which we want to cut 
#@return: calculate boundaries apply fft on it  and save in ouput folder
def region_detection(tolerance,gaussian_smoothing,t_init,neighbors,fraction_cut):
	global region_array
	global seed_array
	global image_output
	global size
	global region_no
	#global all_region_array
	print "Applying region growing to the image   "+" .........."
	for i in range(0,size[0],1):
		 for j in range(0,size[1],1):
			if(seed_array[i][j]==1):
				current_nbh = []
				seed_array[i][j]=0
				region_array[i][j]=region_no
				current_nbh.insert(0,(i,j))
				grow_the_region(current_nbh,tolerance,image_array[i][j],1.0)
				mask= (region_array==region_no)	
				if (sum(mask) <500):
							region_array[mask]=0;
				else:
							region_no=region_no+1

	print "Applying region growing to the image   "+" ...Done"
	region_no=region_no-1
	#all_region_array = region_array
	#Boundary detection
	print "Applying Boundary Detection to the image and finding chain codes  "+" ............"
	boundaries=boundary_detection(region_no,neighbors)		
	print "Applying Boundary Detection to the image and finding chain codes  "+" .....Done"
	#Fourier Transform and low frequnecy shifting to the center
	print "Applying FFT filter on Boundaries to the images for all the regions  "+" ............"
	boundaries = fft_filtering(boundaries,fraction_cut)
	#draw the filtered boundaries
	for i in range(1,len(boundaries)):
		for j in range(0,len(boundaries[i])):
			a=int(real(boundaries[i][j]))
			b=int(imag(boundaries[i][j]))
			if (a <0 or a>=size[0]or b<0 or b>=size[1]):	
				continue
			else:
				image_output[a][b]=255
	print "Applying FFT filter on Boundaries to the images for all the regions  "+" ......Done"
	
	region_array = region_array.clip(0,255)
	image_output = image_output.clip(0,255)	
	output_name = '_neighbors_'+str(neighbors)+'_tolerance_'+str(tolerance)+'_fraction_cut_'+str(fraction_cut)
	if (gaussian_smoothing==1):
		output_name = '_gaussian_smoothing_'+'_tolerance_'+str(tolerance)+'_fraction_cut_'+str(fraction_cut)
	
	SaveToFile(output_name,t_init,region_no,fraction_cut)	
	

# input for neighbor approach, gaussian smoothing,tolerance value for region detection and fraction which we wan to cut
def user_input_fun():
	neighbors = raw_input("\n Press 4 for 4-neighbor approach or 8 for 8-neighbor approach[Default 8(Press Enter)]:  \n")
	gaussian_smoothing = raw_input("\n Want to apply gaussian smoothing, type 1 for yes or 0 for no[Default NO(press Enter)]:  \n")
	tolerance = raw_input("\n Type tolerance for region sperating intensity(int) criteria[press Enter for Default (Default is 10)]: \n")
	fraction_cut=raw_input("\n Type percent of low Frequecy you want to have w.r.t. lowest one[example 2% means top 2% low frequecies will remain and all other will become 0][Default is 2(Press Enter)]:  \n ")
	if(neighbors==""):
		neighbors=8
	if (tolerance==""):
		tolerance=10
	if(gaussian_smoothing=="" ):
		gaussian_smoothing = 0
	if(fraction_cut=="" ):
		fraction_cut = 2		
	return float(gaussian_smoothing ),float(tolerance),int(neighbors),(float(fraction_cut)/100.0)
			

#main function which will be run 
def main():		
	t_init= time()
	# Calling the user input function to get maximum no. of regions and tolerance
	(gaussian_smoothing,tolerance,neighbors,fraction_cut) = user_input_fun()
	# initialization of all variables and arrays
	init(gaussian_smoothing)
	#calculation of seed points 
	calculate_seed_points()
	# call to region growing
	region_detection(tolerance,gaussian_smoothing,t_init,neighbors,fraction_cut)
	# in case to rerun the program		
	rerun = raw_input("\nPress 'q' to quit  : \n"+"Press Enter to run again: \n")
	if(rerun==""):
		main()
		
main()
	
