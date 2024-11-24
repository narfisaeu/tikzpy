# python3

### Load tikzpy library
import os, sys
import tikzpy as py_tikZ
import numpy as np

### Load main object
tikZ = py_tikZ.load()
tikZ.dpi=300

### Add point at x=0, y=0, z=0
p0 = tikZ.pto.pto(0,0,0)

### Assembly type racime
vbar = tikZ.plots.bars_vertical(group = 0)

N = 4
data_buff = tikZ.dbuffer.load_empty_dbuff(N)
vbar.lbl_axis0 = "axis0"
data_buff[vbar.lbl_axis0] = np.asarray([15,	43,	35,	7])
vbar.lbl_label1 = "axis1"
data_buff[vbar.lbl_label1] = np.asarray(["15\\%", "43\\%", "35\\%", "7\\%"])
vbar.lbl_label2 = "axis2"
data_buff[vbar.lbl_label2] = np.asarray(["Primario","Inicial","Secundario","Sup. no universitario"])
vbar.title = "\\textbf{Alumnos}"
vbar.load_data_buffer(data_buff)

vbar.width = 4
vbar.p0 = p0

vbar.draw_plot()
# Changeline type & fill
tikZ.shp.fill_to_shapes(vbar.lst_path0, "red!10")
tikZ.shp.thick_to_shapes(vbar.shps, "very thick")

### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name)
