#!/usr/bin/python

### Load pyTikZ library
import os
import pyTikZ as py_tikZ

### Load main object
tikZ = py_tikZ.pytikz()
#or
tikZ = py_tikZ.load()

### Options
tikZ.dpi=300               #dots per inch property of the drawings
tikZ.extension=".tikz.tex" #extension property use to build TikZ drawings
tikZ.unit=""               #general units use in TikZ drawing, no units by default
tikZ.scale=1.              #scale value of the TikZ drawing
tikZ.scale_text=1.         #scale value for the nodes text the TikZ drawing

### 3D perpective
tikZ.rot_x = 60
tikZ.rot_z = 120

side = 1
p0 = tikZ.pto.pto(0, 0, 0)

### Coordinates
px = tikZ.pto.pto(2*side, 0, 0)
lx = tikZ.shp.line(p0, px, layer=0, thick='thick', type='', color='', fill='')
lx.arrow = "->"
tikZ.shp.text(px, "X", layer=0, color='', fill='', rotate_text=0, position='left', align='')
py = tikZ.pto.pto(0, 2*side, 0)
ly=tikZ.shp.line(p0, py, layer=0, thick='thick', type='', color='', fill='')
ly.arrow = "->"
tikZ.shp.text(py, "Y", layer=0, color='', fill='', rotate_text=0, position='right', align='')
pz = tikZ.pto.pto(0, 0, 2*side)
lz=tikZ.shp.line(p0, pz, layer=0, thick='thick', type='', color='', fill='')
lz.arrow = "->"
tikZ.shp.text(pz, "Z", layer=0, color='', fill='', rotate_text=0, position='above', align='')

### Draw a cube
#Down
grp_front = tikZ.grp.addgroup("grp_down")
grp_front.add = p0
grp_front.add = tikZ.pto.pto(side, 0, 0)
grp_front.add = tikZ.pto.pto(side, side, 0)
grp_front.add = tikZ.pto.pto(0, side, 0)
grp_front.add = tikZ.pto.pto(0, 0, 0)
shp_front = tikZ.shp.path(grp_front.ptos, layer=0, thick='', type='', color='', fill='red')
#Up
grp_up = tikZ.grp.addgroup("grp_up")
grp_up.add = tikZ.pto.pto(0, 0, side)
grp_up.add = tikZ.pto.pto(side, 0, side)
grp_up.add = tikZ.pto.pto(side, side, side)
grp_up.add = tikZ.pto.pto(0, side, side)
grp_up.add = tikZ.pto.pto(0, 0, side)
shp_up = tikZ.shp.path(grp_up.ptos, layer=0, thick='', type='', color='', fill='green')
#back
grp_back = tikZ.grp.addgroup("grp_back")
grp_back.add = tikZ.pto.pto(0, 0, side)
grp_back.add = tikZ.pto.pto(0, side, side)
grp_back.add = tikZ.pto.pto(0, side, 0)
grp_back.add = tikZ.pto.pto(0, 0, 0)
grp_back.add = tikZ.pto.pto(0, 0, side)
shp_back = tikZ.shp.path(grp_back.ptos, layer=0, thick='', type='', color='', fill='green!30')
#back2
shp_back2 = tikZ.shp.copy(shp_back)
tikZ.shp.rotate(shp_back2, tikZ.pto.pto(0, 0, 0), Ax=0.0, Ay=0.0, Az=-90.0)

### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
### Save eps
tikZ.save_eps(path, name)
### Save pdf and pngs
tikZ.save_pdf(path, name)
### Save tikz stand alone file
tikZ.save_tikz_stanalone(path, name)
 

