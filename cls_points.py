#!/usr/bin/python 
# FLC 2013

import math
import numpy as np
import numbers
import obj_data

class _points(object):

    """**Points class:** 
        
        .. _points_cls:
        
        :platform: Unix, Windows
        :synopsis: Allows to add, operate and edit points in a 3D space
        
        :properties:
            * Get a point by unique id. (pto = pyTikZ.pto[id])
            * Set a point by unique id. (pyTikZ.pto[id]=pto). When set just the coordinates are changed.
            * Iterate points as point object
        
        **Chracteristics of a point (pto) object**
        
        :ivar id: get unique id of the point
        :ivar alias: set/get alias name of the point
        :ivar x: set/get x coordinate property
        :ivar y: set/get y coordinate property
        :ivar z: set/get z coordinate property
        :ivar xyz: set/get the three coordinates
        :ivar layer: set/get layer member property
        :ivar info: get formated text with point info
                
        :Operations:
            * **equality (pto1 == pto2):** check the three coordinates are the same
            * **sum (pto1 + pto2):** allow to sum to points as it were two vectors
            * **sum (pto1 + real):** sum to all the coordinates the real number
            * **diff (pto1 - pto2):** allow to subtracts to points as it were two vectors
            * **diff (pto1 - real):** substract to all the coordinates the real number
            * **multiplication (pto1 * pto2):** multiplicate each coordinate by the other
            * **multiplication (pto1 * real):** multiplicate each coordinate by the real number
            * **print (print pto1):** prints the point info
            * **copy (pto3 = pto1.copy(alias)):** deepcopy of a point (diferent unique id)
        
    """
    
    """
        Future functions:
            * Export points to csv and txt file (separate by ;)
            * Import points to csv and txt file (separate by ;)
            * Add scale of ptos
            * Translation of a point function -- April 2016
            * Rotation of a point function -- April 2016
            * Show points -- April 2016
    
    """

    def __init__(self, parent):
        
        self.parent = parent
        self.auto_save_aux = False      
        
        ### Counters
        self.counters = obj_data._clsdata(type = int(0)) 
        
        ### Dictionary of points
        self.points = obj_data._clsdata(type = [])
        self.counters["points"] = 0
    
    ###################################### Internal
    
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
    
    def _type_of_point(self):
        ### Returns the type of point
        return type(_point(self,None))
        
    def _choices(self, v):
        ### returns the point object, v types: as id, alias or point
        if type(v) == type(""):
            #empty name
            if v == "":
                self.parent.error("Wrong point format while adding a point, empty string. In addpto.", ref = "")  
            #id or alias
            if v[0] == "#":
                pt = self.parent.pto[v]
            else:
                pt = self.parent.pto.alias(v)
            #return point
            if pt is None:
                self.parent.error("Wrong point format while adding a point, empty string. In addpto.", ref = "")        
            else:
                return pt
        elif type(v) == self.parent.pto._type_of_point():
            return v
        else:
            self.parent.error("Wrong point format while adding a point. In addpto.", ref = "")            
    
    def _check_alias(self, alias):
        ### Check alias possibilities
        
        if alias == "":
            return True
        if type(alias) == type(""):
            if alias[0] == "#":
                self.parent.error("Alias name can not start with a # character. In _check_alias")
            else:
                if self.alias(alias) is None:
                    return True
                else:
                    self.parent.error("Alias already exist. In _check_alias")
        else:   
            self.parent.error("Alias of point is not a string value. In _check_alias")
    
    def _point_format(self, x, y, z = 0, layer = 0, alias = ""):
        ### Bottle neck point
        self._check_alias(alias)
        return [x,y,z,[int(layer)],str(alias)]
    
    def addpoint(self, x, y, z = 0, layer = 0, alias = ""):
        # Create new point
        _key =  "#%i" % self.counters["points"]
        self.counters["points"] = self.counters["points"] + 1
        self.points[_key] = self._point_format(x, y, z = z , layer = layer, alias = alias)
        return self.point(_key)
    
    def auxpoint(self, x=0, y=0, z = 0, layer = 0):
        # Create new auxiliary
        lst = self._point_format(x, y, z = z , layer = layer)
        p = _point(self, None, lst)
        if self.auto_save_aux: p.save()
        return p   
       
    ###################################### Functions
    
    def pto(self, x=0, y=0, z=0, layer = 0, alias = ""):
    
        """
        
        .. _points_pto:         
                
        **Synopsis:**
            * Add a new point
        
        **Args:**
            * x=0: x coordinate
            * y=0: y coordinate
            * z=0: z coordinate
            * layer = 0: layer member
            * alias = "": alias name            
            
        **Returns:**
            * A point object with the x, y, z, layer and name properties
            
        .. note::
        
            * See example
        
        """     
        
        return self.addpoint(x, y, z = z, layer = layer, alias = alias)
        
    def aux(self, x=0, y=0, z = 0, layer = 0):
    
        """
        
        .. _points_aux:         
                
        **Synopsis:**
            * Add an new auxiliary point
        
        **Args:**
            * x=0: x coordinate
            * y=0: y coordinate
            * z=0: z coordinate
            * layer = 0: layer member
            
        **Returns:**
            * A point object with the x, y, z, layer and name properties
            
        .. note::
        
            * Auxiliary points do not have unique id
            * Atribute .save() asign a unique id to an auxiliary point
        
        """    
        
        return self.auxpoint(x=x, y=y, z = z, layer = layer)
        
    def alias(self, alias):
    
        """
        
        .. _alias:         
                
        **Synopsis:**
            * Return a point by alias
        
        **Args:**
            * alias: point alias
            
        **Returns:**
            * The first point object with such alias
            
        .. note::
        
            * Alias can be empty or be a unique identification. Can not start with a **#** character.
        
        """    
        
        for ii in range(0,self.counters["points"]):
            
            _key =  "#%i" % ii
            
            p = self.point(_key)
            
            if p is not None:
                if p.alias == str(alias): return p
        
        return None  

    def translate(self, ptos, x = 0., y = 0., z = 0.):
    
        """
        
        .. _pto_translate:         
                
        **Synopsis:**
            * Translate a point of list of points in a 3D space
        
        **Args:**
            * ptos: multiple points. Can be set as a point, a list o points, an alias or a list of alias. See :ref:`addpto examples <ex_shapes_addpto>`
            
        **Optional parameters:**
            * x = 0: increment in x coordinate to tranlate
            * y = 0: increment in y coordinate to tranlate
            * z = 0: increment in z coordinate to tranlate
            
        **Returns:**
            * None
            
        .. note::
            
            * See :ref:`addpto examples <ex_shapes_addpto>`
            * See :ref:`example 3 <ex_points_ex3>`
        
        """    
        
        if type(ptos) is type([]):       
            for v in ptos:
                _pto = self._choices(v)
                _pto.x = _pto.x + x
                _pto.y = _pto.y + y
                _pto.z = _pto.z + z
        else:
            _pto = self._choices(ptos)
            _pto.x = _pto.x + x
            _pto.y = _pto.y + y
            _pto.z = _pto.z + z 
            
    def translate_to(self, ptos, pto_ref, pto_ref_final):
    
        """
        
        .. _pto_translate_to:         
                
        **Synopsis:**
            * Given a reference point and a final position for such point. Translate a point or list of points in a 3D space in a similar manner.
        
        **Args:**
            * ptos: multiple points. Can be set as a point, a list o points, an alias or a list of alias. See :ref:`addpto examples <ex_shapes_addpto>`
            
        **Optional parameters:**
            * pto_ref: reference point
            * pto_ref_final: final refence point position
            
        **Returns:**
            * None
            
        .. note::
            
            * See :ref:`addpto examples <ex_shapes_addpto>`
            * See :ref:`example 3 <ex_points_ex3>`
        
        """    
        
        ix = pto_ref_final.x - pto_ref.x
        iy = pto_ref_final.y - pto_ref.y
        iz = pto_ref_final.z - pto_ref.z
        
        if type(ptos) is type([]):       
            for v in ptos:
                _pto = self._choices(v)
                _pto.x = _pto.x + ix
                _pto.y = _pto.y + iy
                _pto.z = _pto.z + iz
        else:
            _pto = self._choices(ptos)
            _pto.x = _pto.x + ix
            _pto.y = _pto.y + iy
            _pto.z = _pto.z + iz             
            
    def rotate(self, ptos, pto_rotation, Ax = 0., Ay = 0., Az = 0.):
    
        """
        
        .. _pto_rotate:         
                
        **Synopsis:**
            * Rotate a point of list of points in a 3D space respect an origin point
        
        **Args:**
            * ptos: multiple points. Can be set as a point, a list o points, an alias or a list of alias. See :ref:`addpto examples <ex_shapes_addpto>`
            * pto_rotation: center point of rotation
            
        **Optional parameters:**
            * Ax = 0.: yaw angle in degrees to turn respect axis X
            * Ay = 0.: pitch angle in degrees to turn respect axis Y
            * Az = 0.: roll angle in degrees to turn respect axis Z
            
        **Returns:**
            * None
            
        .. note::
        
            * See :ref:`addpto examples <ex_shapes_addpto>`
            * See :ref:`example 3 <ex_points_ex3>`
        
        """
        def _rotation_matrix(Ax,Ay,Az):
            
            AAx,AAy,AAz = Ax*np.pi/180.,Ay*np.pi/180.,Az*np.pi/180.
            Rx = np.matrix([[1.,0.,0.], [0.,np.cos(AAx),-np.sin(AAx)], [0., np.sin(AAx), np.cos(AAx)]])
            Ry = np.matrix([[np.cos(AAy),0.,np.sin(AAy)], [0.,1.,0.], [-np.sin(AAy), 0., np.cos(AAy)]])
            Rz = np.matrix([[np.cos(AAz),-np.sin(AAz),0.], [np.sin(AAz),np.cos(AAz),0.], [0., 0., 1.]])
            
            return (Rx*Ry)*Rz
            
        def _rotate(self,_pto,pto_rotation,R):
            #Tranlate to oringin
            if type(pto_rotation) == self._type_of_point():
                trans = pto_rotation
                tx,ty,tz = trans.x,trans.y,trans.z
                self.translate(_pto, x = tx, y = ty, z = tz)
            else:
                self.parent.error("Origing point in translate not a point")
            #Rotate
            x, y, z = _pto.x, _pto.y, _pto.z
            
            _pto.x = x * R[0,0] + y * R[0,1] + z * R[0,2]
            _pto.y = x * R[1,0] + y * R[1,1] + z * R[1,2]
            _pto.z = x * R[2,0] + y * R[2,1] + z * R[2,2]
            
            #Un-translate to origin
            if type(pto_rotation) == self._type_of_point():
                self.translate(_pto, x = -tx, y = -ty, z = -tz)
            
        ### Check lists
        R = _rotation_matrix(Ax,Ay,Az)
        
        if type(ptos) is type([]):       
            for v in ptos:
                _pto = self._choices(v)
                _rotate(self,_pto,pto_rotation,R)
        else:
            _pto = self._choices(ptos)
            _rotate(self,_pto,pto_rotation,R)            
        
    def copy(self, ptos, alias_prefix = "", alias_sufix = ""):
    
        """
        
        .. _pto_copy:         
                
        **Synopsis:**
            * Returns a copy of the list of points
        
        **Args:**
            * ptos: multiple points. Can be set as a point, a list o points, an alias or a list of alias. See :ref:`addpto examples <ex_shapes_addpto>`
            
        **Optional parameters:**
            * alias_sufix = "": Add a sufix to the alias of each point
            * alias_prefix = "": Add a prefix to the alias of each point
            
        **Returns:**
            * List of points copied, with the alias modified
            
        .. note::
        
            * If alias_sufix and alias_prefix is "", an empty alias for each copied point is return
            * See :ref:`addpto examples <ex_shapes_addpto>`
            * See :ref:`example 3 <ex_points_ex3>`
        
        """    
        lst_out = []
        if len(ptos) == 0: return []
        
        if type(ptos) is type([]):       
            for v in ptos:
                _pto = self._choices(v)
                
                _alias = _pto.alias
                if alias_prefix != "" and type(alias_prefix) == type(""):
                    _alias = alias_prefix + _alias
                if alias_sufix != "" and type(alias_sufix) == type(""):
                    _alias = _alias + alias_sufix
                if _alias == _pto.alias: _alias = "" 
                
                lst_out.append(_pto.copy(alias = _alias))
        else:
            _pto = self._choices(ptos)
            
            _alias = _pto.alias
            if alias_prefix != "" and type(alias_prefix) == type(""):
                _alias = alias_prefix + _alias
            if alias_sufix != "" and type(alias_sufix) == type(""):
                _alias = _alias + alias_sufix            
            if _alias == _pto.alias: _alias = ""
            
            lst_out.append(_pto.copy(alias = _alias))
        
        return lst_out
        
    def draw_points(self, ptos = None, mark_radius = 1, color = "", label = "#marker_points", layer = -1e-10):
    
        """
        .. _draw_points:         
                
        **Synopsis:**
            * Draw a list of points with a marker
            * If no list of points is given, all the points are draw with a marker
            
        **Args:**
            * ptos = None: multiple points. Can be set as a point, a list o points, an alias or a list of alias. See :ref:`addpto examples <ex_shapes_addpto>`
            
        **Optional parameters:**
            * mark_radius = 1: scale of marker size
            * color = "": color of the marker
            * label = "#marker_points": label added to the markers
            * layer = -1e-10: layer were the markers belong
            
        **Returns:**
            * None
            
        .. note::
        
            * See :ref:`example 3 <ex_points_ex3>`
        
        """ 
        if ptos is None:
            ptos = self._all_points()
            
        self._draw_list_points(ptos, mark_radius = mark_radius, \
                               color = color, label = label, layer = layer)
        
        return None
    
    ###################################### Internal
    def _all_points(self):
        ### Return a list with all points
        lst_out = []        
        
        ### Check all points
        for key, value in self.points._data.iteritems():
            if key[0] == "#":
                p = self.point(key)
                lst_out.append(p.id)
               
        ### Call all shapes
        for key, value in self.parent.shp.shapes._data.iteritems():
            if key[0] == "#":
                for p in self.parent.shp[key].addpto:
                    if p.id in lst_out:
                        pass
                    else:
                        lst_out.append(p)
        
        return lst_out
        
    def _canavas_size(self, ptos):
        ### Return canavas cube from a list of points [[max_x,_min_x],[max_y,_min_y],[max_z,_min_z]]
                
        def _max_min_canavas(_canavas, x, y, z):
            # [[max_x,min_x],[max_y,min_y],[max_z,min_z]] = self._canavas
            #_canavas = [[0.,0.],[0.,0.],[0.,0.]]
            
            if x > _canavas[0][1]: _canavas[0][1] = x
            if x < _canavas[0][0]: _canavas[0][0] = x
            
            if y > _canavas[1][1]: _canavas[1][1] = y
            if y < _canavas[1][0]: _canavas[1][0] = y

            if z > _canavas[2][1]: _canavas[2][1] = z
            if z < _canavas[2][0]: _canavas[2][0] = z        
            
            return _canavas        
        
        start = True
        # Iterate list of points
        if type(ptos) is type([]): 
            for pto in ptos:
                p = self._choices(pto)
                if start:
                    start = False
                    _canavas = [[p.x,p.x],[p.y,p.y],[p.z,p.z]]
                else:
                    _canavas = _max_min_canavas(_canavas, p.x, p.y, p.z)
        else:
            p = self._choices(ptos)
            if start:
                start = False
                _canavas = [[p.x,p.x],[p.y,p.y],[p.z,p.z]]
            else:
                _canavas = _max_min_canavas(_canavas, p.x, p.y, p.z)                    
        
        ### Get values
        [[min_x,max_x],[min_y,max_y],[min_z,max_z]] = _canavas
        
        ### Space lengths
        size_x, size_y, size_z = max_x - min_x, max_y - min_y, max_z - min_z
        
        ### Max length
        max_size = abs(size_x)
        if abs(size_y) > max_size: max_size = size_y
        if abs(size_z) > max_size: max_size = size_z
        
        return size_x, size_y, size_z, max_size, _canavas
        
    def _draw_list_points(self, ptos, mark_radius = 1, color = "", label = "#marker_points", layer = -1e-10):
        ### Draw markers for a list of points
        
        # Find max sizes of drawing. Canavas
        size_x, size_y, size_z, max_size, _canavas = self._canavas_size(ptos)
        s = max_size / 200.
        s_mark_radius = mark_radius * s
        
        # draw marker
        def _draw_marker(self, pto, mark_radius, color, layer, label):
            if pto.id is None: return
            x,y,z = pto.x,pto.y,pto.z
            p1 = self.auxpoint(x=x+mark_radius, y=y, z=z, layer = layer)
            p2 = self.auxpoint(x=x-mark_radius, y=y, z=z, layer = layer)
            l = self.parent.shp.line(p1,p2,color=color,layer=layer)
            l.addlabel = label            
            p1 = self.auxpoint(x=x, y=y+mark_radius, z=z, layer = layer)
            p2 = self.auxpoint(x=x, y=y-mark_radius, z=z, layer = layer)
            l = self.parent.shp.line(p1,p2,color=color,layer=layer)
            l.addlabel = label
            p1 = self.auxpoint(x=x, y=y, z=z+mark_radius, layer = layer)
            p2 = self.auxpoint(x=x, y=y, z=z-mark_radius, layer = layer)
            l = self.parent.shp.line(p1,p2,color=color,layer=layer)
            l.addlabel = label               
            
        # Iterate list of points
        if type(ptos) is type([]): 
            for pto in ptos:
                _p = self._choices(pto)
                _draw_marker(self, _p, s_mark_radius, color, layer, label)
        else:
            _p = self._choices(ptos)
            _draw_marker(self, _p, s_mark_radius, color, layer, label)                 
        
