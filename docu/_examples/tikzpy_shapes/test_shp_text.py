#!/usr/bin/python

### Load tikzpy library
import os, sys
import tikzpy as py_tikZ

### Load main object
tikZ = py_tikZ.load()
tikZ.scale_text=0.75

### Text label 
p = tikZ.pto.pto(1.5, 0, 0)
txt = tikZ.shp.text(p, "**Position**", layer=0, color='', fill='', rotate_text=0, position='below', align='center')

p = tikZ.pto.pto(0, -1, 0)
tikZ.shp.circle(p, 0.1, layer=0, thick='', type='', color='green', fill='green!10')
txt = tikZ.shp.text(p, "above", layer=0, color='', fill='', rotate_text=0, position='above', align='')
txt = tikZ.shp.text(p, "below", layer=0, color='', fill='', rotate_text=0, position='below', align='')
txt = tikZ.shp.text(p, "left", layer=0, color='', fill='', rotate_text=0, position='left', align='')
txt = tikZ.shp.text(p, "right", layer=0, color='', fill='', rotate_text=0, position='right', align='')

p = tikZ.pto.pto(3, -1, 0)
tikZ.shp.circle(p, 0.1, layer=0, thick='', type='', color='green', fill='green!10')
txt = tikZ.shp.text(p, "above left", layer=0, color='', fill='', rotate_text=0, position='above left', align='')
txt = tikZ.shp.text(p, "below left", layer=0, color='', fill='', rotate_text=0, position='below left', align='')
txt = tikZ.shp.text(p, "above right", layer=0, color='', fill='', rotate_text=0, position='above right', align='')
txt = tikZ.shp.text(p, "below right", layer=0, color='', fill='', rotate_text=0, position='below right', align='')


p = tikZ.pto.pto(6, 0, 0)
txt = tikZ.shp.text(p, "**Align**", layer=0, color='', fill='', rotate_text=0, position='below', align='center')

p = tikZ.pto.pto(6, -1, 0)
tikZ.shp.circle(p, 0.1, layer=0, thick='', type='', color='green', fill='green!10')
txt = tikZ.shp.text(p, "align center", layer=0, color='', fill='', rotate_text=0, position='right', align='center')
p = tikZ.pto.pto(6, -1.5, 0)
tikZ.shp.circle(p, 0.1, layer=0, thick='', type='', color='green', fill='green!10')
txt = tikZ.shp.text(p, "align right", layer=0, color='', fill='', rotate_text=0, position='right', align='right')
p = tikZ.pto.pto(6, -2, 0)
tikZ.shp.circle(p, 0.1, layer=0, thick='', type='', color='green', fill='green!10')
txt = tikZ.shp.text(p, "align left", layer=0, color='', fill='', rotate_text=0, position='right', align='left')

p = tikZ.pto.pto(9, 0, 0)
txt = tikZ.shp.text(p, "**Rotate**", layer=0, color='', fill='', rotate_text=0, position='below', align='center')

p = tikZ.pto.pto(9, -1, 0)
tikZ.shp.circle(p, 0.1, layer=0, thick='', type='', color='green', fill='green!10')
txt = tikZ.shp.text(p, "20$^\circ$ degrees", layer=0, color='', fill='', rotate_text=20, position='right', align='center')
p = tikZ.pto.pto(9, -1.5, 0)
tikZ.shp.circle(p, 0.1, layer=0, thick='', type='', color='green', fill='green!10')
txt = tikZ.shp.text(p, "10$^\circ$ degrees", layer=0, color='', fill='', rotate_text=10, position='right', align='right')
p = tikZ.pto.pto(9, -2, 0)
tikZ.shp.circle(p, 0.1, layer=0, thick='', type='', color='green', fill='green!10')
txt = tikZ.shp.text(p, "-45$^\circ$ degrees", layer=0, color='', fill='', rotate_text=-45, position='right', align='left')


### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name)


