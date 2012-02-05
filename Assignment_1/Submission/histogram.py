## 
 #          File: histogram.py
 #          Author: Tarun Yadav
 #          Last Modified: January 24, 2012
 #          Topic: Histogram for Images
 #          Instructor: Dr. Anil Seth
 # ----------------------------------------------------------------
 #
 #          Script to run algorithm on an input images.
##


from os import *
from sys import *
from scipy import *
from numpy import *
from Image import *
from pylab import *

# open the images passed as agrument
image = open(sys.argv[1])
size = image.size
image_arr = array(image);

#initialization of histogram matrix
# Y axis in histogram
Frequency = zeros(256,dtype=int32)
# X axis is Intensity
Intensity = range(0,256)

# calculate # of pixel for a particular intensity
if (len(size)==2):
    for i in range(0,size[1],1):
        for j in range(0,size[0],1):
            intensity_val = image_arr[i][j]
            Frequency[intensity_val]= Frequency[intensity_val]+1
else:
    for i in range(0,size[1],1):
        for j in range(0,size[0],1):
            for k in range(0,size[2],1):
                intensity_val = image_arr[i][j][k]
                Frequency[intensity_val]= Frequency[intensity_val]+1
# Plotting the histogram and saving it to output folder with _histogram.png extension
plot(Intensity,Frequency,label='Histogram')
file_name= sys.argv[1].split('/')
xlabel('Intensity --->')
ylabel('No. of pixels --->')
title('Image Histogram for '+ file_name[1])


# check if output directory exists or not. if doesn't exists then create it
if (os.path.exists(os.path.dirname(file_name[0]+'_histogram/'))==False):
    os.mkdir(file_name[0]+'_histogram',0777)

#if output file exists then delete it
output_file_name = file_name[0]+'_histogram/'+file_name[1].split('.')[0]+'_histogram'
if (os.path.exists(output_file_name)==True):
    os.remove(output_file_name)

#save plot in output directory     
savefig(output_file_name)
show()





