#!/usr/bin/python

### Load tikzpy library
import os, sys
import tikzpy as py_tikZ

### Load main object
tikZ = py_tikZ.load()
tikZ.scale = 1.00
tikZ.scale_text = 1.00
tikZ.density = 100

### Add point at x=0, y=0, z=0
p1 = tikZ.pto.pto(0,0,0, layer=0, alias='pto1')
p2 = tikZ.pto.pto(3,0,0, layer=0, alias='pto2')

### First line
l = tikZ.shp.line(p1,p2,thick="") #Default case
tx = tikZ.shp.text(p2, "Default thickness, type=\"\"", layer = 0)
tx.position = "right"

# Types of line
line_types1, line_types2 = l.line_type_options()
line_types = line_types1 + line_types2
in_y = 1
in_x = 8

# Add segment length to type line
for l in line_types2:
    line_types.append(l + "_2.1")

# Add segment length and amplitude to type line
for l in line_types2:
    line_types.append(l + "_5.1_4.1")

#Iterate types
ii = 1
for t in line_types:
    p1 = p1.copy()
    p2 = p2.copy()
    p1.y = p1.y + in_y
    p2.y = p2.y + in_y
    print( t)
    l = tikZ.shp.line(p1,p2,type=t)
    tx = tikZ.shp.text(p2, "type=\"%s\"" % t.replace("_","\_"), layer = 0)
    tx.position = "right"
    ii = ii + 1
    if ii == 14:
        p1 = tikZ.pto.alias('pto1').copy()
        p2 = tikZ.pto.alias('pto2').copy()
        p1.x = p1.x + in_x
        p2.x = p2.x + in_x

### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name)
