#!/usr/bin/python

### Load tikzpy library
import tikzpy as py_tikZ

### Load main object
tikZ = py_tikZ.pytikz()

### Add point at x=0, y=0, z=0
p1 = tikZ.pto.pto(0.1,0.2,0.3, layer=0, alias='pto1')

p2 = tikZ.pto.pto(1.1,1.2,1.3, layer=0, alias='pto2')
print( p2)

### How to call a point?
p3 = tikZ.pto.pto(1.1,1.2,1.3, layer=0, alias='pto3')
print(  p3.id == tikZ.pto.alias('pto3').id) #Is True
print(  p3.id == tikZ.pto[p3.id].id )#Is True
print(  p3.id == (p3*2).id) #Is False

### How to make ne point?
p4 = tikZ.pto.pto(1.2,1.3,1.4, layer=0, alias='pto4')
print( p4)
p5 = p4 # Assignment by reference (same pointer)
print( p5)
p5 = p4.copy() # Copy a new point with no alias
print( p5)
p5 = p4.copy('pto5') # Copy a new point with alias
print( p5)

### Operations return an axuiliary point
p2 = p2 + 1 #p2 becomes an auxiliary point
print( p2, p2.id == tikZ.pto.alias('pto2').id)

### To modify the point coord use .xyz
p2 = tikZ.pto.alias('pto2')
p2.xyz = p2 + 1
print( p2, p2.id == tikZ.pto.alias('pto2').id)
p2.xyz = p2 + 1
print( p2, p2.id == tikZ.pto.alias('pto2').id)
