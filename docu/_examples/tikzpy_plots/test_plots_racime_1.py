#!/usr/bin/python

### Load tikzpy library
import os, sys
import tikzpy as py_tikZ

### Load main object
tikZ = py_tikZ.load()
tikZ.dpi=300

### Add point at x=0, y=0, z=0
p0 = tikZ.pto.pto(0,0,0)

### Add point at x=1, y=1, z=1
p1 = tikZ.pto.pto(1,1,1)

### Assembly type racime
rac = tikZ.plots.racime(group = 0)
rac.l1 = 10.             #Add length 1 value
rac.l2 = 5.              #Add length 2 value
rac.l3 = 1.              #Add length 3 value
rac.origin = p0          #Add point

rac.add_element("Example", thickness = None, separation = None)
rac.add_element("Example 1", thickness = None, separation = None)
rac.add_element("Example 2", thickness = None, separation = None)
rac.move(p1-p0)          #Move assembly
rac.addlabel="patatin"   #Add a label

### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name)
