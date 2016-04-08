#!/usr/bin/python 
# FLC 2013

import math
import numbers
import obj_data
import copy

def log(txt):
    
    print txt

class _shapes(object):

    """**Shapes class:** 
    
    .. _shapes_cls:
   
    :platform: Unix, Windows
    :synopsis: Allows to add 2D shapes using points
    
    :properties:
        * Possible shapes
            * Line between two points. See :ref:`shp.line <shapes_line>`
            * Path of multiple points. See :ref:`shp.path <shapes_path>`
            * Rectangle given by two corners
            * Circle given by center and radius
            * Arc given by starting point, radius and angles
            * Grid rectangle
            * Text frame
            * Parabola given by three points
        * Shapes allow to set labels (see labels section)
    
    **Chracteristics of a shape (shp) object**
    
        * Each shape object has different properties depending on the nature of the shape
    
    """
    
    """
        For the furture:
            * Add mapbits, images
            * Translate and rotation
    """
    
    def __init__(self, parent):
        
        self.parent = parent
        
        ### Counters
        self.counters = obj_data._clsdata(type = int(0))
        
        ### Dictionary of lines
        self.shapes = obj_data._clsdata(type = {})
        self.counters["shapes"] = 0    
        
    def __getitem__(self, key):
    
        return self.getitem(key)        
        
    def keys(self):
        
        return self.shapes.keys
        
    def getitem(self, key):        
        
        ### Give a point
        _key = str(key)
        
        if self.shapes[_key]:
            return _shape(self,_key)
        else:
            return None            

    def line(self, p1, p2, layer = 0, thick = "", type = "", color = "", fill = ""):
        """
        .. _shapes_line:         
                
        **Synopsis:**
            * Add a line shape or segment between two points
        
        **Args:**
            * p1: segment start point (given by id, alias or point object)
            * p2: segment end point (given by id, alias or point object)
            
        **Optional parameters:**
            * layer = 0: layer member where the shape belongs
            * thick = "": line thickness (see :ref:`thick examples <ex_shapes_thick>`)
            * type = "": type of line (see :ref:`type examples <ex_shapes_type>`)
            * color = "": color of the line (see :ref:`colors examples <ex_shapes_color>`)
            * fill = "": fill texture of the line (see fill examples)
            
        **Returns:**
            * A line shape object
           
        **Chracteristics of a shape line object**
        
        :ivar id: get unique id of the point
        :ivar action: get type of shape object
        :ivar zorder: set/get z position respect the drawing plane and viewer
        :ivar labels: get labels to which the shape belongs
        :ivar addlabel: set/get add a label to the shape
        :ivar comment: multifunctional text field
        
        :ivar arrow: set/get arrow parameters (see arrows examples)
        :ivar arrow_build(start,end,scale): arrow parameter (see arrows examples)
        :ivar thick: set/get line thickness (see :ref:`thick examples <ex_shapes_thick>`)
        :ivar type: set/get type of line (see :ref:`type examples <ex_shapes_type>`)
        :ivar color: set/get color of the line (see :ref:`colors examples <ex_shapes_color>`)
        :ivar fill: set/get fill texture of the line (see fill examples)  
        
        :ivar addpto: set or add a new points to the line. Get a list of points that form the line. See :ref:`addpto examples <ex_shapes_addpto>`
           
        .. note::
        
            * See example of lines 
        
        """     
        
        item = self._additem("line", layer = layer)
        item.addpto = p1
        item.addpto = p2
        if thick != "": item.thick = thick
        if type != "":  item.type = type
        if color != "": item.color = color
        if fill != "": item.fill = fill
        return item       
        
    def path(self, ptos, layer = 0, thick = "", type = "", color = "", fill = ""):
        """
        .. _shapes_path:         
                
        **Synopsis:**
            * Add a path of multiple points connected by a line
        
        **Args:**
            * ptos: multiple points. Can be set as a point, a list o points, an alias or a list of alias. See :ref:`addpto examples <ex_shapes_addpto>`
            
        **Optional parameters:**
            * layer = 0: layer member where the shape belongs
            * thick = "": line thickness (see :ref:`thick examples <ex_shapes_thick>`)
            * type = "": type of line (see :ref:`type examples <ex_shapes_type>`)
            * color = "": color of the line (see :ref:`colors examples <ex_shapes_color>`)
            * fill = "": fill texture of the line (see fill examples)
            
        **Returns:**
            * A path shape object
           
        **Chracteristics of a shape line object**
        
        :ivar id: get unique id of the point
        :ivar action: get type of shape object
        :ivar zorder: set/get z position respect the drawing plane and viewer
        :ivar labels: get labels to which the shape belongs
        :ivar addlabel: set/get add a label to the shape
        :ivar comment: multifunctional text field
        
        :ivar arrow: set/get arrow parameters (see arrows examples)
        :ivar arrow_build(start,end,scale): arrow parameter (see arrows examples)
        :ivar thick: set/get line thickness (see :ref:`thick examples <ex_shapes_thick>`)
        :ivar type: set/get type of line (see :ref:`type examples <ex_shapes_type>`)
        :ivar color: set/get color of the line (see :ref:`colors examples <ex_shapes_color>`)
        :ivar fill: set/get fill texture of the line (see fill examples)       
        
        :ivar addpto: set or add a new points to the line. Get a list of points that form the line. See :ref:`addpto examples <ex_shapes_addpto>`
        
        .. note::
        
            * See example of paths 
        
        """    
        
        item = self._additem("path", layer = layer)
        item.addpto = ptos
        if thick != "": item.thick = thick
        if type != "":  item.type = type
        if color != "": item.color = color
        if fill != "": item.fill = fill
        return item  

    def rectangle(self, layer = 0):
        
        return self._additem("rectangle", layer = layer)   

    def circle(self, pto, radius, layer = 0, thick = "", type = "", color = "", fill = ""):       
        """
        .. _shapes_circle:         
                
        **Synopsis:**
            * Add a circle defined by the centre and the radius
        
        **Args:**
            * pto: point of the centre of the circle (given by id, alias or point object)
            * radius: radius of the circle
            
        **Optional parameters:**
            * layer = 0: layer member where the shape belongs
            * thick = "": line thickness (see :ref:`thick examples <ex_shapes_thick>`)
            * type = "": type of line (see :ref:`type examples <ex_shapes_type>`)
            * color = "": color of the line (see :ref:`colors examples <ex_shapes_color>`)
            * fill = "": fill texture of the line (see fill examples)
            
        **Returns:**
            * A circle shape object
           
        **Chracteristics of a shape circle object**
        
        :ivar id: get unique id of the point
        :ivar action: get type of shape object
        :ivar zorder: set/get z position respect the drawing plane and viewer
        :ivar labels: get labels to which the shape belongs
        :ivar addlabel: set/get add a label to the shape
        :ivar comment: multifunctional text field
        
        :ivar arrow: set/get arrow parameters (see arrows examples)
        :ivar arrow_build(start,end,scale): arrow parameter (see arrows examples)
        :ivar thick: set/get line thickness (see :ref:`thick examples <ex_shapes_thick>`)
        :ivar type: set/get type of line (see :ref:`type examples <ex_shapes_type>`)
        :ivar color: set/get color of the line (see :ref:`colors examples <ex_shapes_color>`)
        :ivar fill: set/get fill texture of the line (see fill examples)       
                
        .. note::
        
            * See example of circles 
        
        """        
        
        item = self._additem("circle", layer = layer)          
        item.radius = float(radius)
        item.addpto = pto
        if thick != "": item.thick = thick
        if type != "":  item.type = type
        if color != "": item.color = color
        if fill != "": item.fill = fill        
        
        return item
        
    def arc(self, start_point, radius, start_angle, end_angle, layer = 0, thick = "", type = "", color = "", fill = ""):
        """
        .. _shapes_arc:         
                
        **Synopsis:**
            * Add an arc defined by the starting point, radius, start angle and end angle
        
        **Args:**
            * start_point: starting point of the arc (given by id, alias or point object)
            * radius: radius of the arc
            * start_angle: start angle in degrees
            * end_angle: end angle in degrees
            
        **Optional parameters:**
            * layer = 0: layer member where the shape belongs
            * thick = "": line thickness (see :ref:`thick examples <ex_shapes_thick>`)
            * type = "": type of line (see :ref:`type examples <ex_shapes_type>`)
            * color = "": color of the line (see :ref:`colors examples <ex_shapes_color>`)
            * fill = "": fill texture of the line (see fill examples)
            
        **Returns:**
            * An arc shape object
           
        **Chracteristics of a shape arc object**
        
        :ivar id: get unique id of the point
        :ivar action: get type of shape object
        :ivar zorder: set/get z position respect the drawing plane and viewer
        :ivar labels: get labels to which the shape belongs
        :ivar addlabel: set/get add a label to the shape
        :ivar comment: multifunctional text field
        
        :ivar arrow: set/get arrow parameters (see arrows examples)
        :ivar arrow_build(start,end,scale): arrow parameter (see arrows examples)
        :ivar thick: set/get line thickness (see :ref:`thick examples <ex_shapes_thick>`)
        :ivar type: set/get type of line (see :ref:`type examples <ex_shapes_type>`)
        :ivar color: set/get color of the line (see :ref:`colors examples <ex_shapes_color>`)
        :ivar fill: set/get fill texture of the line (see fill examples)       
                
        .. note::
        
            * See example of arcs
        
        """         
        
        # Angles in degrees
        item = self._additem("arc", layer = layer)          
        item.radius = float(radius)
        item.start_angle = float(start_angle)
        item.end_angle = float(end_angle)
        item.addpto = start_point
        
        return item        
        
    def grid(self, step, xstep = 0, ystep = 0, layer = 0):
        
        item = self._additem("grid", layer = layer)          
        item.step = [step, xstep, ystep]
        
        return item
        
    def text(self, pto, text, layer = 0):
        
        item = self._additem("text", layer = layer)          
        item.text = text
        item.addpto = pto
        
        return item  
    
    def parabola(self, pto1, ptobend, pto2, layer = 0):
        
        item = self._additem("parabola", layer = layer)          
        item.addpto = pto1
        item.addpto = ptobend
        item.addpto = pto2
        
        return item        
        
    def _additem(self, type, layer = 0):
        
        # Create auto new
        _key =  "#%i" % self.counters["shapes"]
        self.counters["shapes"] = self.counters["shapes"] + 1
        self.shapes[_key] = {}
        
        lline = _shape(self,_key)
        lline.layer = layer
        lline.action = type
        lline.addlabel = "default"
        return lline
    
    #########################
    @property
    def labels(self):
        return self.parent.lbl.labels
    
    @property
    def addlabel(self):
        return self.labels
        
    @addlabel.setter
    def addlabel(self, value):
        self.parent.lbl.addlabel = value        
            
    def dellabel(self, value):
        if value in self.labels:
            
            ### Delete from all the shapes
            for key in self.keys():
                shp = self.getitem(key)             
                shp.dellabel(value)
            
            ### Remake list
            self.parent.lbl._dellabel(value)
            
            return True
        else:
            #log("The label %s has not been previously declared" % value)   
            return False

    def rename_label(self, name_old, name_new):
        if name_old != name_new:            
                        
            ### Add new name
            self.addlabel=name_new
            
            ### Delete from all the shapes
            for key in self.keys():
                shp = self.getitem(key)             
                if name_old in self.shapes[key]["labels"]:
                    shp.dellabel(name_old)
                    shp.addlabel=name_new
            
            ### Remake list
            self.parent.lbl._dellabel(name_old)
            
            return True
        else:
            #log("Inconsistent")            
            return False
            
