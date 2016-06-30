#!/usr/bin/python

### Load pyTikZ library
import os, sys
import pyTikZ as py_tikZ

### Load main object
tikZ = py_tikZ.load()


### Text label 
p1 = tikZ.pto.pto(0, 0, 0)
p2 = tikZ.pto.pto(20, 10, 0)

tikZ.shp.grid(p1,p2, xstep = 1, ystep = 2, layer = 0, thick = "help lines", type = "dashdotted", color = "red")

### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name)


