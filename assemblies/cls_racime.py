import math
import numbers
import obj_data
import copy

def log(txt):
    
    print txt

class _racime(object):

    def __init__(self, parent):
        
        self._parent = parent
        self._tik = self._parent.parent
        
    def load_data_ini(self, assem):
        
        _key = assem.id
        
        self._parent.assemblys[_key]["element"] = []
        self._parent.assemblys[_key]["l1"] = None
        self._parent.assemblys[_key]["l2"] = None
        self._parent.assemblys[_key]["l3"] = None
        self._parent.assemblys[_key]["origin"] = None
        self._parent.assemblys[_key]["separation"] = 1
            
    def draw_group_elements(self, units):
        
        ### Common heander
        tik = self._tik
        shps = []
        ##
        
        p0 = tik.pto.pto(0,1,0)
        p1 = tik.pto.pto(1,0,0)        
        
        l1 = tik.shp.line(0)        
        l1.addpto = p1
        l1.addpto = p0
        
        l1.zorder = -1         
        
        shps.append(l1)
        
        ### Common return
        return shps