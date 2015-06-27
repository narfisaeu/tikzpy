import copy
import obj_data

def log(txt):
    
    print txt

class _labels(object):

    def __init__(self, parent):
    
        self.parent = parent
        self.__labels = {}
        self.addlabel = "default"
    
    ################
    def list_active_labels(self, active = True):
        
        if type(active) is type(True):
            lst = []
            for key in self._labels:
                
                if self.__labels[key].active == active:
                    lst.append(key)
            
            return lst  
        else:
            return None
            
    def set_all_active(self, active = True):
        
        if type(active) is type(True):
            self.set_active_labels(self._labels, active = active)
    
    def set_active_labels(self, value, active = True):
        
        ### List or name
        ### True all active False all inactive
        if type(active) is type(True):
            if type(value) is type([]):
                for val in value:
                    self.set_active_labels(val,active = active)
            elif type(value) is type(True):
                self.set_all_active(active = value)
            else:
                if value in self._labels:
                    self.__labels[value].active = active          
                else:
                    pass
    
    ################    
    @property
    def _labels(self):
        return self.__labels.keys()
        
    @property
    def labels(self):
        return copy.deepcopy(self._labels)
        
    @property
    def addlabel(self):
        return self.labels
        
    @addlabel.setter
    def addlabel(self, value):
        
        if value in self.__labels:
            #log("The label %s has been previously declared" % value)
            return False
        else:
            self.__labels[value] = _label() 
            return True   
            
    def _dellabel(self, value):            
        
        self.__labels.pop(value,None)
        return True
        
class _label(object):

    def __init__(self):
    
        self.active = True