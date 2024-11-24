# python3

### Load tikzpy library
import tikzpy as py_tikZ
import random, os, sys

### Load main object
tikZ = py_tikZ.load()

### Create a cloud of points
max_number = 10
radius = 10

### Create a group
grp1 = tikZ.grp.addgroup("grp1")

for i in range(0,max_number):
    ### Random points
    x, y, z = random.uniform(-radius, radius), \
              random.uniform(-radius, radius), \
              0 #random.uniform(-radius, radius)
    
    ### Create a point
    p = tikZ.pto.pto(x, y, z, layer=0, alias='pto%i' %i)
    
    if i > 0:
        l = tikZ.shp.line(grp1.ptos[-1], p)
        l.arrow_build("","Latex",1)
        grp1.add = l
        
    ### List of points
    grp1.add = p

### Point copy
grp2 = tikZ.grp.addgroup("grp2")
grp2.add = tikZ.pto.copy(grp1.ptos, alias_prefix = "", alias_sufix = "")
grp2.add = tikZ.shp.copy(grp1.shps)

### Translate
[[min_x,max_x],[min_y,max_y],[min_z,max_z]] = grp1.canvas(ptos = None)
p1 = tikZ.pto.pto(min_x, (min_y + max_y)/2., (min_z + max_z)/2., layer=0)
p2 = tikZ.pto.pto(max_x, (min_y + max_y)/2., (min_z + max_z)/2., layer=0)

tikZ.pto.translate_to(grp2.ptos, p1, p2)
tikZ.shp.translate_to(grp2.shps, p1, p2)  
tikZ.shp.translate(grp2.shps, x = 1., y = 0., z = 0.) #Offset of 1.
for shp in grp2.shps:
    shp.color = "orange"
    
### Show points
tikZ.pto.draw_points(ptos =grp1.ptos, color = "black")
tikZ.pto.draw_points(ptos =grp2.ptos, color = "red")

### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name)





