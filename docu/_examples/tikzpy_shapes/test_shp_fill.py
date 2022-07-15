#!/usr/bin/python

### Load tikzpy library
import os, sys
import tikzpy as py_tikZ

### Load main object
tikZ = py_tikZ.load()
tikZ.scale = 1.00
tikZ.scale_text = 1.00
rad = 0.05
iy = -0.8
ix = 5

def _new_p(p, ix, iy):
    _p = p.copy()
    _p.y = _p.y + iy
    _p.x = _p.x + ix
    return _p

### Add point at x=0, y=0, z=0
p = tikZ.pto.pto(0,0,0)
tx = tikZ.shp.circle(p, rad, layer = 0, fill="0_0_0_50")
tx = tikZ.shp.text(p, "Fill by color: fill=red!10", layer = 0, fill="red!10", position = "right")

p=_new_p(p, 0, iy)
tikZ.col["custom"] = "green!50"
tx = tikZ.shp.circle(p, rad, layer = 0, fill="0_0_0_50")
tx = tikZ.shp.text(p, "Fill by color: fill=custom", layer = 0, fill="custom", position = "right")

ii = 0
for pattern_type in tikZ.shp._types_patterns():
    
    if ii == 5:
        p = tikZ.pto.pto(ix,0,0)
    else:
        p=_new_p(p, 0, iy)
    pattern1 = tikZ.shp.pattern_build(pattern_type, color = "blue!50") 
    tx = tikZ.shp.circle(p, rad, layer = 0, fill="0_0_0_50")
    tx = tikZ.shp.text(p, "Pattern: %s" % pattern_type, layer = 0, fill=pattern1, position = "right")
    
    ii += 1
    
### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name, as_png = True)



