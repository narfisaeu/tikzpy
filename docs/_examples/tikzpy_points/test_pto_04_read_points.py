# python3

### Load tikzpy library
import tikzpy as py_tikZ
import random, os, sys

### Load main object
tikZ = py_tikZ.load()
tikZ.scale=1.

### Create a cloud of points
def _read_csv(tikZ, file_name):
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, file_name)
    #read csv file
    ptos = tikZ.pto.read_list_csv(path, delimiter = None)
    #scale points coordinates
    sc = 1 /100.
    tikZ.pto.scale(ptos, Sx = sc, Sy = sc, Sz = 1., pto_origin= None)
    #return list of points
    return ptos

ptos_1 = _read_csv(tikZ, r"profile_10.csv")    
ptos_2 = _read_csv(tikZ, r"profile_11.csv")    
    
### Show points
tikZ.pto.draw_points(ptos_1, color = "black")
tikZ.pto.draw_points(ptos_2, color = "black")

### Make drawing
path = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(os.path.abspath(__file__))
name = os.path.splitext(name)[0]
tikZ.save_pdf(path, name)





