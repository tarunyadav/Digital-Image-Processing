## 
 #          File: frequency_filters.py
 #          Author: Tarun Yadav
 #          Last Modified: March 10, 2012
 #          Topic: Hough transformation for finding straight line
 #          Instructor: Dr. Anil Seth
 # -----------------------------------------------------------------------------------------------------------------------------------
 #
 #          Script to apply hough transformation and finding straight line with local maxima approach
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
import scipy.ndimage.filters as filters

# open the image which is passed in argument
def init():
	global image_array
	global image_output
	global size
	
	image = open(sys.argv[1])  
	image = image.convert('L')
	image_array = array(image);
	size = image_array.shape
	image_array = are brightest in their neighborhood (here 10 * 10 pixels)ray(image_array,dtype=float)
	image_output = zeros((size[0],size[1]),dtype=float)
	
	
#Save the output file
def SaveToFile(output_name):
	global image_output			

	file_name= sys.argv[1].split('/')
	# check if output directory exists or not. if doesn't exists then create it
	if (os.path.exists(os.path.dirname(file_name[0]+'_Hough_Transformed/'))==False):
	    print "\nCreating Directory "+file_name[0]+"_Hough_Transformed ... Done"
	    os.mkdir(file_name[0]+'_Hough_Transformed',0777) 
	else:
	    print "\nOutput Directory "+file_name[0]+"_Hough_Transformed already exist... Done"		

	#convert array from float to uint8 for image display
	image_output = image_output.astype('uint8')
	
	# convert from array to image
	image_mod=fromarray(image_output);
	print "Saving the filter applied image to output directory..."
	# save the image in destination folder	
	image_mod.save(file_name[0]+'_Hough_Transformed/'+file_name[1].split('.')[0]+output_name+'.gif')
	print "Hough Transformation to applied  image is saved in output Directory with name: "+ file_name[1].split('.')[0]+output_name+'.gif   ...Done\n'
	#image.show()
	image_mod.show()
	
#Function to roberts operator for edge detection	
def robert():
	global image_array
	image_arr = zeros((size[0],size[1]),dtype=float)
	for i in range(0,size[0]-1,1):
		 for j in range(0,size[1]-1,1):
				image_arr[i][j] =  abs(image_array[i][j]-image_array[i+1][j+1])+abs(image_array[i][j+1]-image_array[i+1][j])
										
	image_arr = image_arr.clip(0,255)							
	return image_arr
			    			
#Function to apply hough transformation
#@paramter: steps for theta and r
#@return: Hough array containg votes in r-theta space
def Hough_Transformation(edge_image_array,delta_theta,delta_r):
#	global image_array
	
	thetas = range(-90,90+round(delta_theta),round(delta_theta))
	rs = range(0,sqrt(size[0]*size[0]+size[1]*size[1])+delta_r, delta_r )
	Hough = zeros((len(rs),len(thetas)),dtype=float)
	
#	edge_image_flat= edge_image_array.flat 
#	x  = range(0,size[1])
#	y = range(0,size[0])
#	y= repeat(y,size[1])
#	int i=0;
#	while (i<size[0]):
#		x = append(x,x)
#		i++
#	thetas = range(-90,90+round(delta_theta),round(delta_theta))
#	sine = sin(thetas*pi/180))
#	cosine = cos(thetas*pi/180)
#	r = transpose(edge_image_flat*x)*cosines + transpose(edge_image_array*y)*sines
#	Hough = zeros((len(thetas),len(r)),dtype=float)
#	for x in thetas:
#			Hough[x][round(r[:][x])] = Hough[x][round(r[:][x])]+1

	for i in range(0,size[0]):
		for j in range(0,size[1]):
			if edge_image_array[i][j]==0:
				continue
			else:
				for theta in thetas:
					r = i*cos(theta*pi/180) + j*sin(theta*pi/180)
					Hough[r][theta]++;
	return Hough
			    		
#Function to detect local maximas in given r-theta space array
#@paramter:Hough array with votes for r-theta space
#@return : points of maximas in r-theta space, bool r-theta space matrix where all local maximas are true
def Maxima_Detection(Hough,neighborhood):
	
	maximas = filters.maximun_filters(Hough,5)
	local_maximas = (Hough==maximas)
	
	return local_maximas

#Function to draw the straigt lines of maxima on the image
#@parameter: matrix of r-theta space where all local maximas are true
#@return: No return just draw all the straight lines got from hough transformations
def Draw(maximas):
	global image
	global image_output
	
	maximas_size = maximas.shape
	draw = ImageDraw.Draw(image)
	start_x=0;start_y=0
	end_x=0;end_y=0
	for r in range(0,maximas_size[0]):
		for theta in range(0,maximas_size[1]):
			if (maximas[r][theta] == TRUE):
				if ((r/sin(theta)>size[0]-1):
					start_y = size[0]-1
					start_x = r-(start_y*sin(theta))
				else:
					start_y = r/sin(theta)
					start_x = 0
				if ((r/cos(theta)>size[1]-1):
					end_x = size[1]-1
					end_y = r-(start_x*cos(theta))
				else:
					end_x = r/cos(theta)
					end_y = 0
				draw.line([(start_x,start_y),(end_x,end_y)])
	image_output = array(image)
	print "\nApplying Hough Transformation   "+"...Done\n"
	output_name = '_hough_transformation_'
	SaveToFile(output_name)
				
# input for steps of theta and r for r-theta space
def user_input_fun():
	delta_theta = raw_input("\n Type step theta (delta theta) for r-theta space : \n")
	delta_r = raw_input("\n Type step r (delta r) for r-theta space : \n")
	neighborhood = raw_input("\n Type neighborhood size for local maxima detection for r-theta space : \n")
	# Exit case	
	if(delta_theta=="" or delta_theta=="" or neighborhood==""):
		exit()
	else:
		return float(delta_theta),float(delta_r),neighborhood

		
#main function which will be run 
def main():		

	# initialization of all variables and arrays
	init()
	# Calling the user input function for type of image
	(delta_theta,delta_r,neighborhood) = user_input_fun()
	edge_image_array = roberts()
	Hough = Hough_Transformation(edge_image_array,delta_theta,delta_r)
	maximas = Maxima_Detection(Hough,neighborhood)
	Draw(maximas);	
	rerun = raw_input("\nPress 'q' to quit  : \n"+"Press Enter to run again: \n")
	if(rerun==""):
		main()
		
main()
	
	
