#!/usr/bin/python

### Load tikzpy library
import os, sys
import math
import tikzpy as py_tikZ

tikZ = py_tikZ.load()

### Create a list points according a sinus
f=1.
total = 100.

lst_ids = []
lst_pto = []
lst_alias = []

for i in range(0, int(total)):
    x = (5. / total) * i
    y = 0.5*math.sin(2*math.pi*f*x)

    alias = 'pto%i' % i
    p = tikZ.pto.pto(x,y,0, layer=0, alias=alias)

    ### Create list
    lst_ids.append(p.id)
    lst_pto.append(p)
    lst_alias.append(alias)

### Draw a path of points by ids
l1 = tikZ.shp.path(lst_ids, layer = 0, color = "black", thick = "2")
l1.zorder = 0
#See points in line
print( l1.addpto)

### Draw a path of points by pto
l2 = tikZ.shp.path(lst_pto, layer = 0, color = "red", thick = "1")
l2.zorder = 1
#See points in line
print( l2.addpto)

### Draw a path of points by pto
l3 = tikZ.shp.path(lst_alias, layer = 0, color = "blue", thick = "0.5")
l3.zorder = 2
#See points in line
print( l3.addpto)

### Copy an translate
lst_copy = tikZ.pto.copy(l3.addpto, alias_prefix = "(", alias_sufix = ")")
print( lst_copy, "-",lst_copy[0].alias)
l4 = tikZ.shp.path(lst_copy, layer = 0, color = "green", thick = "2")
l4.zorder = 3
# translate
tikZ.pto.translate(lst_copy, x = 0.2, y = 1., z = 0.1)

### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name)
