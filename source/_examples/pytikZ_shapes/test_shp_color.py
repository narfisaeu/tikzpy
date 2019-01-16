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

### First line
l = tikZ.shp.line(p1,p2, thick="5", color="white") #Due to tranparent background
l.zorder = -1
l = tikZ.shp.line(p1,p2, thick="5", color="") #Default case
l.zorder = 1
tx = tikZ.shp.text(p2, "Default color, color=\"\"", layer = 0)
tx.position = "right"

# Types of line
colors = tikZ.col._default
in_y = 0.75
in_x = 6

# Add custom colors
direct_custom = ["red!10","red!80","red!10!yellow","red!80!yellow"]
colors = colors + direct_custom
direct_custom = ["red!10","red!80","red!10!yellow","red!80!yellow"]
colors = colors + direct_custom
direct_custom = ["0_0_0","0_0_0_10","0_0_0_50"]
colors = colors + direct_custom

# Add custom colors with object color
tikZ.col["custom1"] = "black!10"
tikZ.col["custom2"] = "0_0_0_10"
tikZ.col["custom3"] = "red"
tikZ.col["custom4"] = "red!80"
colors = colors + ["custom1","custom2","custom3","custom4"]

#Iterate types
ii = 1
for col in colors:
    p1 = p1.copy()
    p2 = p2.copy()
    p1.y = p1.y + in_y
    p2.y = p2.y + in_y
    print col
    l = tikZ.shp.line(p1,p2, thick="5", color="white")
    l.zorder = -1
    l = tikZ.shp.line(p1,p2, thick="5", color=col)
    l.zorder = 1
    tx = tikZ.shp.text(p2, "color=\"%s\"" % col.replace("_","\_"), layer = 0)    
    tx.position = "right"
    tx.zorder = 1
    ii = ii + 1
    if ii == 18:  
        p1 = tikZ.pto.alias('pto1').copy()
        p2 = tikZ.pto.alias('pto2').copy()
        p1.x = p1.x + in_x
        p2.x = p2.x + in_x

#Number of colors       
print "Num colors: %i" % tikZ.col.num_colors
        
### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name, as_png = True)