class _shape(object):
   
    def __init__(self, parent, key):
        
        self.parent = parent
        self._key = key
        self._draw = False
        
        if not self.parent.shapes[key]:
        
            self.parent.shapes[self._key]["action"] = ""
            self.parent.shapes[self._key]["layer"] = 0
            self.parent.shapes[self._key]["z-order"] = 0.
            self.parent.shapes[self._key]["labels"] = []
            self.parent.shapes[self._key]["group_label"] = None
            
            self.parent.shapes[self._key]["comment"] = ""
            self.parent.shapes[self._key]["ptos"] = []
            self.parent.shapes[self._key]["arrow"] = ""
            self.parent.shapes[self._key]["thick"] = ""
            self.parent.shapes[self._key]["type"] = ""
            self.parent.shapes[self._key]["color"] = ""
            self.parent.shapes[self._key]["fill"] = ""
            self.parent.shapes[self._key]["radius"] = 1.
            self.parent.shapes[self._key]["start_angle"] = 0.
            self.parent.shapes[self._key]["end_angle"] = 90.
            self.parent.shapes[self._key]["step"] = []
            self.parent.shapes[self._key]["text"] = ""
            self.parent.shapes[self._key]["position"] = ""
            self.parent.shapes[self._key]["align"] = ""
            self.parent.shapes[self._key]["textsize"] = ""
            self.parent.shapes[self._key]["rotate_text"] = 0.
            
    
    #############################################
    
    def copy(self):
            
        shp = self.parent._additem(self.action, layer = self.layer)
        
        for key in self.parent.shapes[self.id].keys():
            
            self.parent.shapes[shp.id][key] = copy.deepcopy(self.parent.shapes[self.id][key])
           
    def move(self, mpto):
        
        lst = []
        
        for pto in self.addpto:        
            
            lst.append( pto.copy() )
            new_pto = lst[-1]
            
            new_pto.x = new_pto.x + mpto.x
            new_pto.y = new_pto.y + mpto.y
            new_pto.z = new_pto.z + mpto.z
            
        self.parent.shapes[self._key]["ptos"] = copy.deepcopy(lst)   
    
    def build_tik_string(self, units = ""):
        
        str = ""
        
        if self.action == "line" or self.action == "path":
            
            opt = ""
            if self.arrow != "": opt += self.arrow.replace("##units##",units) + " ,"
            if self.thick != "": opt += self.thick.replace("##units##",units) + " ,"
            if self.type != "": opt += self.type.replace("##units##",units) + " ,"
            if self.color != "": opt += self._color_build() + " ,"
            if self.fill != "": opt += " fill= " + self.fill + " ,"
            if len(opt) > 0: opt = "[" + opt[:-2] + "] "
            
            ptos = ""
            if len(self.addpto) >= 2:
                for ii in range(0,len(self.addpto)):
                    pto = self.addpto[ii]
                    ptos += "(%.4f%s,%.4f%s,%.4f%s) -- " % (pto.x, units, pto.y, units, pto.z, units)
                if len(ptos) > 0: ptos = ptos[:-4]
            else:
                log("Less than two point for the line %s" % self.id)
            
            
            str = r"\draw %s %s;" % (opt, ptos)
            #str = r"\path %s %s;" % (opt, ptos) ### Invisible lines, intersection
            
        if self.action == "rectangle":

            opt = ""
            #if self.arrow != "": opt += self.arrow.replace("##units##",units) + " ,"
            if self.thick != "": opt += self.thick.replace("##units##",units) + " ,"
            if self.type != "": opt += self.type.replace("##units##",units) + " ,"
            if self.color != "": opt += self._color_build() + " ,"
            if self.fill != "": opt += " fill= " + self.fill + " ,"
            if len(opt) > 0: opt = "[" + opt[:-2] + "] "
            
            ptos = ""
            if len(self.addpto) >= 2:
                for ii in range(0,2):
                    pto = self.addpto[ii]
                    ptos += "(%.4f%s,%.4f%s,%.4f%s) rectangle " % (pto.x, units, pto.y, units, pto.z, units)
                if len(ptos) > 0: ptos = ptos[:-11]
            else:
                log("Less than two point for the rectangle %s" % self.id)            
            
            str = r"\draw %s %s;" % (opt, ptos)   
        
        if self.action == "circle":
            
            opt = ""
            #if self.arrow != "": opt += self.arrow.replace("##units##",units) + " ,"
            if self.thick != "": opt += self.thick.replace("##units##",units) + " ,"
            if self.type != "": opt += self.type.replace("##units##",units) + " ,"
            if self.color != "": opt += self._color_build() + " ,"
            if self.fill != "": opt += " fill= " + self.fill + " ,"
            if len(opt) > 0: opt = "[" + opt[:-2] + "] "
            
            ptos = ""
            if len(self.addpto) > 0:
                pto = self.addpto[0]
                ptos = "(%.4f%s,%.4f%s,%.4f%s) circle [radius=%.4f%s]" % (pto.x, units, pto.y, units, pto.z, units, float(self.radius), units)
            else:
                log("Less than one point for the circle %s" % self.id)   

            str = r"\draw %s %s;" % (opt, ptos)  

        if self.action == "arc":
            
            opt = ""
            if self.arrow != "": opt += self.arrow.replace("##units##",units) + " ,"
            if self.thick != "": opt += self.thick.replace("##units##",units) + " ,"
            if self.type != "": opt += self.type.replace("##units##",units) + " ,"
            if self.color != "": opt += self._color_build() + " ,"
            if self.fill != "": opt += " fill= " + self.fill + " ,"
            if len(opt) > 0: opt = "[" + opt[:-2] + "] "
            
            ptos = ""
            if len(self.addpto) > 0:
                pto = self.addpto[0]
                ptos = "(%.4f%s,%.4f%s,%.4f%s) arc [radius=%.4f%s, start angle=%.4f%s, end angle=%.4f%s]" % \
                (pto.x, units, pto.y, units, pto.z, units, float(self.radius), units, float(self.start_angle), units, float(self.end_angle), units)
            else:
                log("Less than one point for the arc %s" % self.id)   

            str = r"\draw %s %s;" % (opt, ptos)
            
        if self.action == "grid":

            opt = ""
            #if self.arrow != "": opt += self.arrow.replace("##units##",units) + " ,"
            if self.thick != "": opt += self.thick.replace("##units##",units) + " ,"
            if self.type != "": opt += self.type.replace("##units##",units) + " ,"
            if self.color != "": opt += self._color_build() + " ,"
            if self.fill != "": opt += self.fill + " ,"
            if self.step[2] != 0: opt += "ystep=%.4f ," % self.step[2]
            if self.step[1] != 0: opt += "xstep=%.4f ," % self.step[1]
            if self.step[0] != 0: opt += "step=%.4f ," % self.step[0]            
            if len(opt) > 0: opt = "[" + opt[:-2] + "] "
            
            ptos = ""
            if len(self.addpto) >= 2:
                for ii in range(0,2):
                    pto = self.addpto[ii]
                    ptos += "(%.4f%s,%.4f%s,%.4f%s) grid " % (pto.x, units, pto.y, units, pto.z, units)
                if len(ptos) > 0: ptos = ptos[:-11]
            else:
                log("Less than two point for the grid %s" % self.id)            
            
            str = r"\draw %s %s;" % (opt, ptos)   

        if self.action == "text":

            opt = ""
            #if self.arrow != "": opt += self.arrow.replace("##units##",units) + " ,"
            #if self.thick != "": opt += self.thick.replace("##units##",units) + " ,"
            #if self.type != "": opt += self.type.replace("##units##",units) + " ,"
            if self.color != "": opt += self._color_build() + " ,"
            #if self.fill != "": opt += self.fill + " ,"            
            if self.fill != "": opt += self.fill + " ,"   
            if self.position != "": opt += self.position + " ,"   
            if self.align != "": opt += "align=" + self.align + " ,"            
            if self.rotate_text != 0.:  opt += "rotate=%.3f" %  self.rotate_text+ " ,"               
            if len(opt) > 0: opt = "[" + opt[:-2] + "] "
            
            ptos = ""
            if len(self.addpto) >= 1:
                for ii in range(0,1):
                    pto = self.addpto[ii]
                    ptos += r"(%.4f%s,%.4f%s,%.4f%s) " % (pto.x, units, pto.y, units, pto.z, units)
                #if len(ptos) > 0: ptos = ptos[:]
            else:
                log("Less than one point for the node %s" % self.id)            
            
            str = r"\node %s at %s {%s};" % (opt, ptos,self.text)             
                
        if self.action == "parabola":
            
            opt = ""
            if self.arrow != "": opt += self.arrow.replace("##units##",units) + " ,"
            if self.thick != "": opt += self.thick.replace("##units##",units) + " ,"
            if self.type != "": opt += self.type.replace("##units##",units) + " ,"
            if self.color != "": opt += self._color_build() + " ,"
            if self.fill != "": opt += self.fill + " ,"
            if len(opt) > 0: opt = "[" + opt[:-2] + "] "
            
            ptos = ""
            if len(self.addpto) == 3:
                
                pto = self.addpto[0]
                ptos += "(%.4f%s,%.4f%s,%.4f%s) parabola " % (pto.x, units, pto.y, units, pto.z, units)
                
                pto = self.addpto[1]
                ptos += " bend (%.4f%s,%.4f%s,%.4f%s) " % (pto.x, units, pto.y, units, pto.z, units)
                
                pto = self.addpto[2]
                ptos += "(%.4f%s,%.4f%s,%.4f%s)" % (pto.x, units, pto.y, units, pto.z, units)                              
                
            else:
                log("Only three points allowed in the parabla %s" % self.id)
            
            str = r"\draw%s %s;" % (opt,ptos)       
        
            
        return str
    
    #############################################
    """
    id
    addpto
    
    arrow
    arrow_build(self, start, end, scale)
    
    thick
    type
    color
    fill

    radius
    start_angle
    end_angle
    step

    text
    rotate_text
    position
    align

    action
    layer
    zorder
    labels
    addlabel
    comment    
    """
    @property
    def id(self):
        return self._key      
    
    @property
    def addpto(self):
        return self.parent.shapes[self._key]["ptos"]
    
    @addpto.setter
    def addpto(self, value):
        ### Can be set as a point, a list o points, an alias, a list of alias or 
        ### a list of alias and points objects. Also id of points can be used.
        
        ### Add points
        if type(value) is type([]):       
            for v in value:
                _pto = self.parent.parent.pto._choices(v)
                self.parent.shapes[self._key]["ptos"].append(_pto)
        else:
            _pto = self.parent.parent.pto._choices(value)
            self.parent.shapes[self._key]["ptos"].append(_pto)
    
    @property
    def arrow(self):
        # \usetikzlibrary{arrows}
        # -> <-> <- |-| <-| |-> <<->> o-stealth [-] (-)
        # arrow head = 4mm
        # page 311 pgfmanualCVS2012-11-04        
        return self.parent.shapes[self._key]["arrow"]
    
    @arrow.setter
    def arrow(self, value):
        val = str(value).lower().strip()
        self.parent.shapes[self._key]["arrow"] = val
    
    def arrow_build(self, start, end, scale):
        
        txt,s,e = "","",""
        if start != "" and not start is None: s = r"{%s[scale=%.4f##units##]}" % (start, scale)
        
        if end != "" and not end is None: e =  r"{%s[scale=%.4f##units##]}" % (end, scale)    
        
        if s != "" or e != "": txt = s + r"-" + e
        
        self.parent.shapes[self._key]["arrow"] = txt
        
    def line_thick_options(self):
        lst = ["ultra thin" , "very thin" , "thin" , "semithick" , "thick" , "very thick", "ultra thick", "help lines"]
        return lst
    
    @property
    def thick(self):
        # \usetikzlibrary{arrows}
        # ultra thin , very thin , thin , semithick , thick , very thick and ultra thick
        # line width=0.2cm
        # page 311 pgfmanualCVS2012-11-04
        return self.parent.shapes[self._key]["thick"]
    
    @thick.setter
    def thick(self, value):
        lst = self.line_thick_options()
        val = str(value).lower().strip()
        if val in lst:
            self.parent.shapes[self._key]["thick"] = val
        elif val == "":
            pass
        else:
            self.parent.shapes[self._key]["thick"] = "line width = %.4f##units##" % float(val)

    def line_type_options(self):
        lst = ["solid", "dashed" , "dotted" , "dashdotted" , "dashdotdotted"]
        lst = lst + ["densely dashed" , "densely dotted" , "densely dashdotted" , "densely dashdotdotted"]
        lst = lst + ["loosely dashed" , "loosely dotted" , "loosely dashdotted" , "loosely dashdotdotted"]
        lst2 = ["zigzag", "random", "saw", "snake"]
        return lst, lst2    
            
    @property
    def type(self):
        # \usetikzlibrary{decorations, decorations.pathmorphing}
        # page 159 pgfmanualCVS2012-11-04
        # page 377 pgfmanualCVS2012-11-04
        return self.parent.shapes[self._key]["type"]
    
    @type.setter
    def type(self, value):
        lst,lst2 = self.line_type_options()
        val = str(value).lower().strip()
        if val in lst:        
            self.parent.shapes[self._key]["type"] = val
        elif val in lst2:
            if val == "zigzag": val2 = "decorate, decoration={straight zigzag}"
            if val == "random": val2 = "decorate, decoration={random steps}"
            if val == "saw": val2 = "decorate, decoration={saw}"
            if val == "snake": val2 = "decorate, decoration={snake}"
            
            self.parent.shapes[self._key]["type"] = val2
        elif (val.split("_")[0] in lst2) and len(val.split("_")) == 2:            
            if val.split("_")[0] == "zigzag": val2 = "decorate, decoration={straight zigzag, segment length=%s##units##}" % val.split("_")[1]           
            if val.split("_")[0] == "random": val2 = "decorate, decoration={random steps, segment length=%s##units##}" % val.split("_")[1]           
            if val.split("_")[0] == "saw": val2 = "decorate, decoration={saw, segment length=%s##units##}" % val.split("_")[1]           
            if val.split("_")[0] == "snake": val2 = "decorate, decoration={snake, segment length=%s##units##}" % val.split("_")[1]      
            
            self.parent.shapes[self._key]["type"] = val2
        elif (val.split("_")[0] in lst2) and len(val.split("_")) == 3:            
            if val.split("_")[0] == "zigzag": val2 = "decorate, decoration={straight zigzag, segment length=%s##units##, amplitude=%s##units##}" % (val.split("_")[1], val.split("_")[2])
            if val.split("_")[0] == "random": val2 = "decorate, decoration={random steps, segment length=%s##units##, amplitude=%s##units##}" % (val.split("_")[1], val.split("_")[2])
            if val.split("_")[0] == "saw": val2 = "decorate, decoration={saw, segment length=%s##units##, amplitude=%s##units##}" % (val.split("_")[1], val.split("_")[2])
            if val.split("_")[0] == "snake": val2 = "decorate, decoration={snake, segment length=%s##units##, amplitude=%s##units##}" % (val.split("_")[1], val.split("_")[2])
            
            self.parent.shapes[self._key]["type"] = val2
        else:
            self.parent.shapes[self._key]["type"] = val      
        
    def line_color_options(self):
        lst = ["red" , "green" , "blue" , "cyan", "magenta" , "yellow" , "black" , "gray" , "darkgray" , "lightgray" , "brown" , "lime" , "olive" , "orange" , "pink" , "purple" , "teal" , "violet", "white"]
        return lst
        
    @property
    def color(self):
        # name, black!30, green!20!white, 255_255_255, 255_255_255_0, custom defined in colors
        return self.parent.shapes[self._key]["color"]
    
    def _color_build(self):
        return self.parent.parent.col[self.color]
        
    @color.setter
    def color(self, value):
        self.parent.parent.col[value] = value
        self.parent.shapes[self._key]["color"] = value 

    @property
    def fill(self):
        # name, black!30, green!20!white
        # 
        return self.parent.shapes[self._key]["fill"]
    
    @fill.setter
    def fill(self, value):
        lst = self.line_color_options()
        val = str(value).lower().strip()     
        
        if val in lst:        
            self.parent.shapes[self._key]["fill"] = "fill=" + val  
        else:
            self.parent.shapes[self._key]["fill"] = val              
    
    @property
    def action(self):
        return self.parent.shapes[self._key]["action"]
        
    @action.setter
    def action(self, value):
        self.parent.shapes[self._key]["action"] = value
    
    @property
    def layer(self):
        return self.parent.shapes[self._key]["layer"]
        
    @layer.setter
    def layer(self, value):
        self.parent.shapes[self._key]["layer"] = float(value)
        
    @property
    def zorder(self):
        return self.parent.shapes[self._key]["z-order"]
        
    @zorder.setter
    def zorder(self, value):
        self.parent.shapes[self._key]["z-order"] = float(value)  

    @property
    def _labels(self):
        return self.parent.shapes[self._key]["labels"]
        
    @property
    def labels(self):
        return copy.deepcopy(self.parent.shapes[self._key]["labels"])
       
    @property
    def addlabel(self):
        return self.labels
        
    @addlabel.setter
    def addlabel(self, value):
        if type(value) is type([]):
            for val in value:
                self.addlabel = val
        else:    
            if value in self.parent.labels:
                if not value in self.parent.shapes[self._key]["labels"]:
                    self.parent.shapes[self._key]["labels"].append(value)
                return True
            else:
                self.parent.addlabel = value
                if not value in self.parent.shapes[self._key]["labels"]:
                    self.parent.shapes[self._key]["labels"].append(value)
                return True
            
    def dellabel(self, value):
        if value in self.parent.labels:
            if value in self.parent.shapes[self._key]["labels"]:
                newlst = [x for x in self.labels if x != value]
                self.parent.shapes[self._key]["labels"] = newlst
                return True
            else:
                #log("The label %s has not been added before" % value)            
                return False
        else:
            #log("The label %s has not been previously declared" % value)            
            return False
            
    @property
    def comment(self):
        return self.parent.shapes[self._key]["comment"]
        
    @comment.setter
    def comment(self, value):
        self.parent.shapes[self._key]["comment"] = str(value)  

    @property
    def radius(self):
        return float(self.parent.shapes[self._key]["radius"])
        
    @radius.setter
    def radius(self, value):
        self.parent.shapes[self._key]["radius"] = float(value)   
        
    @property
    def start_angle(self):
        return float(self.parent.shapes[self._key]["start_angle"])
        
    @start_angle.setter
    def start_angle(self, value):
        self.parent.shapes[self._key]["start_angle"] = float(value)  

    @property
    def end_angle(self):
        return float(self.parent.shapes[self._key]["end_angle"])
        
    @end_angle.setter
    def end_angle(self, value):
        self.parent.shapes[self._key]["end_angle"] = float(value)        

    @property
    def step(self):
        return self.parent.shapes[self._key]["step"]
        
    @step.setter
    def step(self, value):
        if isinstance(value,[]):
            self.parent.shapes[self._key]["step"] = value
        else:
            log("Step is not a list")
    @property
    def text(self):
        return self.parent.shapes[self._key]["text"]
        
    @text.setter
    def text(self, value):
        self.parent.shapes[self._key]["text"] = str(value)
        
    @property
    def rotate_text(self):
        return self.parent.shapes[self._key]["rotate_text"]
        
    @rotate_text.setter
    def rotate_text(self, value):
        ### float number in degrees
        self.parent.shapes[self._key]["rotate_text"] = float(value)        

    def positions_options(self):
        lst = ["above" , "below" , "left" , "right", "above left" , "below left" , "above right" , "below right"]
        return lst
        
    @property
    def position(self):
        return self.parent.shapes[self._key]["position"]
        
    @position.setter
    def position(self, value):
        lst =  self.positions_options()
        if value in lst:
            self.parent.shapes[self._key]["position"] = value               
        if isinstance(value, numbers.Real):
            if int(value) >= 0 and int(value) < len(lst):
                self.parent.shapes[self._key]["position"] = lst[int(value)]
                
    def align_options(self):
        lst = ["left" , "center" , "right"]
        return lst
        
    @property
    def align(self):
        return self.parent.shapes[self._key]["align"]
        
    @align.setter
    def align(self, value):
        lst =  self.align_options()
        if value in lst:
            self.parent.shapes[self._key]["align"] = value               
        if isinstance(value, numbers.Real):
            if int(value) >= 0 and int(value) < len(lst):
                self.parent.shapes[self._key]["align"] = lst[int(value)]                
        
    def __repr__(self):
        return self.__class__
        
    def __str__(self):
        
        return "Line key:%s layer=%i points=%i NumLines:%i" % (self.id, self.layer, len(self.addpto), len(self.parent.shapes))                
        
        