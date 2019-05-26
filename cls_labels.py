<<<<<<< HEAD
import copy
import obj_data

def log(txt):
    
    print txt

class _labels(object):
    
    """**Labels class:** 
    
    .. _labels_cls:
   
    :platform: Unix, Windows
    :synopsis: Allows to manage shapes labels. Active / hide shapes using labels and filtering shapes using labels. Shapes containing hidden labels will not be shown in the picture.
           
    :ivar labels: return list containing all the lables
    
    
    """    
    
    def __init__(self, parent):
    
        self.parent = parent
        self.__labels = {}
        self.addlabel = "default"
    
    ################
    def list_active_labels(self, active = True):
        """
        .. _labels_list_active_labels:         
                
        **Synopsis:**
            * Returns a list of labels active / hide
            
        **Optional parameters:**
            * active = True: True for active labels. False for hidden labels.
            
        **Returns:**
            * Returns a list of labels active / hide
           
        .. note::
        
            * See :doc:`labels examples </_examples/pytikZ_labels/test_gen>`.
        
        """
        
        if type(active) is type(True):
            lst = []
            for key in self._labels:
                
                if self.__labels[key].active == active:
                    lst.append(key)
            
            return lst  
        else:
            return None
            
    def set_all_active(self, active = True):
        """
        .. _labels_set_all_active:         
                
        **Synopsis:**
            * Set all labels as active / hide
            
        **Optional parameters:**
            * active = True: True for active labels. False for hidden labels.
            
        **Returns:**
            * None
           
        .. note::
        
            * See :doc:`labels examples </_examples/pytikZ_labels/test_gen>`.
        
        """
        
        if type(active) is type(True):
            self.set_active_labels(self._labels, active = active)
    
    def set_active_labels(self, value, active = True):
        """
        .. _labels_set_active_labels:         
                
        **Synopsis:**
            * Set specific labels names as active / hide
        
        **Args:**
            * value: label name or list of labels names
        
        **Optional parameters:**
            * active = True: True for active labels. False for hidden labels.
            
        **Returns:**
            * None
           
        .. note::
        
            * See :doc:`labels examples </_examples/pytikZ_labels/test_gen>`.
        
        """
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
    
    def dellabel(self, value):
        """
        .. _labels_dellabel:         
                
        **Synopsis:**
            * Delete a label from all the shapes
        
        **Args:**
            * value: label name or list of labels names
            
        **Returns:**
            * None
           
        .. note::
        
            * See :doc:`labels examples </_examples/pytikZ_labels/test_gen>`.
        
        """        
        self.parent.shp._dellabel(value)
        
    def shapes_by_label(self, value):        
        """
        .. _labels_shapes_by_label:         
                
        **Synopsis:**
            * Returns a list of shapes ids that contain a label or list of labels
        
        **Args:**
            * value: label name or list of labels names
            
        **Returns:**
            * List of shapes ids. Can be used with :ref:`groups object <canavas_cls>`.
           
        .. note::
        
            * See :doc:`labels examples </_examples/pytikZ_labels/test_gen>`.
        
        """         
        return self.parent.shp._shapes_by_label(value)
        
    def label_to_shapes(self, shps, value, delete_label = False):
        """
        
        .. _labels_label_to_shapes:         
                
        **Synopsis:**
            * Add / delete a label or list of labels to a shape or list of shapes
        
        **Args:**
            * shps: list of shapes or single shape. Given by id or shape object.
            * value: label name or list of labels names
            
        **Optional parameters:**
            * delete_label = False: True add labels. False delete labels.            
            
        **Returns:**
            * None
            
        .. note::
            
            * Can be combine with :ref:`groups object <canavas_cls>` using a group of shapes **grp.shps**.
            * See :doc:`labels examples </_examples/pytikZ_labels/test_gen>`.
        
        """
        if delete_label:
            self.parent.shp._mod_properties(shps, value, "dellabel")
        else:
            self.parent.shp._mod_properties(shps, value, "addlabel")
        
    ################    
    def __getitem__(self, name):
                
        if name in self._labels:
            return self.__labels[name]
        else:
            return None  
    
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
    
