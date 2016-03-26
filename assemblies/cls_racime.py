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
        
        ### List of extra data properties
        self.lst_data = ["element", "l1", "l2", "l3", "origin", "separation", "p_vertex", "p_racimes", "end_thickness", "total_height"]
        
    def load_data_ini(self, assem):
        ### Initialize properties
        _key = assem.id
                
        self._parent.assemblys[_key]["element"] = []
        self._parent.assemblys[_key]["l1"] = None
        self._parent.assemblys[_key]["l2"] = None
        self._parent.assemblys[_key]["l3"] = None
        self._parent.assemblys[_key]["origin"] = None
        self._parent.assemblys[_key]["separation"] = 1.
    
    def set_property(self, attribute, value, _key):
        ### Properties setter bottleneck
        
        if attribute == "p_vertex":
            pass
        elif attribute == "p_racimes":
            pass        
        elif attribute == "end_thickness":
            pass        
        elif attribute == "total_height":
            pass
        else:
            self._parent.assemblys[_key][attribute] = value
    
    def get_property(self, attribute, _key):
        ### Properties getter bottleneck
        
        if attribute == "p_vertex":
            [p1,p2,p3,p4,pm,th_si,sum_si] = self._calculation_points(_key)
            out = []
            for p in p4:
                out.append(p + self._parent.assemblys[_key]["mpto"])
            return out
        elif attribute == "p_racimes":
            [p1,p2,p3,p4,pm,th_si,sum_si] = self._calculation_points(_key)
            out = []
            for p in p1:
                out.append(p + self._parent.assemblys[_key]["mpto"])
            return out
        elif attribute == "total_height":            
            [p1,p2,p3,p4,pm,th_si,sum_si] = self._calculation_points(_key)
            return sum_si
        elif attribute == "end_thickness":
            [p1,p2,p3,p4,pm,th_si,sum_si] = self._calculation_points(_key)
            return th_si            
        else:
            return self._parent.assemblys[_key][attribute]
        
    def draw_group_elements(self, units, assem):
        ### Draw group of shapes function call from main drawer functions
        ### Common heander
        tik = self._tik
        _key = assem.id
        shps = []
        ##
        
        # Calculate points
        [p1,p2,p3,p4,pm,th_si,sum_si] = self._calculation_points(_key)
        
        # Loop elements
        for i in range(0,len(p1)):
            
            [text, thickness, separation] = self._parent.assemblys[_key]["element"][i]
            
            # Add lines
            l1 = tik.shp.line(0)        
            l1.addpto = p1[i]
            l1.addpto = p2[i]
            l1.addpto = p3[i]
            
            if thickness: l1.thick = thickness   
            shps.append(l1)
            
            l = tik.shp.text(pm[i], text,0)
            l.align = 0
            l.position = "above"            
            shps.append(l)
            
        l2 = tik.shp.line(0)  
        l2.addpto = p3[0]
        l2.addpto = p4[0]
        
        l2.thick = th_si 
        shps.append(l2)
            
        ### Common return
        return shps
        
    def _calculation_points(self, key):
        
        #   p1-----------p2
        #          s1      \
        #   p1-----------p2-p3---p4
        #          s2      /
        #   p1-----------p2        
        #          l1      l2  l3
        ### Common heander
        tik = self._tik
        _key = key
        ptos = []
        ##              
                
        ## Looop elements
        i = 0
        sum_si = 0.
        N = len(self._parent.assemblys[_key]["element"])
        p1 = []
        p2 = []
        p3 = []
        p4 = []
        pm = []
        
        for ele in self._parent.assemblys[_key]["element"]:
            # Data
            [text, thickness, separation] = ele
            
            # Points
            _p1 = tik.pto.aux(0.,sum_si,0.)
            p1.append(_p1)
            
            _p2 = tik.pto.aux(float(self._parent.assemblys[_key]["l1"]),sum_si,0.)
            p2.append(_p2)   

            _pm = tik.pto.aux(float(self._parent.assemblys[_key]["l1"])/2.,sum_si,0.)
            pm.append(_pm)              
            
            # Max height
            if i < N - 1:                     
                if separation is None:
                    sum_si = self._parent.assemblys[_key]["separation"] + sum_si
                else:
                    sum_si = separation + sum_si
                                       
            i = i + 1
        
        th = 0.
        x = float(self._parent.assemblys[_key]["l1"]) + float(self._parent.assemblys[_key]["l2"])
        xx = x + float(self._parent.assemblys[_key]["l3"])
        y = (sum_si/2.)# - th_si/2.
        
        for ele in self._parent.assemblys[_key]["element"]:
            # Data
            [text, thickness, separation] = ele        
            
            if self.is_number(thickness):
                 th = th + float(thickness)
            else:
                 th = th + float(1)
            
            _p3 = tik.pto.aux(x,y,0.)
            _p4 = tik.pto.aux(xx,y,0.)
            
            p3.append(_p3)
            p4.append(_p4)
        
        ptos = [p1,p2,p3,p4,pm,th, sum_si]
        
        return ptos
        
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False        
        