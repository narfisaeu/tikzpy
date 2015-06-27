import math
import numbers
import obj_data
import copy

def log(txt):
    
    print txt

class _racimes(object):

    def __init__(self, parent):
    
        self.parent = parent
        
        ### Counters
        self.counters = obj_data._clsdata(type = int(0))
        
        ### Dictionary of lines
        self.racimes = obj_data._clsdata(type = {})
        self.counters["racimes"] = 0    
        
    def __getitem__(self, key):
    
        return self.getitem(key)        
        
    def keys(self):
        
        return self.racimes.keys
        
    def getitem(self, key):        
        
        ### Give a point
        _key = str(key)
        
        if self.racimes[_key]:
            return _racime(self,_key)
        else:
            return None            

    def racime(self, group = 0):
        
        return self._additem("racime", group = group)
        
    def _additem(self, type, group = 0):
        
        # Create auto new
        _key =  "rac#%i" % self.counters["racimes"]
        self.counters["racimes"] = self.counters["racimes"] + 1
        self.racimes[_key] = {}
        
        lline = _racime(self,_key)
        lline.group = group
        lline.action = type
        lline.addlabel = "default"
        lline.group_label = "##group##" + _key
        return lline
    
    #########################
    @property
    def labels(self):
        return self.parent.parent.lbl.labels
    
    @property
    def addlabel(self):
        return self.labels
        
    @addlabel.setter
    def addlabel(self, value):
        self.parent.parent.lbl.addlabel = value        
            
    def dellabel(self, value):
        if value in self.labels:
            
            ### Delete from all the racimes
            for key in self.keys():
                shp = self.getitem(key)             
                shp.dellabel(value)
            
            ### Remake list
            self.parent.parent.lbl._dellabel(value)
            
            return True
        else:
            #log("The label %s has not been previously declared" % value)   
            return False

    def rename_label(self, name_old, name_new):
        if name_old != name_new:            
                        
            ### Add new name
            self.addlabel=name_new
            
            ### Delete from all the racimes
            for key in self.keys():
                shp = self.getitem(key)             
                if name_old in self.racimes[key]["labels"]:
                    shp.dellabel(name_old)
                    shp.addlabel=name_new
            
            ### Remake list
            self.parent.parent.lbl._dellabel(name_old)
            
            return True
        else:
            #log("Inconsistent")            
            return False
            
class _racime(object):
   
    def __init__(self, parent, key):
        
        self.parent = parent
        self._key = key
        self._draw = False
        
        if not self.parent.racimes[key]:
        
            self.parent.racimes[self._key]["action"] = ""
            self.parent.racimes[self._key]["group"] = 0
            self.parent.racimes[self._key]["z-order"] = 0.
            self.parent.racimes[self._key]["labels"] = []
            self.parent.racimes[self._key]["group_label"] = ""
            
            self.parent.racimes[self._key]["element"] = []
            self.parent.racimes[self._key]["l1"] = None
            self.parent.racimes[self._key]["l2"] = None
            self.parent.racimes[self._key]["l3"] = None
            self.parent.racimes[self._key]["origin"] = None
            self.parent.racimes[self._key]["separation"] = 1
    
    #############################################
    
    def copy(self):
        
        ### To change
        
        shp = self.parent._additem(self.action, group = self.group)
        
        for key in self.parent.racimes[self.id].keys():
            
            self.parent.racimes[shp.id][key] = copy.deepcopy(self.parent.racimes[self.id][key])
           
    def move(self, mpto):
        
        ### To change
        
        lst = []
        
        for pto in self.addpto:        
            
            lst.append( pto.copy() )
            new_pto = lst[-1]
            
            new_pto.x = new_pto.x + mpto.x
            new_pto.y = new_pto.y + mpto.y
            new_pto.z = new_pto.z + mpto.z
            
        self.parent.racimes[self._key]["ptos"] = copy.deepcopy(lst)   
    
    def draw_group_elements(self, units = ""):
        
        ### Draw lines
        pass
        
    def draw_group_elements(self, units = ""):
        
        ### Draw lines        
        pass
    
    #############################################
    def add_element(self, text, thickness = None, separation = None):
                
        self.parent.racimes[self._key]["element"].append([text, thickness, separation])
    
    @property
    def l1(self):
        return self.parent.racimes[self._key]["l1"]
        
    @l1.setter
    def l1(self, value):
        self.parent.racimes[self._key]["l1"] = value
        
    @property
    def l2(self):
        return self.parent.racimes[self._key]["l2"]
        
    @l2.setter
    def l2(self, value):
        self.parent.racimes[self._key]["l2"] = value    

    @property
    def l3(self):
        return self.parent.racimes[self._key]["l3"]
        
    @l3.setter
    def l3(self, value):
        self.parent.racimes[self._key]["l3"] = value   

    @property
    def origin(self):
        return self.parent.racimes[self._key]["origin"]
        
    @l3.setter
    def origin(self, value):
        self.parent.racimes[self._key]["origin"] = value     

    @property
    def separation(self):
        return self.parent.racimes[self._key]["separation"]
        
    @separation.setter
    def separation(self, value):
        self.parent.racimes[self._key]["separation"] = value          
    
    #############################################
    
    @property
    def id(self):
        return self._key      
    
    @property
    def action(self):
        return self.parent.racimes[self._key]["action"]
        
    @action.setter
    def action(self, value):
        self.parent.racimes[self._key]["action"] = value
    
    @property
    def group(self):
        return self.parent.racimes[self._key]["group"]
        
    @group.setter
    def group(self, value):
        self.parent.racimes[self._key]["group"] = int(value)
        
    @property
    def zorder(self):
        return self.parent.racimes[self._key]["z-order"]
        
    @zorder.setter
    def zorder(self, value):
        self.parent.racimes[self._key]["z-order"] = float(value)  

    @property
    def _labels(self):
        return self.parent.racimes[self._key]["labels"]
        
    @property
    def labels(self):
        return copy.deepcopy(self.parent.racimes[self._key]["labels"])
       
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
                if not value in self.parent.racimes[self._key]["labels"]:
                    self.parent.racimes[self._key]["labels"].append(value)
                return True
            else:
                #log("The label %s has not been previously declared" % value)
                return False
            
    def dellabel(self, value):
        if value in self.parent.labels:
            if value in self.parent.racimes[self._key]["labels"]:
                newlst = [x for x in self.labels if x != value]
                self.parent.racimes[self._key]["labels"] = newlst
                return True
            else:
                #log("The label %s has not been added before" % value)            
                return False
        else:
            #log("The label %s has not been previously declared" % value)            
            return False
                
    def __repr__(self):
        return self.__class__
        
    def __str__(self):
        
        return "Racime key:%s group=%i NumRacimes:%i" % (self.id, self.group, len(self.parent.racimes))                
    
    @property
    def grouplabel(self):
        return self.parent.racimes[self._key]["group_label"]
        
    @group.setter
    def grouplabel(self, value):
        self.parent.racimes[self._key]["group_label"] = int(value)    
        
    #############################################           