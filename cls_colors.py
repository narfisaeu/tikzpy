#!/usr/bin/python 
# FLC 2013

class _clscolors(object):
   
    def __init__(self, parent):
        
        self.parent = parent
        self._colors = {}
        self._default = ["red" , "green" , "blue" , "cyan", "magenta" , "yellow" , "black" , "gray" , "darkgray" , "lightgray" , "brown" , "lime" , "olive" , "orange" , "pink" , "purple" , "teal" , "violet", "white"]
        
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
           
        return None
        
    def __getitem__(self, name):
        ### Get a given color
        fval = self._return_color_format(name)
        if val is None:
            self.parent.error("Color (%s) assing wrong format of value (%s)" % (name, value))
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
        
    def __setitem__(self, name, value):
        ### Set a given color
        val = self._check_color_format(value)
        if val is None:
            self.parent.error("Color (%s) assing wrong format of value (%s)" % (name, value))
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
                txt = "%s_%s_%s" % (int(lst[0]),int(lst[1]),int(lst[2]))
                return self._color_format(txt, type_col = 3, trans = 0)
            elif len(lst) == 4:
                ### 255_255_255_10, rgb with transparency
                txt = "%s_%s_%s" % (int(lst[0]),int(lst[1]),int(lst[2]))
                return self._color_format(txt, type_col = 4, trans = int(lst[3]))                    
            else:
                return None
                    
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
        if key in self._colors.keys:
            return True
        else:
            return False
    

        