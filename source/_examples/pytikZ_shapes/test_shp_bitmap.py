#!/usr/bin/python

### Load pyTikZ library
import os, sys
import pyTikZ as py_tikZ

### Load main object
tikZ = py_tikZ.load()
tikZ.scale=0.75

### Text label
p = tikZ.pto.pto(-5, 0, 0)
bitmap_path = os.path.dirname(os.path.abspath(__file__))
bitmap_path = os.path.join(bitmap_path, "laplace.jpg")
txt = tikZ.shp.bitmap(p, bitmap_path, width=3, height=None, layer=0, color='', fill='red', rotate_text=0, position='', align='')
 
p = tikZ.pto.pto(0, 0, 0)
bitmap_path = os.path.dirname(os.path.abspath(__file__))
bitmap_path = os.path.join(bitmap_path, "lena_01.jpg")
txt = tikZ.shp.bitmap(p, bitmap_path, width=3, height=None, layer=0, color='', fill='orange', rotate_text=0, position='', align='')

p = tikZ.pto.pto(5, 0, 0)
bitmap_path = os.path.dirname(os.path.abspath(__file__))
bitmap_path = os.path.join(bitmap_path, "gauss.jpg")
txt = tikZ.shp.bitmap(p, bitmap_path, width=3, height=None, layer=0, color='', fill='green', rotate_text=0, position='', align='')

### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name)


