#!/usr/bin/python

### Load pyTikZ library
import os, sys
import pyTikZ as py_tikZ

### Load main object
tikZ = py_tikZ.load()
tikZ.scale = 1.00
tikZ.scale_text = 1.00

### Add point at x=0, y=0, z=0
p1 = tikZ.pto.pto(0,0,0, layer=0, alias='pto1')
p2 = tikZ.pto.pto(1.5,0,0, layer=0, alias='pto2')

tipstypes = ["latex","stealth","triangle 90","triangle 60","triangle 45","open triangle 90","open triangle 60","open triangle 45", "angle 90", "angle 60", "angle 45", "hooks"]
tipstypes += ["latex reversed","stealth reversed","triangle 90 reversed","triangle 60 reversed","triangle 45 reversed","open triangle 90 reversed","open triangle 60 reversed","open triangle 45 reversed", "angle 90 reversed", "angle 60 reversed", "angle 45 reversed", "hooks reversed", "o", "*", "diamond", "square"]

### First line
l = tikZ.shp.line(p1,p2) #Due to tranparent background
tikZ.shp.arrow_to_shapes(l, start=tipstypes[0], end=tipstypes[0], scale=1.)
tx = tikZ.shp.text(p2, "type: %s" % tipstypes[0], layer = 0)
tx.position = "right"

# Types of line
in_y = -0.75
in_x = 6

#Iterate types
ii = 1
for jj in range(1,len(tipstypes)):
    p1 = p1.copy()
    p2 = p2.copy()
    p1.y = p1.y + in_y
    p2.y = p2.y + in_y
    
    l = tikZ.shp.line(p1,p2) #Due to tranparent background
    tikZ.shp.arrow_to_shapes(l, start=tipstypes[ii], end=tipstypes[ii], scale=1.)
    tx = tikZ.shp.text(p2, "type: %s" % tipstypes[ii], layer = 0)
    tx.position = "right"

    ii = ii + 1
    if ii == 15:  
        p1 = tikZ.pto.alias('pto1').copy()
        p2 = tikZ.pto.alias('pto2').copy()
        p1.x = p1.x + in_x
        p2.x = p2.x + in_x
        
### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name, as_png = True)


