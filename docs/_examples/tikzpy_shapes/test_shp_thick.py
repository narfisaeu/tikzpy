# python3

### Load tikzpy library
import os, sys
import tikzpy as py_tikZ

### Load main object
tikZ = py_tikZ.load()
tikZ.dpi=300

### Add point at x=0, y=0, z=0
p1 = tikZ.pto.pto(0,0,0, layer=0, alias='pto1')
p2 = tikZ.pto.pto(3,0,0, layer=0, alias='pto2')

### First line
l = tikZ.shp.line(p1,p2,thick="") #Default case
tx = tikZ.shp.text(p2, "Default thickness, thick=\"\"", layer = 0)
tx.position = "right"

# Types of line
thick_types = l.line_thick_options()
thick_types.append(1.2) ### Is possible to set the thickness number: line width=0.2cm
thick_types.append(5.2)
in_y = 1
in_x = 8

#Iterate types
ii = 1
for t in thick_types:
    p1 = p1.copy()
    p2 = p2.copy()
    p1.y = p1.y + in_y
    p2.y = p2.y + in_y
    l = tikZ.shp.line(p1,p2,thick=t)
    tx = tikZ.shp.text(p2, "thick=\"%s\"" % str(t), layer = 0)    
    tx.position = "right"
    ii = ii + 1
    if ii == 6:  
        p1 = tikZ.pto.alias('pto1').copy()
        p2 = tikZ.pto.alias('pto2').copy()
        p1.x = p1.x + in_x
        p2.x = p2.x + in_x

### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name)


