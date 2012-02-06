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
image_arr = ones((size[0],size[1]),dtype=float)

#Save the output file
def SaveToFile(output_name,image_arr):
				    		
	# writing distance matrix to the output folder with _output.txt extension
	file_name= sys.argv[1].split('/')

	# check if output directory exists or not. if doesn't exists then create it
	if (os.path.exists(os.path.dirname(file_name[0]+'_Output/'))==False):
	    print "\nCreating Directory "+file_name[0]+"_Output ... Done"
	    os.mkdir(file_name[0]+'_Output',0777) 
	else:
	    print "\nOutput Directory "+file_name[0]+"_Output already exist... Done"		

	#convert array from float to uint8 for image display
	image_arr_mod = image_arr.astype('uint8')

	# convert from array to image
	image_mod=fromarray(image_arr_mod);
	print "Saving the Noise removed image to output directory..."
	# save the image in destination folder	
	image_mod.save(file_name[0]+'_Output/'+file_name[1].split('.')[0]+output_name+'.gif')
	print "Noise removed image is saved in output Directory with name: "+ file_name[1].split('.')[0]+output_name+'.gif ...Done\n'
	image_mod.show()

#Function to find median
def FindMedian(H,Median,pixel_less_med,half):
	if (pixel_less_med == half):
		return Median,pixel_less_med
	elif (pixel_less_med < half):
		Median = Median+1
		pixel_less_med = pixel_less_med + H[Median]
		return FindMedian(H,Median,pixel_less_med,half)
	elif(pixel_less_med>half):
		pixel_less_med = pixel_less_med - H[Median]
		if(pixel_less_med<half):
			pixel_less_med = pixel_less_med + H[Median]
			return Median,pixel_less_med
		else:
			Median = Median -1
			return FindMedian(H,Median,pixel_less_med,half)
			
#Function to apply average mask filter to image
def RotatingAverageMask(N,M):
	mean_array = ones((size[0],size[1]),dtype=float)
	variance_array = ones((size[0],size[1]),dtype=float)
	
	for i in range(0,size[0],1):
			 for j in range(0,size[1],1):
			    		if(  i in range (size[0]-(N-1), size[0]) or j in range(size[1]-(M-1),size[1])):
			    				start_row = 0
			    				end_row = min(N-1,size[0]-1-i)
			    				start_column = 0
			    				end_column = min(M-1,size[1]-1-j)
			    		else : 
							start_row=0
							end_row=N-1
							start_column=0
							end_column=M-1			

					window = zeros(1,dtype=float)
					for k in range(start_row,end_row+1,1):
						window = append(window,image_array[i+k][j+start_column:j+end_column+1])
					mean_array[i][j] = mean(window)
					variance_array[i][j] = var(window)			
					
	New_N = 2*(N-1)+1
	New_M = 2*(M-1)+1
	for i in range(0,size[0],1):
			 for j in range(0,size[1],1):
			    		if(i in range(0,(New_N/2)) or  i in range (size[0]-(New_N/2), size[0]) or j in range(0,(New_M/2)) or j in range(size[1]-(New_M/2),size[1])):
			    				start_row = max(-(New_N/2),0-i)
			    				end_row = min((New_N/2),size[0]-1-i)
			    				start_column = max(-(New_M/2),0-j)
			    				end_column = min((New_M/2),size[1]-1-j)
			    		else : 
							start_row=-(N/2)
							end_row=(N/2)
							start_column=-(M/2)
							end_column=(M/2)			    	
					min_variance=10000000;
					for m in range(i+start_row,i+1,1):
						for n in range(j+start_column,j+1,1):
							if (variance_array[m][n]<min_variance):
								min_variance = variance_array[m][n]
								min_variance_index = (m,n)
					image_arr[i][j] = mean_array[min_variance_index[0]][min_variance_index[1]] 
					
	print "\nRotating Average Mask Filter is applied to image  ...Done\n"
	output_name = '_RotatingAverageFilter_'+str(N)+'X'+str(M)
	SaveToFile(output_name,image_arr)
			    		
#Function to add Salt and pepper noise to image array
def EfficientMedianMask(N,M):
	
	for i in range(0,size[0],1):
			    Histogram = zeros(256,dtype=int)
			    pixel_less_med = 0		
			    Median=128
			    start_row=0
			    end_row=0
			    start_column=0
			    end_column=0
			    for j in range(0,size[1],1):

			    		if(i in range(0,(N/2)) or  i in range (size[0]-(N/2), size[0]) or j in range(0,(M/2)) or j in range(size[1]-(M/2),size[1])):
			    				start_row = max(-(N/2),0-i)
			    				end_row = min((N/2),size[0]-1-i)
			    				start_column = max(-(M/2),0-j)
			    				end_column = min((M/2),size[1]-1-j)
			    		else : 
							start_row=-(N/2)
							end_row=(N/2)
							start_column=-(M/2)
							end_column=(M/2)

					if (j==0):
							for m in range(start_row,end_row+1,1):
								for n in range(start_column,end_column+1,1):
										Histogram[image_array[i+m][j+n]] = Histogram[image_array[i+m][j+n]] +1
										if (image_array[i+m][j+n] <= Median):
											pixel_less_med = pixel_less_med+1	
					elif (0<j<size[1]-(M/2)):
		    					for k in range(start_row,end_row+1,1):
		    						Histogram[image_array[i+k][j+end_column]] = Histogram[image_array[i+k][j+end_column]] + 1
		    						if (image_array[i+k][j+end_column] <= Median):
									pixel_less_med = pixel_less_med+1				
					Median,pixel_less_med = FindMedian(Histogram,Median,pixel_less_med,(end_row-start_row+1)*(end_column-start_column+1)/2)
					image_arr[i][j] = Median
	    				if ((M/2)-1<j<size[1]):
		    					for k in range(start_row,end_row+1,1):
		    						Histogram[image_array[i+k][j+start_column]] = Histogram[image_array[i+k][j+start_column]] -1			    				
		    						if (image_array[i+k][j+start_column] <= Median):
									pixel_less_med = pixel_less_med -1 		
	
   	
	print "\nEfficient Median Filter is applied to image  ...Done\n"
	output_name = '_MedianFilter_'+str(N)+'X'+str(M)
	SaveToFile(output_name,image_arr)
	

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
	row_size = int(raw_input("\nType 'height' of window[int]: "))
	column_size = int(raw_input("\nType 'width of window[int]': "))	
	RotatingAverageMask(row_size,column_size)
##Efficient Median Mask case
elif(filter_type==2):
	row_size = int(raw_input("\nType 'height' of window[int]: "))
	column_size = int(raw_input("\nType 'width' of window[int]: "))	
	EfficientMedianMask(row_size,column_size)


	
