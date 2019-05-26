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

### Declare groups
grp1 = tikZ.grp.addgroup("_diagonal")         
grp2 = tikZ.grp.addgroup("_diagonal_sym")  

for i in range(0,rows):

    for j in range(0,columns):
    
        x, y, z = j * sep, -i * sep, 0
    
        p = tikZ.pto.pto(x, y, z, layer=0, alias='pto_%i_%i' % (i,j))
        
        c = tikZ.shp.circle(p, sep/4., color = "yellow", fill = "green!20")
        
        t = tikZ.shp.text(p, r'%i-%i' % (i,j))
        t.zorder = 10
        
        if i==j:
            grp1.add = [p,c,t]
            
        if i+j==rows-1 and i!=j:
            grp2.add = [p,c]            
        
       

### Hide diagonals        
tikZ.lbl.label_to_shapes(grp1.shps, "diagonal", delete_label=False)
tikZ.lbl.label_to_shapes(grp1.shps, "default", delete_label=True)
tikZ.lbl.set_active_labels("diagonal", active=False)
# Show acive labels        
print tikZ.lbl.list_active_labels(active=True)    

### Change color symetric diagonal
tikZ.shp.color_to_shapes(grp2.shps, "red")
tikZ.shp.fill_to_shapes(grp2.shps, "brown!20")
        
### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name)        