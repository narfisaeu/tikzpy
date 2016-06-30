#!/usr/bin/python 
# FLC 2013

import os
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
            * Circle given by center and radius. See :ref:`shp.circle <shapes_circle>`
            * Arc given by starting point, radius and angles. See :ref:`shp.arc <shapes_arc>`
            * Text label. See :ref:`shp.text <shapes_text>`
        * Shapes allow to set labels (see labels section). See :ref:`labels <labels_cls>`
    
    **Chracteristics of a shape (shp) object**
    
        * Each shape object has different properties depending on the nature of the shape
    
    """
    
    """
        For the furture:
            
            * Add scale group of shapes shps
            * .add_arc(angle_in, angle_out, radius ) -- arc (90:-90:.5) in a line
            * add_cycle in a line
            * Shade options
            * Check arrows and example
            * Add opacity/opacity, section 21
            
            * Add mapbits, images -- July 2016 (unclear the scale and units)
            * Add decorations (review in type) -- April 2016
            * Check fill examples -- April 2016
            * Add patterns into fill -- April 2016
            * Add translate of shps -- April 2016
            * Add rotation of shps -- April 2016
            * Add copy of shps -- April 2016            
            * Review labels -- May 2016
            * Grid rectangle -- May 2016 (should be done as an assembly of lines, to be rotable)
            * Rectangle given by two corners --  (should be done as an assembly of lines, to be rotable)
            * Parabola given by three points -- Discarded                   
    """
    
    def __init__(self, parent):
        
        self.parent = parent
        
        ### Counters
        self.counters = obj_data._clsdata(type = int(0))
        
        ### Dictionary of lines
        self.shapes = obj_data._clsdata(type = {})
        self.counters["shapes"] = 0    
        
    def log(self, txt, ref = ""):
        self.parent.log(txt, ref = ref)
        
    def error(self, txt, ref = ""):
        self.parent.error(txt, ref = ref)        
        
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
            * fill = "": fill texture of the line (see :ref:`fill examples <ex_shapes_fill>`)
            
        **Returns:**
            * A line shape object
           
        **Chracteristics of a shape line object**
        
        :ivar id: get unique id of the shape object
        :ivar action: get type of shape object
        :ivar zorder: set/get z position respect the drawing plane and viewer
        :ivar labels: get labels list that the shape is associated to
        :ivar addlabel: set/get add a label or list of labels to the shape
        :ivar dellabel: set/get delete a shape label
        :ivar comment: multifunctional text field
        
        :ivar arrow: set/get arrow parameters (see arrows examples)
        :ivar arrow_build(start,end,scale): arrow parameter (see arrows examples)
        :ivar thick: set/get line thickness (see :ref:`thick examples <ex_shapes_thick>`)
        :ivar type: set/get type of line (see :ref:`type examples <ex_shapes_type>`)
        :ivar color: set/get color of the line (see :ref:`colors examples <ex_shapes_color>`)
        :ivar fill: set/get fill texture of the line (see :ref:`fill examples <ex_shapes_fill>`)
        
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
            * thick = "": path thickness (see :ref:`thick examples <ex_shapes_thick>`)
            * type = "": type of path (see :ref:`type examples <ex_shapes_type>`)
            * color = "": color of the path (see :ref:`colors examples <ex_shapes_color>`)
            * fill = "": fill texture of the path (see :ref:`fill examples <ex_shapes_fill>`)
            
        **Returns:**
            * A path shape object
           
        **Chracteristics of a shape line object**
        
        :ivar id: get unique id of the shape object
        :ivar action: get type of shape object
        :ivar zorder: set/get z position respect the drawing plane and viewer
        :ivar labels: get labels list that the shape is associated to
        :ivar addlabel: set/get add a label or list of labels to the shape
        :ivar dellabel: set/get delete a shape label
        :ivar comment: multifunctional text field
        
        :ivar arrow: set/get arrow parameters (see arrows examples)
        :ivar arrow_build(start,end,scale): arrow parameter (see arrows examples)
        :ivar thick: set/get line thickness (see :ref:`thick examples <ex_shapes_thick>`)
        :ivar type: set/get type of line (see :ref:`type examples <ex_shapes_type>`)
        :ivar color: set/get color of the line (see :ref:`colors examples <ex_shapes_color>`)
        :ivar fill: set/get fill texture of the line (see :ref:`fill examples <ex_shapes_fill>`)
        
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
            * fill = "": fill texture of the line (see :ref:`fill examples <ex_shapes_fill>`)
            
        **Returns:**
            * A circle shape object
           
        **Chracteristics of a shape circle object**
        
        :ivar id: get unique id of the shape object
        :ivar action: get type of shape object
        :ivar zorder: set/get z position respect the drawing plane and viewer
        :ivar labels: get labels list that the shape is associated to
        :ivar addlabel: set/get add a label or list of labels to the shape
        :ivar dellabel: set/get delete a shape label
        :ivar comment: multifunctional text field
        
        :ivar arrow: set/get arrow parameters (see arrows examples)
        :ivar arrow_build(start,end,scale): arrow parameter (see arrows examples)
        :ivar thick: set/get line thickness (see :ref:`thick examples <ex_shapes_thick>`)
        :ivar type: set/get type of line (see :ref:`type examples <ex_shapes_type>`)
        :ivar color: set/get color of the line (see :ref:`colors examples <ex_shapes_color>`)
        :ivar fill: set/get fill texture of the line (see :ref:`fill examples <ex_shapes_fill>`)
                
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
            * fill = "": fill texture of the line (see :ref:`fill examples <ex_shapes_fill>`)
            
        **Returns:**
            * An arc shape object
           
        **Chracteristics of a shape arc object**
        
        :ivar id: get unique id of the shape object
        :ivar action: get type of shape object
        :ivar zorder: set/get z position respect the drawing plane and viewer
        :ivar labels: get labels list that the shape is associated to
        :ivar addlabel: set/get add a label or list of labels to the shape
        :ivar dellabel: set/get delete a shape label
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
        if thick != "": item.thick = thick
        if type != "":  item.type = type
        if color != "": item.color = color
        if fill != "": item.fill = fill      
        
        return item        
    
    def text(self, pto, text, layer = 0, color = "", fill = "", rotate_text = 0, position = "", align = ""):
        """
        .. _shapes_text:         
                
        **Synopsis:**
            * Add a text. Referenced by a point position.
        
        **Args:**
            * pto: point reference for the text node
            * text: text to be added
            
        **Optional parameters:**
            * layer = 0: layer member where the shape belongs
            * color = "": color of the line (see :ref:`colors examples <ex_shapes_color>`)
            * fill = "": fill texture of the line (see :ref:`fill examples <ex_shapes_fill>`)
            * rotate_text = 0.: float number in degrees of text rotation
            * position = "": "above" , "below" , "left" , "right", "above left" , "below left" , "above right" , "below right"
            * align = "": "left" , "center" , "right"
            
        **Returns:**
            * An text shape object
           
        **Chracteristics of a shape text object**
        
        :ivar id: get unique id of the shape object
        :ivar action: get type of shape object
        :ivar zorder: set/get z position respect the drawing plane and viewer
        :ivar labels: get labels list that the shape is associated to
        :ivar addlabel: set/get add a label or list of labels to the shape
        :ivar dellabel: set/get delete a shape label
        :ivar comment: multifunctional text field
        
        :ivar color: set/get color of the text (see :ref:`colors examples <ex_shapes_color>`)
        :ivar fill: set/get fill texture of the text (see :ref:`fill examples <ex_shapes_fill>`)
        
        :ivar text: set/get text label
        :ivar rotate_text: float number in degrees of text rotation
        :ivar position: options: "above" , "below" , "left" , "right", "above left" , "below left" , "above right" , "below right"
        :ivar align: options: "left" , "center" , "right"    
        
        .. note::
        
            * See :ref:`text examples <ex_shapes_text>`
            
        """      
        
        item = self._additem("text", layer = layer)          
        item.text = text
        item.addpto = pto
        if color != "": item.color = color
        if fill != "": item.fill = fill          
        if rotate_text != 0.: item.rotate_text = rotate_text         
        if position != "": item.position = position       
        if align != "": item.align = align       
               
        return item   

    def bitmap(self, pto, bitmap_path, width = None, height = None, layer = 0, color = "", fill = "", rotate_text = 0, position = "", align = ""):
        """
        .. _shapes_bitmap:         
                
        **Synopsis:**
            * Add a bitmap or image file. Referenced by a point position using a node wrapper.
        
        **Args:**
            * pto: point reference for the bitmap node
            * bitmap_path: path to bitmap or image file (jpg, png, pdf)
            
        **Optional parameters:**
            * width = None: image width, if just width or height is supply the aspect ratio is mantain (in cm)
            * height = None: image height, if just width or height is supply the aspect ratio is mantain (in cm)
            * layer = 0: layer member where the shape belongs
            * color = "": color of the line (see :ref:`colors examples <ex_shapes_color>`)
            * fill = "": fill texture of the line (see :ref:`fill examples <ex_shapes_fill>`)
            * rotate_text = 0.: float number in degrees of image rotation
            * position = "": "above" , "below" , "left" , "right", "above left" , "below left" , "above right" , "below right"
            * align = "": "left" , "center" , "right"
            
        **Returns:**
            * An bitmap shape object
           
        **Chracteristics of a shape bitmap object**
        
        :ivar id: get unique id of the shape object
        :ivar action: get type of shape object
        :ivar zorder: set/get z position respect the drawing plane and viewer
        :ivar labels: get labels list that the shape is associated to
        :ivar addlabel: set/get add a label or list of labels to the shape
        :ivar dellabel: set/get delete a shape label
        :ivar comment: multifunctional bitmap field
        
        :ivar color: set/get color of the bitmap (see :ref:`colors examples <ex_shapes_color>`)
        :ivar fill: set/get fill texture of the bitmap (see :ref:`fill examples <ex_shapes_fill>`)
        
        :ivar text: set/get bitmap path (windows backslash is replace by slash)
        :ivar rotate_text: float number in degrees of bitmap rotation
        :ivar position: options: "above" , "below" , "left" , "right", "above left" , "below left" , "above right" , "below right"
        :ivar align: options: "left" , "center" , "right"    
        
        .. note::
        
            * See :ref:`bitmap examples <ex_shapes_bitmap>`
            
        """      
        
        item = self._additem("bitmap", layer = layer)          
        item.text = self._build_bitmap_text(bitmap_path, width, height)
        item.addpto = pto
        if color != "": item.color = color
        if fill != "": item.fill = fill          
        if rotate_text != 0.: item.rotate_text = rotate_text         
        if position != "": item.position = position       
        if align != "": item.align = align       
               
        return item          
    
    def _build_bitmap_text(self, bitmap_path, width, height):
        ### Build a bitmap text
        opt = ""
        if width is not None: opt = "width=%.4fcm," % width
        if height is not None: opt = "height=%.4fcm" % height
        if not os.path.isfile(bitmap_path):
            self.error("Bitmap file does not exist", ref = "_build_bitmap_text")
        txt = r"\includegraphics[%s]{%s}" % (opt, bitmap_path.replace("\\", r"/"))
        return txt
    
    def grid(self, corner1_pto, corner2_pto, xstep = 1, ystep = 1, layer = 0, thick = "help lines", type = "", color = ""):
        """
        .. _shapes_grid:         
                
        **Synopsis:**
            * Add a renctangular grid defined by the two opposite corner points
        
        **Args:**
            * corner1_pto: point of corner 1
            * corner2_pto: point of corner 2
            
        **Optional parameters:**
            * xstep = 1: grid step in x direction
            * ystep = 1: grid step in y direction        
            * layer = 0: layer member where the shape belongs
            * thick = "help lines": line thickness (see :ref:`thick examples <ex_shapes_thick>`)
            * type = "": type of line (see :ref:`type examples <ex_shapes_type>`)
            * color = "": color of the line (see :ref:`colors examples <ex_shapes_color>`)
            
        **Returns:**
            * A grid shape object
           
        **Chracteristics of a shape line object**
        
        :ivar id: get unique id of the shape object
        :ivar action: get type of shape object
        :ivar zorder: set/get z position respect the drawing plane and viewer
        :ivar labels: get labels list that the shape is associated to
        :ivar addlabel: set/get add a label or list of labels to the shape
        :ivar dellabel: set/get delete a shape label
        :ivar comment: multifunctional text field
        
        :ivar thick: set/get line thickness (see :ref:`thick examples <ex_shapes_thick>`)
        :ivar type: set/get type of line (see :ref:`type examples <ex_shapes_type>`)
        :ivar color: set/get color of the line (see :ref:`colors examples <ex_shapes_color>`)   
                
        .. note::
            
            * The grid cannot be rotated
            * See :ref:`grid examples <ex_shapes_grid>`
        
        """     
        
        item = self._additem("grid", layer = layer)          
        item.step = [1, xstep, ystep]
        item.addpto = corner1_pto
        item.addpto = corner2_pto     
        if thick != "": item.thick = thick
        if type != "":  item.type = type
        if color != "": item.color = color      
        
        return item 
    
    def parabola(self, pto1, ptobend, pto2, layer = 0):
        
        item = self._additem("parabola", layer = layer)          
        item.addpto = pto1
        item.addpto = ptobend
        item.addpto = pto2
        
        return item       
        
    ######################### Translation, copy, rotate  
    def copy(self, shps):
        
        """
        .. _shapes_copy_list:         
                
        **Synopsis:**
            * For a list of shapes (give by id or object), it return a list of ids copied shapes
        
        **Args:**
            * shps: list of shapes or single shape. Given by id or shape object.
            
        **Optional parameters:**
            * None
            
        **Returns:**
            * List of unique ids of the copied shapes
                
        .. note::
        
            * See example :ref:`copy shapes <ex_groups_ex2>`.
        
        """        
        
        lst_out = []
            
        if type(shps) is type([]):
            
            for shp in shps:
                id = self._check_shp(shp)
                _shp = self.getitem(id).copy()
                lst_out.append( _shp.id )            
        
        else:
            id = self._check_shp(shps)
            _shp = self.getitem(id).copy()
            lst_out.append( _shp.id )          
        
        return lst_out
        
    def translate(self, shps, x = 0., y = 0., z = 0.):
        
        """
        
        .. _shapes_translate:      
                
        **Synopsis:**
            * Translate a shapes of list in a 3D space
        
        **Args:**
             * shps: list of shapes or single shape. Given by id or shape object.
            
        **Optional parameters:**
            * x = 0: increment in x coordinate to tranlate
            * y = 0: increment in y coordinate to tranlate
            * z = 0: increment in z coordinate to tranlate
            
        **Returns:**
            * None
            
        .. note::
            
            * See example :ref:`translate shapes <ex_groups_ex2>`.
        
        """  

        ### Create auxiliary group
        grp = self.parent.grp._auxgroup()
        grp.add = shps
        
        ### Translate
        self.parent.pto.translate(grp.ptos_of_shapes, x = x, y = y, z = z)
        
    def translate_to(self, shps, pto_ref, pto_ref_final):
    
        """
        
        .. _shapes_translate_to:         
                
        **Synopsis:**
            * Given a reference point and a final position for such point. Translate a shape or list of shapes in a 3D space in a similar manner.
        
        **Args:**
            * shps: list of shapes or single shape. Given by id or shape object.
            
        **Optional parameters:**
            * pto_ref: reference point
            * pto_ref_final: final refence point position
            
        **Returns:**
            * None
            
        .. note::
            
            * See example :ref:`translate shapes <ex_groups_ex2>`.
        
        """    
        
        ### Create auxiliary group
        grp = self.parent.grp._auxgroup()
        grp.add = shps
        
        ### Translate       
        self.parent.pto.translate_to(grp.ptos_of_shapes, pto_ref, pto_ref_final)  

    def rotate(self, shps, pto_rotation, Ax = 0., Ay = 0., Az = 0.):
    
        """
        
        .. _shapes_rotate:         
                
        **Synopsis:**
            * Rotate a shape of list of shapes in a 3D space respect an origin point
        
        **Args:**
            * shps: list of shapes or single shape. Given by id or shape object.
            * pto_rotation: center point of rotation
            
        **Optional parameters:**
            * Ax = 0.: yaw angle in degrees to turn respect axis X
            * Ay = 0.: pitch angle in degrees to turn respect axis Y
            * Az = 0.: roll angle in degrees to turn respect axis Z
            
        **Returns:**
            * None
            
        .. note::
        
            * See example :ref:`rotation shapes <ex_groups_ex3>`.
        
        """    

        ### Create auxiliary group
        grp = self.parent.grp._auxgroup()
        grp.add = shps
        
        ### Translate       
        self.parent.pto.rotate(grp.ptos_of_shapes, pto_rotation, Ax = Ax, Ay = Ay, Az = Az)
        
    
    ######################### 
    def _check_shp(self, val):
        ### Check type of shape entry
        
        if type(val) is self._type_of_shape():
            id = val.id
        else:
            id = self.getitem(val).id
            if id is None: self.error("Error key.", ref = "shapes_copy_list")
        return id    
    
    def _additem(self, type, layer = 0):
        
        # Create auto new
        _key =  "#s%i" % self.counters["shapes"]
        self.counters["shapes"] = self.counters["shapes"] + 1
        self.shapes[_key] = {}
        
        lline = _shape(self,_key)
        lline.layer = layer
        lline.action = type
        lline.addlabel = "default"
        return lline
    
    def _type_of_shape(self):
        ### Returns the type of shape
        return type(_shape(self,None))      
    
    ######################### Mod properties in block
    def zorder_to_shapes(self, shps, value):
        """
        
        .. _shapes_zorder_to_shapes:   
                
        **Synopsis:**
            * Modify zorder value for a shape or list of shapes
        
        **Args:**
            * shps: list of shapes or single shape. Given by id or shape object.
            * value: zorder value            
            
        **Returns:**
            * None
            
        .. note::
            
            * zorder: z position respect the drawing plane and viewer
        
        """        
        self._mod_properties(shps, value, "zorder")
        
    def thick_to_shapes(self, shps, value):
        """
        
        .. _shapes_thick_to_shapes:   
                
        **Synopsis:**
            * Modify thick value for a shape or list of shapes
        
        **Args:**
            * shps: list of shapes or single shape. Given by id or shape object.
            * value: thick value            
            
        **Returns:**
            * None
            
        .. note::
            
            * thick: shape thickness (see :ref:`thick examples <ex_shapes_thick>`)
        
        """        
        self._mod_properties(shps, value, "thick")   

    def type_to_shapes(self, shps, value):
        """
        
        .. _shapes_type_to_shapes:   
                
        **Synopsis:**
            * Modify type value for a shape or list of shapes
        
        **Args:**
            * shps: list of shapes or single shape. Given by id or shape object.
            * value: type value            
            
        **Returns:**
            * None
            
        .. note::
            
            * type: type of shape (see :ref:`type examples <ex_shapes_type>`)
        
        """        
        self._mod_properties(shps, value, "thick")        
        
    def color_to_shapes(self, shps, value):
        """
        
        .. _shapes_color_to_shapes:   
                
        **Synopsis:**
            * Modify color value for a shape or list of shapes
        
        **Args:**
            * shps: list of shapes or single shape. Given by id or shape object.
            * value: color value            
            
        **Returns:**
            * None
            
        .. note::
            
            * color: color of the shape (see :ref:`colors examples <ex_shapes_color>`)
        
        """        
        self._mod_properties(shps, value, "color")    

    def fill_to_shapes(self, shps, value):
        """
        
        .. _shapes_fill_to_shapes:   
                
        **Synopsis:**
            * Modify fill value for a shape or list of shapes
        
        **Args:**
            * shps: list of shapes or single shape. Given by id or shape object.
            * value: fill value            
            
        **Returns:**
            * None
            
        .. note::
            
            * fill: fill texture of the shape (see fill examples)
        
        """        
        self._mod_properties(shps, value, "fill")         
    
    def _mod_properties(self, shps, value, txt_property):
        ### Modifies properties by name
        
        def _mode_prop(_shp, txt_property, val, islist):
            if txt_property == "addlabel":
                _shp.addlabel = val            
            elif txt_property == "dellabel":
                _shp.dellabel = val
            elif txt_property == "zorder":
                if islist: self.error("Not accept lists of zorder")
                _shp.zorder = val
            elif txt_property == "thick":
                if islist: self.error("Not accept lists of thick")
                _shp.thick = val  
            elif txt_property == "type":
                if islist: self.error("Not accept lists of type")
                _shp.type = val   
            elif txt_property == "color":
                if islist: self.error("Not accept lists of color")
                _shp.color = val        
            elif txt_property == "fill":
                if islist: self.error("Not accept lists of fill")
                _shp.fill = val                
            else:
                self.error("Wrong labeling ")
            
        ### Create auxiliary group
        grp = self.parent.grp._auxgroup()
        grp.add = shps
        
        ### Iterate
        for _shp in grp.shps:
            if type(value) == type([]):
                for _value in value:
                    _mode_prop(_shp, txt_property, _value, True)                   
            else:
                _mode_prop(_shp, txt_property, value, False)                           
        
     ######################### Labels
    def _shapes_by_label(self, value):
        ### Return list of shapes by label or list of labels
        lst = []
        
        if type(value) == type([]):
            for _value in value:
                for key in self.keys():
                    shp = self.getitem(key)             
                    if _value in self.shapes[key]["labels"]:
                        if shp.id not in lst:
                            lst.append(shp.id)            
            
        else:
            for key in self.keys():
                shp = self.getitem(key)             
                if value in self.shapes[key]["labels"]:
                    if shp.id not in lst:
                        lst.append(shp.id)
        
        return lst
        
    def _dellabel(self, value):
        ### Delete a label from all the shapes
        
        if value in self.parent.lbl.labels:
            
            ### Delete from all the shapes
            for key in self.keys():
                shp = self.getitem(key)             
                shp.dellabel = value
            
            ### Remake list
            self.parent.lbl._dellabel(value)
            
            return True
        else:
            #log("The label %s has not been previously declared" % value)   
            return False

    def _rename_label(self, name_old, name_new):
        ### Rename a label from all the shapes
        
        if name_old != name_new:            
                        
            ### Add new name
            self.parent.lbl.addlabel = name_new
            
            ### Delete from all the shapes
            for key in self.keys():
                shp = self.getitem(key)             
                if name_old in self.shapes[key]["labels"]:
                    shp.dellabel = name_old
                    shp.addlabel = name_new
            
            ### Remake list
            self.parent.lbl._dellabel(name_old)
            
            return True
        else:
            #log("Inconsistent")            
            return False  

    ######################### Builder
    def _types_patterns(self):
        
        v = ["horizontal lines", "vertical lines", "north east lines", "north west lines", "grid", \
            "crosshatch", "dots", "crosshatch dots", "fivepointed stars", "sixpointed stars", "bricks", "checkerboard"]
        
        return v
    def pattern_build(self, type_pattern, color = ""):
        """
        
        .. _shapes_pattern_build:   
                
        **Synopsis:**
            * Builds a type of pattern fill object that can be set to the fill property
        
        **Args:**
            * type_pattern: type of pattern
        
        **Optional parameters:**
            * color="": color of pattern (see :ref:`colors examples <ex_shapes_color>`)
                        
        **Returns:**
            * A pattern object that can be set to the fill property
            
        .. note::
            
            * Possible types: horizontal lines, vertical lines, north east lines, north west lines, grid, crosshatch, dots, crosshatch dots, fivepointed stars, sixpointed stars, bricks, checkerboard
            * See :ref:`fill examples <ex_shapes_fill>`
        
        """        
        _type_pattern = str(type_pattern).lower().strip()
        if _type_pattern not in self._types_patterns():
            self.error("Type of pattern not found")
        
        _color = str(color).lower().strip()
        self.parent.col[_color] = _color

        lst = ["#pat#", _type_pattern, _color]
        
        return lst        
            
class _shape(object):
   
    def __init__(self, parent, key):
        
        self.parent = parent
        self._key = key
        self._draw = False
        
        if key is None: return
        
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
        
        return shp
        
    def build_tik_string(self, units = ""):
        
        str = ""
        
        if self.action == "line" or self.action == "path":
            
            opt = ""
            if self.arrow != "": opt += self.arrow.replace("##units##",units) + " ,"
            if self.thick != "": opt += self.thick.replace("##units##",units) + " ,"
            if self.type != "": opt += self.type.replace("##units##",units) + " ,"
            if self.color != "": opt += self._color_build() + " ,"
            if self.fill != "": opt += self._construct_fill() + " ,"
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
            if self.fill != "": opt += self._construct_fill() + " ,"
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
            if self.fill != "": opt += self._construct_fill() + " ,"
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
            if self.fill != "": opt += self._construct_fill() + " ,"
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
            #if self.fill != "": opt += self._construct_fill() + " ,"
            if self.step[2] != 0: opt += "ystep=%.4f ," % self.step[2]
            if self.step[1] != 0: opt += "xstep=%.4f ," % self.step[1]
            #if self.step[0] != 0: opt += "step=%.4f ," % self.step[0]            
            if len(opt) > 0: opt = "[" + opt[:-2] + "] "
            
            ptos = ""
            if len(self.addpto) >= 2:
                for ii in range(0,2):
                    pto = self.addpto[ii]
                    ptos += "(%.4f%s,%.4f%s,%.4f%s) grid " % (pto.x, units, pto.y, units, pto.z, units)
                if len(ptos) > 0: ptos = ptos[:-6]
            else:
                log("Less than two point for the grid %s" % self.id)            
            
            str = r"\draw %s %s;" % (opt, ptos)   
            print str
        if self.action == "text":

            opt = ""
            #if self.arrow != "": opt += self.arrow.replace("##units##",units) + " ,"
            #if self.thick != "": opt += self.thick.replace("##units##",units) + " ,"
            #if self.type != "": opt += self.type.replace("##units##",units) + " ,"
            if self.color != "": opt += self._color_build() + " ,"
            if self.fill != "": opt += self._construct_fill() + " ,"   
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
        
        if self.action == "bitmap":

            opt = ""
            #if self.arrow != "": opt += self.arrow.replace("##units##",units) + " ,"
            #if self.thick != "": opt += self.thick.replace("##units##",units) + " ,"
            #if self.type != "": opt += self.type.replace("##units##",units) + " ,"
            if self.color != "": opt += self._color_build() + " ,"
            if self.fill != "": opt += self._construct_fill() + " ,"   
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
            if self.fill != "": opt += self._construct_fill() + " ,"
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
        
    @property
    def color(self):
        # name, black!30, green!20!white, 255_255_255, 255_255_255_0, custom defined in colors
        return self.parent.shapes[self._key]["color"]
    
    def _color_build(self):
        return self.parent.parent.col[self.color]
        
    @color.setter
    def color(self, value):
        val = str(value).lower().strip()
        self.parent.parent.col[val] = val
        self.parent.shapes[self._key]["color"] = val 

    @property
    def fill(self):
        # name, black!30, green!20!white
        # 
        return self.parent.shapes[self._key]["fill"]
    
    @fill.setter
    def fill(self, value):
        if type(value) == type([]):
            if value[0] == "#pat#":
                ### Pattern case
                self.parent.shapes[self._key]["fill"] = value
            elif value[0] == "#sha#":
                ### Shade case
                self.parent.shapes[self._key]["fill"] = value                
            else:
                self.parent.error("Wrong fill type, %s" % value)
        else:
            ### Color type
            val = str(value).lower().strip()
            self.parent.parent.col[val] = val
            self.parent.shapes[self._key]["fill"] = val
    
    def _construct_fill(self):
        
        value = self.parent.shapes[self._key]["fill"]
        _out = ""
        
        if type(value) == type([]):
            if value[0] == "#pat#":
                ### Pattern case
                [nn, _type_pattern, _color] = value
                if _color != "": _out = "pattern color=%s ," % self.parent.parent.col[_color]
                _out += "pattern=%s" % _type_pattern
            elif value[0] == "#sha#":
                ### Shade case
                pass
            else:
                self.parent.error("Wrong fill type, %s" % value)
        else:        
            _out = " fill= " + self.parent.parent.col[value] + " ,"
        
        return _out
    
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
        if type(value) == type([]):
            self.parent.shapes[self._key]["step"] = value
        else:
            log("Step is not a list")
    
    ############### Labels
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
            if value in self.parent.parent.lbl.labels:
                if not value in self.parent.shapes[self._key]["labels"]:
                    self.parent.shapes[self._key]["labels"].append(value)
                return True
            else:
                self.parent.parent.lbl.addlabel = value
                if not value in self.parent.shapes[self._key]["labels"]:
                    self.parent.shapes[self._key]["labels"].append(value)
                return True
    
    @property
    def dellabel(self):
        return self.labels    
    
    @dellabel.setter
    def dellabel(self, value):
        if value in self.parent.parent.lbl.labels:
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
    
    ############### Text
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
        else:
            if isinstance(value, numbers.Real):
                if int(value) >= 0 and int(value) < len(lst):
                    self.parent.shapes[self._key]["position"] = lst[int(value)]
                else:
                    self.parent.error("Wrong position type, %s" % value)
            else:
                self.parent.error("Wrong position type, %s" % value)                 
                
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
        else:
            if isinstance(value, numbers.Real):
                if int(value) >= 0 and int(value) < len(lst):
                    self.parent.shapes[self._key]["align"] = lst[int(value)]                
                else:
                    self.parent.error("Wrong align type, %s" % value)
            else:
                self.parent.error("Wrong align type, %s" % value)      
            
    def __repr__(self):
        return self.id
        
    def __str__(self):
        
        return "Line key:%s layer=%i points=%i NumLines:%i" % (self.id, self.layer, len(self.addpto), len(self.parent.shapes))                
        
        