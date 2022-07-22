#!/usr/bin/python

### Load wmcimg library
import tikzpy.files_crawl as libfile

files = libfile.load_obj_files()

### Choose a folder
folder = r"../tikzpy_shapes"

### Crawl the folder
file_obj1 = libfile.read_folder_list_files(folder, "png", prefix = "test_shp_f", max_recursive_level = 0, data = False, case_sensitive = False)
print( file_obj1)

### Crawl the folder for prefix bird
file_obj2 = libfile.read_folder_list_files(folder, "png", prefix = "test_shp_c", max_recursive_level = 0, data = False, case_sensitive = False)

print( file_obj2)

### Add the objects
file_obj3 = file_obj1 + file_obj2

print( file_obj3)

### Print indexed folders
print( file_obj3.folders)

### Iterate paths
for x in file_obj3:

    print( x.path)

### Object from zero
file_obj4 = libfile.load_obj_files()

### Add single path
path = r"../tikzpy_shapes/test_shp_addpto.tikz.png"

### If the file does not exist will not be add
idx = file_obj4.set_by_path(path)

if idx < 0:
    print( "If the file does not exist will not be add: %s" % file_obj4[idx].path)
else:
    print( "If the file exist will be add: %s" % file_obj4[idx].path)

### Add single path
path = r"../tikzpy_shapes/test_shp_addpto.tikz.png"

### If the file exist will be add
idx = file_obj4.set_by_path(path)
if idx < 0:
    print( "If the file does not exist will not be add: %s" % file_obj4[idx].path)
else:
    print( "If the file exist will be add: %s" % file_obj4[idx].path)

print( file_obj4)

### Print indexed folders
print( file_obj3.folders)
