# python3

import os

import tikzpy.files_crawl as libfile


llist = []

llist.append("files_crawl")
llist.append("drawings")
llist.append("tikzpy")
llist.append("tikzpy_assembly")
llist.append("tikzpy_labels")
llist.append("tikzpy_points")
llist.append("tikzpy_shapes")
llist.append("tikzpy_groups")
llist.append("tikzpy_colors")
llist.append("tikzpy_plots")

"""
llist.append("files_crawl")
llist.append("drawings")
llist.append("tikzpy")
llist.append("tikzpy_assembly")
llist.append("tikzpy_labels")
llist.append("tikzpy_points")
llist.append("tikzpy_shapes")
llist.append("tikzpy_groups")
llist.append("tikzpy_colors")
llist.append("tikzpy_plots")
"""

filess = libfile.load_obj_files()

### Find python files
for f in llist:

    txt = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f
    )

    filess= filess + libfile.read_folder_list_files(txt, "py", prefix = "test", max_recursive_level = 0, data = False, case_sensitive = False)

### Run
for ff in filess:

    actual = os.getcwd()
    os.chdir(ff.folder)

    print("Running ", os.getcwd())

    order = r"python %s" % ff.file_name

    txt = ""

    p = os.popen(order)
    while 1:
        line = p.readline()
        if not line: break
        txt = txt + line.rstrip() + os.linesep

    os.chdir(actual)

    f = open(ff.path_noExt + ".testout",'w')
    f.write(txt) # python will convert \n to os.linesep
    f.close() # you can omit in most cases as the destructor will call if

    print(txt)
