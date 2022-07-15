#!/usr/bin/python

### Load pyTikZ library
import pyTikZ as py_tikZ
import os, sys

### Load main object
tikZ = py_tikZ.load()

### Create a cloud of points
max_number = 4
radius = 5

### Create a group
angle = 0
pm = tikZ.pto.pto(0, 0, 0)

for i in range(0,max_number):

    ### Create a point
    p1 = tikZ.pto.pto(radius, 0, 0, layer=0, alias='pto1%i' %i)
    p2 = tikZ.pto.pto(-radius, 0, 0, layer=0, alias='pto2%i' %i)
    l = tikZ.shp.line(p1,p2)
    c1 = tikZ.shp.circle(p1, radius*0.3, color = "green", fill="green!30")
    c2 = tikZ.shp.circle(p2, radius*0.3, color = "red", fill="red!30")
    c1.zorder = 1
    c2.zorder = 1

    grp = tikZ.grp.addgroup("grp%i" % i)
    grp.add = [p1,p2,c1,c2, l]

    if i > 0:
        tikZ.shp.rotate(grp.shps, pm, Ax = 0, Ay = 0, Az = -180*i/max_number)

print( tikZ.col.names)

### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name)
