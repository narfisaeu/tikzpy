# python3

import tikzpy

### Load main object
tikZ = tikzpy.pytikz()

### Add point at x=0, y=0, z=0
p0 = tikZ.pto.pto(0,0,0)

### Add point at x=1, y=1, z=1
p2 = tikZ.pto.pto(1,1,1)

### Define custom color
tikZ.col["custom_color_rgb"] = "150_50_5"
tikZ.col["custom_color"] = "red!50"

### Add a line for example
l1 = tikZ.shp.line(p0, p2, color = "custom_color")

print(l1)