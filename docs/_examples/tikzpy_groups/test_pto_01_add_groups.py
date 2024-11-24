# python3

### Load tikzpy library
import tikzpy as py_tikZ
import random, os, sys

### Load main object
tikZ = py_tikZ.load()

### Create a cloud of points
max_number = 10
radius = 10
ptos = []
shps = []

### Create a group
grp = tikZ.grp.addgroup("grp1")

for i in range(0,max_number):
    ### Random points
    x, y, z = random.uniform(-radius, radius), \
              random.uniform(-radius, radius), \
              random.uniform(-radius, radius)

    ### Create a point
    p = tikZ.pto.pto(x, y, z, layer=0, alias='pto%i' %i)
    p1 = tikZ.pto.pto(x, y, z, layer=0, alias='ptoo%i' %i) #Not in shapes
    if i > 0:
        l = tikZ.shp.line(ptos[i-1], p)
        l.arrow_build("","Latex",1)
        shps.append(l)
        grp.add = l

    ### List of points
    ptos.append(p.id)
    tikZ.grp["grp1"] = p
    tikZ.grp["grp1"] = p1

print( "Points and shapes in first group")
print( grp.ptos, grp.shps)

### Create a second group
grp1 = tikZ.grp.addgroup("grp2")
grp1.add = ptos
print( "Points and shapes in second group")
print( grp1.ptos, grp1.shps)

### Operate
print( grp.ptos_of_shapes, grp.all_ptos)
print( grp.ptos[-1].id)


### Show points
tikZ.pto.draw_points(ptos, color = "black")

### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name)
