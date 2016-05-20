#!/usr/bin/python
import header ### Not neccesary in a normal running (just due to documentation purposes)
import numpy as np
import os
#!/usr/bin/python

### Load wmcimg library
import wmc_img_tools as wmc_img_tools

wmcimg = wmc_img_tools.load()

### Choose a folder
folder = r"../images"

### Crawl the folder
img_file = wmcimg.read_folder_list_images(folder, extNoPoint = "SEQ", prefix = "", max_recursive_level = 0, data = False)

### Choose the first seq file path
seq_file_path = img_file[0].path

### Load seq file into and object file
seq_obj = wmcimg.ir.load_seq_obj(seq_file_path)

### See total frames
print "Total frames", seq_obj.total_frames #, " len ",  len(seq_obj)
print "Actual frame", seq_obj.actual_frame

### Go to frame 1
seq_obj.actual_frame = 1
print "Actual frame", seq_obj.actual_frame

### Get fff object
img_fff_1 = seq_obj.fff_image

### Go to frame 2
seq_obj.actual_frame = 100
print "Actual frame", seq_obj.actual_frame

### Get fff object
img_fff_2 = seq_obj.fff_image    

print "Mean diffrentce btw two frams ", np.mean(img_fff_1.image - img_fff_2.image)

###Iterate
for ii in range(1,10):
    
    seq_obj.actual_frame = ii
    
    img_fff = seq_obj.fff_image
    
    print "Mean of freme ", seq_obj.actual_frame, " is ", np.mean(img_fff.image), " Kelvin"
        
    
    