=======
import copy
import obj_data

def log(txt):
    
    print txt

class _labels(object):
    
    """**Labels class:** 
    
    .. _labels_cls:
   
    :platform: Unix, Windows
    :synopsis: Allows to manage shapes labels. Active / hide shapes using labels and filtering shapes using labels. Shapes containing hidden labels will not be shown in the picture.
           
    :ivar labels: return list containing all the lables
    
    
    """    
    
    def __init__(self, parent):
    
        self.parent = parent
        self.__labels = {}
        self.addlabel = "default"
    
    ################
    def list_active_labels(self, active = True):
        """
        .. _labels_list_active_labels:         
                
        **Synopsis:**
            * Returns a list of labels active / hide
            
        **Optional parameters:**
            * active = True: True for active labels. False for hidden labels.
            
        **Returns:**
            * Returns a list of labels active / hide
           
        .. note::
        
            * See :doc:`labels examples </_examples/pytikZ_labels/test_gen>`.
        
        """
        
        if type(active) is type(True):
            lst = []
            for key in self._labels:
                
                if self.__labels[key].active == active:
                    lst.append(key)
            
            return lst  
        else:
            return None
            
    def set_all_active(self, active = True):
        """
        .. _labels_set_all_active:         
                
        **Synopsis:**
            * Set all labels as active / hide
            
        **Optional parameters:**
            * active = True: True for active labels. False for hidden labels.
            
        **Returns:**
            * None
           
        .. note::
        
            * See :doc:`labels examples </_examples/pytikZ_labels/test_gen>`.
        
        """
        
        if type(active) is type(True):
            self.set_active_labels(self._labels, active = active)
    
    def set_active_labels(self, value, active = True):
        """
        .. _labels_set_active_labels:         
                
        **Synopsis:**
            * Set specific labels names as active / hide
        
        **Args:**
            * value: label name or list of labels names
        
        **Optional parameters:**
            * active = True: True for active labels. False for hidden labels.
            
        **Returns:**
            * None
           
        .. note::
        
            * See :doc:`labels examples </_examples/pytikZ_labels/test_gen>`.
        
        """
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
    
    def dellabel(self, value):
        """
        .. _labels_dellabel:         
                
        **Synopsis:**
            * Delete a label from all the shapes
        
        **Args:**
            * value: label name or list of labels names
            
        **Returns:**
            * None
           
        .. note::
        
            * See :doc:`labels examples </_examples/pytikZ_labels/test_gen>`.
        
        """        
        self.parent.shp._dellabel(value)
        
    def shapes_by_label(self, value):        
        """
        .. _labels_shapes_by_label:         
                
        **Synopsis:**
            * Returns a list of shapes ids that contain a label or list of labels
        
        **Args:**
            * value: label name or list of labels names
            
        **Returns:**
            * List of shapes ids. Can be used with :ref:`groups object <canavas_cls>`.
           
        .. note::
        
            * See :doc:`labels examples </_examples/pytikZ_labels/test_gen>`.
        
        """         
        return self.parent.shp._shapes_by_label(value)
        
    def label_to_shapes(self, shps, value, delete_label = False):
        """
        
        .. _labels_label_to_shapes:         
                
        **Synopsis:**
            * Add / delete a label or list of labels to a shape or list of shapes
        
        **Args:**
            * shps: list of shapes or single shape. Given by id or shape object.
            * value: label name or list of labels names
            
        **Optional parameters:**
            * delete_label = False: True add labels. False delete labels.            
            
        **Returns:**
            * None
            
        .. note::
            
            * Can be combine with :ref:`groups object <canavas_cls>` using a group of shapes **grp.shps**.
            * See :doc:`labels examples </_examples/pytikZ_labels/test_gen>`.
        
        """
        if delete_label:
            self.parent.shp._mod_properties(shps, value, "dellabel")
        else:
            self.parent.shp._mod_properties(shps, value, "addlabel")
        
    ################    
    def __getitem__(self, name):
                
        if name in self._labels:
            return self.__labels[name]
        else:
            return None  
    
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
    
>>>>>>> develop
        self.active = True