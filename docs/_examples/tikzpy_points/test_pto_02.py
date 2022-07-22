#!/usr/bin/python

### Load tikzpy library
import tikzpy as py_tikZ

### Load main object
tikZ = py_tikZ.pytikz()
# or
tikZ = py_tikZ.load()

### Add point at x=0, y=0, z=0
p1 = tikZ.pto.pto(0.1,0.2,0.3, layer=0, alias='pto1')

### Add point at x=1, y=1, z=1
p2 = tikZ.pto.pto(1,1,1, layer=0, alias='pto2')

########### Operations

### Vector between point 1 and 2 as auxiliary point
vec = p2 - p1

print( "01-", p1)
print( "02-", p2)
print( "03-", vec)

### Conversion of auxiliary into point
vec.save()
vec.alias = "vec"
print( "04-", vec)

### Scaling a point into an auxiliary point
p3 = p2 * 2.
print( "05-", p3)

### Scaling a point and modify the values
tikZ.pto[p2.id] = p2 * 2.
#or
p2.xyz = p2 * 2.
print( "06-", p2)

### Array multiplication
print( "07-", p1 * p2)

### Adding a real number
print( "08-", p1 + 3.)

### Proof
print( "09-", p1 == p2)
print( "10-", p1 != p2)
print( "11-", p1 != p1)
print( "12-", p1 == p1)

### Searching by alias
pp1 = tikZ.pto.alias("vec")
pp2 = tikZ.pto.alias("pto1")
print( "13-", pp1)
print( "14-", pp2)