#################################################        
################# Point object ##################        
#################################################        
        
class _point(object):
   
    def __init__(self, parent, key, lst = []):
        
        self.parent = parent
        self._key = key
        self._lst = lst
    
    ######################## Operators        
    def __eq__(self, other):
        ### equality
        if isinstance(other, self.__class__):
            if self.x == other.x:
                if self.y == other.y:
                    if self.z == other.z:
                        return True
            return False
        else:
            return False

    def __ne__(self, other):
        ### not equality
        return not self.__eq__(other)    
    
    def _add(self, other):
        ### summatory
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
        ### summatory
        return self._add(other)
        
    def __radd__(self, other):
        ### difference
        return self._add(other)

    def __sub__(self, other) :  
        ### substraction
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
        ### reverse substraction
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

    def _mul(self, other) :
        ### multiplication
        if isinstance(other, self.__class__):
            p = self.parent.auxpoint()
            if self.id == other.id: p = self
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
            
    def __mul__(self, other) :  
        ### multiplication
        return self._mul(other) 
            
    def __rmul__(self, other) :  
        ### reverse multiplication
        return self._mul(other)               
        
    def __repr__(self):
        return self.id
        
    def __str__(self):
        return self.info
        
    ######################## Functions
    def save(self):
        p = self.parent.addpoint(self.x, self.y, z = self.z , layer = self.layer, alias = self.alias)
        self._key = p.id
        return p
        
    def copy(self, alias = ""):
        
        if self._key is not None:
            if alias == "" or alias is None:
                p = self.parent.addpoint(self.x, self.y, z = self.z , layer = self.layer)
            else:
                p = self.parent.addpoint(self.x, self.y, z = self.z , layer = self.layer, alias = alias)
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
    def info(self):
        return "Point key:%s x=%.4f y=%.4f z=%.4f layer=%i alias=%s NumPoints:%i" % (self.id, self.x, self.y, self.z, self.layer, self.alias,len(self.parent.points))           
            
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
    def xyz(self): 
        return self.parent.points[self._key][0],self.parent.points[self._key][1],self.parent.points[self._key][2]
        
    @xyz.setter 
    def xyz(self, value): 
        if isinstance(value, self.__class__):
            if self._key is None:
                self.x = self._valchnage(value.x)
                self.y = self._valchnage(value.y)
                self.z = self._valchnage(value.z)
            else:
                self.parent.points[self._key][0] = self._valchnage(value.x)
                self.parent.points[self._key][1] = self._valchnage(value.y)
                self.parent.points[self._key][2] = self._valchnage(value.z)
        else:
            pass
            
    @property
    def layer(self):
        if self._key is None:
            return self._lst[3][0]
        else:
            return self.parent.points[self._key][3][0]

    @layer.setter
    def layer(self, value):        
        if self._key is None:
            self._lst[3][0] = self._valchnage(value)
        else:
            self.parent.points[self._key][3][0] = self._valchnage(value)
            
    @property
    def alias(self):
        if self._key is None:
            return self._lst[4]
        else:
            return self.parent.points[self._key][4]

    @alias.setter
    def alias(self, value):        
        if self._key is None:
            self._lst[4] = value
        else:
            self.parent.points[self._key][4] = value
            