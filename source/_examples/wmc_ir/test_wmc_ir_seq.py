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

print img_file
### Iterate FPF images
for x in img_file:
    
    print "File ", x.file_name
    
    ### Open SEQ movie, into a file object
    file_obj = wmcimg.ir.read_seq(x.path, fff_files_out_path = "", prefix = "")
    
    ### Open the first image
    img_fff_1 = wmcimg.ir.read_fff(file_obj[0].path)

    ### Open the second image
    img_fff_2 = wmcimg.ir.read_fff(file_obj[1].path)
    
    ### See mean
    print "Difference 1 2 mean ", np.mean(img_fff_1.image - img_fff_2.image)  
    
    