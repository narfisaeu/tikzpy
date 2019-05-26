#!/usr/bin/python

### Load pyTikZ library
import pyTikZ as py_tikZ
import os, sys

### Load main object
tikZ = py_tikZ.load()

### Create a cloud of points
rows = 10
columns = rows
sep = 2


for i in range(0,rows):

    for j in range(0,columns):
    
        x, y, z = j * sep, -i * sep, 0
    
        p = tikZ.pto.pto(x, y, z, layer=0, alias='pto_%i_%i' % (i,j))
        
        c = tikZ.shp.circle(p, sep/4., color = "yellow", fill = "green!20")
        
        t = tikZ.shp.text(p, r'%i-%i' % (i,j))
        t.zorder = 10
        
        if i==j:
            c.addlabel = "diagonal"
            c.dellabel = "default"
        
        if i+j==rows-1 and i!=j:
            c.addlabel = "diagonal_sym"
            c.dellabel = "default"            

### Hide diagonals        
tikZ.lbl.set_active_labels("diagonal", active=False)                     
# Show acive labels        
print tikZ.lbl.list_active_labels(active=True)    

### Change color symetric diagonal
shps = tikZ.lbl.shapes_by_label("diagonal_sym")    
tikZ.shp.color_to_shapes(shps, "red")
tikZ.shp.fill_to_shapes(shps, "brown!20")
        
### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name)        