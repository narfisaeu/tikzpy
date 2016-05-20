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
img_file = wmcimg.read_folder_list_images(folder, extNoPoint = "FFF", prefix = "", max_recursive_level = 0, data = False)

print img_file
### Iterate FPF images
for x in img_file:
    
    print "File ", x.file_name
    
    ### Open FFF image, into object img_fpf
    img_fff = wmcimg.ir.read_fff(x.path)
    
    ### See mean
    print "Mean 1 ", np.mean(img_fff.image)
    
    ### Convert fff to fpf
    img_fpf = wmcimg.ir.convert_fff_to_fpf(img_fff)
    
    ### Add one degree
    img_fpf.image[:] = img_fpf.image[:] + 1.
    
    ### Save FPF image
    new_file = x.path_noExt + "_out.FPF"
    
    wmcimg.ir.save_fpf(img_fpf, new_file)
    
    ### Open new FPF image
    img_fpf = wmcimg.ir.read_fpf(new_file)

    ### See mean
    print "Mean 2 ", np.mean(img_fpf.image)    
    
    #Delete out
    if os.path.isfile(new_file):
        os.remove(new_file)
    