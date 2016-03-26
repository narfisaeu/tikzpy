import math
import numbers
import obj_data

class _points(object):

    def __init__(self, parent):
        
        self.parent = parent
        self.auto_save_aux = False
        
        ### Counters
        self.counters = obj_data._clsdata(type = int(0)) 
        
        ### Dictionary of points
        self.points = obj_data._clsdata(type = [])
        self.counters["points"] = 0
        
    def __getitem__(self, key):
    
        return self.point(key)

    def __setitem__(self, key, other_point):
        
        porigin = self.point(key)
        
        if isinstance(other_point, porigin.__class__):
            porigin.x = other_point.x
            porigin.y = other_point.y
            porigin.z = other_point.z
        else:
            pass
    
    def point(self, key):        
        
        ### Give a point
        _key = str(key)
        
        if self.points[_key]:
            return _point(self,_key)
        else:
            return None
    
    def _point_format(self, x, y, z = 0, layer = 0):
        
        return [x,y,z,[int(layer)]]
    
    def addpoint(self, x, y, z = 0, layer = 0):
        
        # Create auto new
        _key =  "#%i" % self.counters["points"]
        self.counters["points"] = self.counters["points"] + 1
        self.points[_key] = self._point_format(x, y, z = z , layer = layer)
        return self.point(_key)
    
    def auxpoint(self, x=0, y=0, z = 0, layer = 0):
    
        lst = self._point_format(x, y, z = z , layer = layer)
        p = _point(self, None, lst)
        if self.auto_save_aux: p.save()
        return p
        
    def pto(self, x=0, y=0, z=0, layer = 0):
        
        return self.addpoint(x, y, z = z, layer = layer)
        
    def aux(self, x=0, y=0, z = 0, layer = 0):
        
        return self.auxpoint(x=x, y=y, z = z, layer = layer)
        
class _point(object):
   
    def __init__(self, parent, key, lst = []):
        
        self.parent = parent
        self._key = key
        self._lst = lst

    def __eq__(self, other):
        
        if isinstance(other, self.__class__):
            if self.x == other.x:
                if self.y == other.y:
                    if self.z == other.z:
                        return True
            return False
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
    ######################## Operators        
    def _add(self, other):
        
        if isinstance(other, self.__class__):
            p = self.parent.auxpoint()
            p.x = self.x + other.x
            p.y = self.y + other.y
            p.z = self.z + other.z
            p.layer = self.layer
            return p
        elif isinstance(other, numbers.Real):
            p = self.parent.auxpoint()
            p.x = self.x + self._valchnage(other)
            p.y = self.y + self._valchnage(other)
            p.z = self.z + self._valchnage(other)
            p.layer = self.layer
            return p        
        else:
            return None    
            
    def __add__(self, other):    
        return self._add(other)
        
    def __radd__(self, other):    
        return self._add(other)

    def __sub__(self, other) :  
        
        if isinstance(other, self.__class__):
            p = self.parent.auxpoint()
            p.x = self.x - other.x
            p.y = self.y - other.y
            p.z = self.z - other.z
            p.layer = self.layer
            return p
        elif isinstance(other, numbers.Real): 
            p = self.parent.auxpoint()
            o = self._valchnage(other)
            p.x = self.x - o
            p.y = self.y - o
            p.z = self.z - o
            p.layer = self.layer
            return p        
        else:
            return None     
    
    def __rsub__(self, other) :        
        
        if isinstance(other, self.__class__):
            p = self.parent.auxpoint()
            p.x = other.x - self.x
            p.y = other.y - self.y
            p.z = other.z - self.z
            p.layer = self.layer
            return p
        elif isinstance(other, numbers.Real): 
            p = self.parent.auxpoint()
            o = self._valchnage(other)
            p.x = o - self.x
            p.y = o - self.y
            p.z = o - self.z
            p.layer = self.layer
            return p                    
        else:
            return None  
            
    def __mul__(self, other) :  
        
        if isinstance(other, self.__class__):
            p = self.parent.auxpoint()
            p.x = self.x * other.x
            p.y = self.y * other.y
            p.z = self.z * other.z
            p.layer = self.layer
            return p
        elif isinstance(other, numbers.Real): 
            p = self.parent.auxpoint()
            o = self._valchnage(other)
            p.x = self.x * o
            p.y = self.y * o
            p.z = self.z * o
            p.layer = self.layer
            return p        
        else:
            return None 
            
    def __rmul__(self, other) :  
        
        if isinstance(other, self.__class__):
            p = self.parent.auxpoint()
            p.x = self.x * other.x
            p.y = self.y * other.y
            p.z = self.z * other.z
            p.layer = self.layer
            return p
        elif isinstance(other, numbers.Real): 
            p = self.parent.auxpoint()
            o = self._valchnage(other)
            p.x = self.x * o
            p.y = self.y * o
            p.z = self.z * o
            p.layer = self.layer
            return p        
        else:
            return None              
        
    def __repr__(self):
        return self.__class__
        
    def __str__(self):
        return "Point key:%s x=%.4f y=%.4f z=%.4f layer=%i NumPoints:%i" % (self.id, self.x, self.y, self.z, self.layer,len(self.parent.points))
        
    ######################## Functions
    def save(self):
        p = self.parent.addpoint(self.x, self.y, z = self.z , layer = self.layer)
        self._key = p.id
        return key
        
    def copy(self):
        if self._key is None:
            p = self.parent.addpoint(self.x, self.y, z = self.z , layer = self.layer)
        else:
            p = self.parent.auxpoint(self.x, self.y, z = self.z , layer = self.layer)
        
        return p   

    def __deepcopy__(self, memo):
        
        return self.copy()
        
    ######################## Properties
    def _valchnage(self,val):
        return float(val)
   
    @property
    def id(self):
        if self._key is None:
            return None
        else:
            return self._key
            
    @property
    def x(self):
        if self._key is None:
            return self._lst[0]
        else:
            return float(self.parent.points[self._key][0])

    @x.setter
    def x(self, value):  
        if self._key is None:
            self._lst[0] = self._valchnage(value)
        else:
            self.parent.points[self._key][0] = self._valchnage(value)

    @property
    def y(self):
        if self._key is None:
            return self._lst[1]
        else:
            return float(self.parent.points[self._key][1])

    @y.setter
    def y(self, value):        
        if self._key is None:
            self._lst[1] = self._valchnage(value)
        else:
            self.parent.points[self._key][1] = self._valchnage(value)
        
    @property
    def z(self):
        if self._key is None:
            return self._lst[2]
        else:
            return float(self.parent.points[self._key][2])

    @z.setter
    def z(self, value):        
        if self._key is None:
            self._lst[2] = self._valchnage(value)
        else:
            self.parent.points[self._key][2] = self._valchnage(value)
        
    @property
    def layer(self):
        if self._key is None:
            return self._lst[3][0]
        else:
            return self.parent.points[self._key][3][0]

    @z.setter
    def layer(self, value):        
        if self._key is None:
            self._lst[3][0] = self._valchnage(value)
        else:
            self.parent.points[self._key][3][0] = self._valchnage(value) 