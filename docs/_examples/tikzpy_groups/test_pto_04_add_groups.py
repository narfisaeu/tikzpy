# python3

### Load tikzpy library
import tikzpy as py_tikZ
import os, sys
import numpy as np

### Load main object
tikZ = py_tikZ.load()

### Create path of void
steps = 50
thetas = np.arange(0., 2.*np.pi, 2.*np.pi/steps).tolist()

### Hypocycloid
# https://en.wikipedia.org/wiki/Hypocycloid

grp = tikZ.grp.addgroup("grp%i" % 0)

pm = tikZ.pto.pto(0, 0, 0)
grp.add = pm

k = 2
c_steps = 40
c_max = 1./(k)
css = np.arange(-c_max, c_max, 2.*c_max/c_steps).tolist() + [c_max]

cols = 6
sep = 2.5
(row, col) = (0., 0.)
(x_c, y_c) = (0, 0)

ii = 0
for c in css:      
    
    (x_c, y_c) = (col * sep * 1.15, row*sep*1.35)
    
    for theta in thetas:
        
        x = ( np.cos(theta)) + (c * np.cos(k * theta)) 
        y = ( np.sin(theta)) - (c * np.sin(k * theta))
        
        p1 = tikZ.pto.pto(x+x_c, y+y_c, 0, layer=0)
        grp.add = p1
        
        ii = ii + 1
    
    pc = tikZ.pto.pto(x_c, y_c-0.7*sep, 0, layer=0)
    
    txt = tikZ.shp.text(pc, r'(k,c)=(%i,%.3f)' % (k,c))
    grp.add = txt         
    
    if col >= cols:
        col = 0
        row = row - 1
    else:
        col = col + 1    

print( tikZ.col.names)

tikZ.pto.draw_points(grp.ptos, color = "black")

### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name)
