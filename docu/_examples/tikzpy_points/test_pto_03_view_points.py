#!/usr/bin/python

### Load tikzpy library
import tikzpy as py_tikZ
import random, os, sys

### Load main object
tikZ = py_tikZ.load()

### Create a cloud of points
max_number = 100
radius = 10
ptos = []

for i in range(0,max_number):
    ### Random points
    x, y, z = random.uniform(-radius, radius), \
              random.uniform(-radius, radius), \
              random.uniform(-radius, radius)
              
    ### Create a point
    p = tikZ.pto.pto(x, y, z, layer=0, alias='pto%i' %i)
    
    ### List of points
    ptos.append(p.id)

ptosB = tikZ.pto.copy(ptos, alias_prefix = "B-")
ptosC = tikZ.pto.copy(ptos, alias_prefix = "C-")

tikZ.pto.translate(ptosB, x=(2*radius)*1.1)
tikZ.pto.translate(ptosC, x=(4*radius)*1.1)

#tikZ.pto.rotate(ptosC, pto_rotation = None, Ax = 0., Ay = 0., Az = 0.)
    
### Show points
tikZ.pto.draw_points(ptos, color = "black")
tikZ.pto.draw_points(ptosB, color = "red")
tikZ.pto.draw_points(ptosC, color = "blue")

### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name)





