#!/usr/bin/python 
# FLC 2013

class _colors(object):
   
    """**Colors object:** 
    
    .. _colors_cls:
   
    :platform: Unix, Windows
    :synopsis: Allows to add colors in different formats, with or without tranparency. As well as modifiying the values.
    
    :ivar names: get list of unique ids of the colors containt in the colors object
    :ivar num_colors: get number of unique ids of the colors containt in the colors object

    **Chracteristics of a colors (pyTikZ.col) object**
    
        * The object colors is workable as a python dictionary
        * A color can be set by his name, pyTikZ.col["navy"] = "blue"
        * A color can be get by his name, color_value = pyTikZ.col["navy"]
    
    """   
   
    def __init__(self, parent):
        
        self.parent = parent
        self._colors = {}
        self._default = ["red" , "green" , "blue" , "cyan", "magenta" , "yellow" , "black" , "gray" , "darkgray" , "lightgray" , "brown" , "lime" , "olive" , "orange" , "pink" , "purple" , "teal" , "violet", "white"]
    
    ########################## Properties
    @property
    def num_colors(self):
        return len(self._colors)
        
    @property
    def names(self):
        return self._colors.keys()
    
    ########################## Functions
    
    
    ########################## Functions internal
    def _colors_to_define_lst(self):
        ### Returns the colors that need to be defined previously
        lst = []
        for name, val in self._colors.iteritems():
            cname, type_col, trans, cname2 = self._color_format_back(val)
            if type_col == 3 or type_col == 4:
                lst.append(name)
        return lst
        
    def _colors_to_define_lst_text(self):
        ### Returns the define text that need to be defined previously when TikZ is printed
        lst = self._colors_to_define_lst()
        
        if len(lst)>0:
            lst_out = []
            for name in lst:
                cname, type_col, trans, cname2 = self._color_format_back(self._colors[name])       
                txt = "\definecolor{%s}{RGB}{%s}" % (name, cname)
                lst_out.append(txt)
                
            return lst_out
           
        return []
    
    ########################## Get items
    def _check_names(self,name):
        ###
        lst = name.split("_")
        if len(lst) == 3 or len(lst) == 4:        
            name = "a" + name.replace("_","") + "b"
        return name
        
    def __getitem__(self, vname):
        ### Get a given color
        name = self._check_names(vname)
        fval = self._return_color_format(name)
        if fval is None:
            self.parent.error("Color (%s) assigning wrong format of value (%s)" % (name, fval))
        else:
            return fval
    
    def _return_color_format(self, name):
        ###Returns formated value
        if self._check_key(name):
            val = self._colors[name]
            cname, type_col, trans, cname2 = self._color_format_back(val)
            
            if type_col == 0:
                return cname
            elif type_col == 1:
                return "%s!%i" % (cname, trans)
            elif type_col == 2:
                return "%s!%i!%s" % (cname, trans, cname2)     
            elif type_col == 3:
                return name
            elif type_col == 4:
                return "%s!%i" % (name, trans)                
            else:
                return None
        else:
            return None
    
    ########################## Set items  
    def __setitem__(self, vname, value):
        ### Set a given color
        name = self._check_names(vname)
        
        if self._check_key(name):
            ### Assigned by name, predifined
            pass
        else:      
            if value == "" or value is None:
                pass
            else:
                val = self._check_color_format(value)
                if val is None:
                    self.parent.error("Color (%s) wrong format or not previously defined. In __setitem__" % (name))
                else:
                    self._colors[name] = val
                    
    def _check_color_format(self, txt):
        ### Check possible formats of the value
        if txt in self._default:
            ### Default names
            return self._color_format(txt, type_col = 0, trans = 0)
        else:
            lst = txt.split("!")
            if len(lst) == 2:
                ### red!10
                if not self._check_cname(lst[0]):
                    self.parent.error("Color name (%s) does not exists or not added. In _check_color_format" % lst[0])
                return self._color_format(lst[0], type_col = 1, trans = int(lst[1]),cname2 = "")
            elif len(lst) == 3:
                ### red!10!red
                if not self._check_cname(lst[0]):
                    self.parent.error("Color name (%s) does not exists or not added. In _check_color_format" % lst[0])
                if not self._check_cname(lst[2]):
                    self.parent.error("Color name (%s) does not exists or not added. In _check_color_format" % lst[2])                    
                return self._color_format(lst[0], type_col = 2, trans = int(lst[1]),cname2 = lst[2])
                
            lst = txt.split("_")
            if len(lst) == 3:
                ### 255_255_255, rgb without transparency
                txt = "%s,%s,%s" % (int(lst[0]),int(lst[1]),int(lst[2]))
                return self._color_format(txt, type_col = 3, trans = 0)
            elif len(lst) == 4:
                ### 255_255_255_10, rgb with transparency
                txt = "%s,%s,%s" % (int(lst[0]),int(lst[1]),int(lst[2]))
                return self._color_format(txt, type_col = 4, trans = int(lst[3]))                    
            else:
                return None
    
    ########################## Others           
    def _color_format(self, cname, type_col = False, trans = 0.,cname2 = ""):
        ### List to be save in the dictionary
        return [cname, type_col, trans, cname2]
        
    def _color_format_back(self, val):
        ### List to be save in the dictionary
        [cname, type_col, trans, cname2] = val
        return cname, type_col, trans, cname2
    
    def __delitem__(self, name):
        ### Only delete custom colors
        self._colors.pop(name, None)           
    
    def _check_cname(self, cname):
        if cname in self._default:
            return True
        if _check_key(cname):
            return True
        return False
        
    def _check_key(self, key):
        if key in self._colors:
            return True
        else:
            return False
    

        