#!/usr/bin/python

### Load tikzpy library
import os, sys
import tikzpy as py_tikZ
import numpy as np

### Load main object
tikZ = py_tikZ.load()
tikZ.dpi=300

### Add point at x=0, y=0, z=0
p0 = tikZ.pto.pto(0,0,0)

### Assembly type bar plots 1
vbar = tikZ.plots.bars_vertical(group = 0)

N = 4
data_buff = tikZ.dbuffer.load_empty_dbuff(N)
vbar.lbl_axis0 = "axis0"
data_buff[vbar.lbl_axis0] = np.asarray([15,	43,	35,	7])
vbar.lbl_label1 = "axis1"
data_buff[vbar.lbl_label1] = np.asarray(["15\%", "43\%", "35\%", "7\%"])
vbar.lbl_label2 = "axis2"
data_buff[vbar.lbl_label2] = np.asarray(["","","",""])
vbar.title = r"\textbf{Alumnos} \\ 10.759.510"
vbar.load_data_buffer(data_buff)

vbar.width = 4
vbar.p0 = p0
vbar.draw_plot()
# Changeline type & fill
tikZ.shp.fill_to_shapes(vbar.lst_path0, "green!10")
tikZ.shp.thick_to_shapes(vbar.shps, "very thick")

### Assembly type bar plots 2
vbar = tikZ.plots.bars_vertical(group = 0)

N = 4
data_buff = tikZ.dbuffer.load_empty_dbuff(N)
vbar.lbl_axis0 = "axis0"
data_buff[vbar.lbl_axis0] = np.asarray([18,	52,	26,	4])
vbar.lbl_label1 = "axis1"
data_buff[vbar.lbl_label1] = np.asarray(["18\%", "52\%", "26\%", "4\%"])
vbar.lbl_label2 = "axis2"
data_buff[vbar.lbl_label2] = np.asarray(["Primario","Inicial","Secundario","Sup. no universitario"])
vbar.title = r"\textbf{Docentes} \\ 670.579"
vbar.load_data_buffer(data_buff)

vbar.width = 5
vbar.p0 = p0
mpto = p0.copy()
mpto.x = mpto.x + 6 + 1
vbar.move(mpto)
vbar.draw_plot()
# Changeline type & fill
pattern1 = tikZ.shp.pattern_build("crosshatch dots", color = "blue!50")
tikZ.shp.fill_to_shapes(vbar.lst_path0, pattern1)
tikZ.shp.thick_to_shapes(vbar.shps, "very thick")

### Assembly type bar plots 3
vbar = tikZ.plots.bars_vertical(group = 0)

N = 4
data_buff = tikZ.dbuffer.load_empty_dbuff(N)
vbar.lbl_axis0 = "axis0"
data_buff[vbar.lbl_axis0] = np.asarray([33,	41,	22,	4])
vbar.lbl_label1 = "axis1"
data_buff[vbar.lbl_label1] = np.asarray(["33\%", "41\%", "22\%", "4\%"])
vbar.lbl_label2 = "axis2"
data_buff[vbar.lbl_label2] = np.asarray(["","","",""])
vbar.title = r"\textbf{Unidades educativas} \\ 54.610"
vbar.load_data_buffer(data_buff)

vbar.width = 5
vbar.p0 = p0
mpto = p0.copy()
mpto.x = mpto.x - 6 - 1
vbar.move(mpto)
vbar.draw_plot()
# Changeline type & fill
pattern1 = tikZ.shp.pattern_build("crosshatch dots", color = "red!50")
tikZ.shp.fill_to_shapes(vbar.lst_path0, pattern1)
tikZ.shp.thick_to_shapes(vbar.shps, "very thick")

### Assembly type arrow plot
vbar = tikZ.plots.arrow_vertical(group = 0)

N = 4
data_buff = tikZ.dbuffer.load_empty_dbuff(N)
vbar.lbl_axis0 = "axis0"
data_buff[vbar.lbl_axis0] = np.asarray([13.2,13.1,22.0,31.1])
vbar.lbl_label1 = "axis1"
data_buff[vbar.lbl_label1] = np.asarray(["13.2", "13.1", "22.0", "31.1"])
vbar.title = r"\textbf{$\frac{Alumnos}{Docente}$}"
vbar.load_data_buffer(data_buff)

vbar.width = 4
vbar.p0 = p0
vbar.up_down = True
vbar.thick_scale = 0
mpto = p0.copy()
mpto.x = mpto.x + 3.5
vbar.move(mpto)
vbar.draw_plot()
tikZ.shp.thick_to_shapes(vbar.shps, "very thick")

### Assembly type arrow plot
vbar = tikZ.plots.arrow_vertical(group = 0)

N = 4
data_buff = tikZ.dbuffer.load_empty_dbuff(N)
vbar.lbl_axis0 = "axis0"
data_buff[vbar.lbl_axis0] = np.asarray([89.3,206.8,313.7,354.8])
vbar.lbl_label1 = "axis1"
data_buff[vbar.lbl_label1] = np.asarray(["89.3","206.8","313.7","354.8"])
vbar.title = r"\textbf{$\frac{Alumnos}{Unidad}$}"
vbar.load_data_buffer(data_buff)

vbar.width = 4
vbar.p0 = p0
vbar.up_down = False
vbar.thick_scale = 0
mpto = p0.copy()
mpto.x = mpto.x - 3.5
vbar.move(mpto)
vbar.draw_plot()
tikZ.shp.thick_to_shapes(vbar.shps, "very thick")

### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name)
