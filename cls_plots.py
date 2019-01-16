#!/usr/bin/python

import math
import numbers
import obj_data
import copy

import plots.cls_racime as asse_rac

def log(txt):

    print txt

class _plots(object):

    """**Plots class:**

    .. _plots_cls:

    :platform: Unix, Windows
    :synopsis: buld-in plots based on pyTikZ

    :properties:
        Available plots:
            * Racime

    **Chracteristics of a shape (shp) object**

        * Each shape object has different properties depending on the nature of the shape

    """

    def __init__(self, parent):

        self.parent = parent

        ### Counters
        self.counters = obj_data._clsdata(type = int(0))

        ### Dictionary of lines
        self.assemblys = obj_data._clsdata(type = {})
        self.counters["assemblys"] = 0

    def __getitem__(self, key):

        return self.getitem(key)

    def keys(self):

        return self.assemblys.keys

    def getitem(self, key):

        ### Give a point
        _key = str(key)
        if self.assemblys[_key]:
            return _assembly(self,_key, self.assemblys[_key]["action"])
        else:
            return None
    ##########################################
    def racime(self, group = 0):

        """
        .. _racime_plot:

        **Synopsis:**
            * Returns a racime plot object

        **Args:**
            * None

        **Optional parameters:**
            * group = 0: group id

        **Returns:**
            * A racime plot object

        **Usage**

            * See :doc:`plots examples </_examples/pytikZ_plots/test_gen>`

        """

        rac = self._additem("racime", group = group)

        rac._handler.load_data_ini(rac)

        return rac

    ##########################################
    def _additem(self, type, group = 0):

        # Create auto new
        _key =  "rac#%i" % self.counters["assemblys"]
        self.counters["assemblys"] = self.counters["assemblys"] + 1
        self.assemblys[_key] = {}

        lline = _assembly(self,_key, type)
        lline.group = group
        lline.action = type
        lline.addlabel = "default"
        lline.group_label = "##group##" + _key
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

            ### Delete from all the assemblys
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

            ### Delete from all the assemblys
            for key in self.keys():
                shp = self.getitem(key)
                if name_old in self.assemblys[key]["labels"]:
                    shp.dellabel(name_old)
                    shp.addlabel=name_new

            ### Remake list
            self.parent.lbl._dellabel(name_old)

            return True
        else:
            #log("Inconsistent")
            return False

class _assembly(object):

    def __init__(self, parent, key, type):

        self.parent = parent
        self._key = key
        self._draw = False

        if not self.parent.assemblys[key]:

            self.parent.assemblys[self._key]["action"] = ""
            self.parent.assemblys[self._key]["group"] = 0
            self.parent.assemblys[self._key]["z-order"] = 0.
            self.parent.assemblys[self._key]["labels"] = []
            self.parent.assemblys[self._key]["group_label"] = ""
            self.parent.assemblys[self._key]["mpto"] = None

        if type == "racime":
            self._handler = asse_rac._racime(self.parent)
        else:
            raise Error

        #Setter and getter properties dynamically add
        for ele in self._handler.lst_data:
            self.addProperty(ele)

    def addProperty(self, attribute):
        # create local setter and getter with a particular attribute name
        getter = lambda self: self._getProperty(attribute)
        setter = lambda self, value: self._setProperty(attribute, value)

        # construct property attribute and add it to the class
        setattr(self.__class__, attribute, property(fget=getter, \
                                                    fset=setter, \
                                                    doc="Auto-generated method"))

    def _setProperty(self, attribute, value):
        #print "Setting: %s = %s" %(attribute, value)
        #self.parent.assemblys[self._key][attribute] = value
        self._handler.set_property(attribute, value, self._key)

    def _getProperty(self, attribute):
        #print "Getting: %s" %attribute
        #return self.parent.assemblys[self._key][attribute]
        return self._handler.get_property(attribute, self._key)

    #############################################

    def copy(self):

        ### To change

        shp = self.parent._additem(self.action, group = self.group)

        for key in self.parent.assemblys[self.id].keys():

            self.parent.assemblys[shp.id][key] = copy.deepcopy(self.parent.assemblys[self.id][key])

    def move(self, mpto):
        ### Move function
        self.parent.assemblys[self._key]["mpto"] = mpto.copy()

    def draw_group_elements(self, asse, units = ""):

        shps = self._handler.draw_group_elements(units, asse)
        if type(shps) != type([]):
            log("Error draw_group_elements function definition")

        ### Common practices
        for shp in shps:
            # Edit zorder
            zorder = shp.zorder
            zorder = (zorder / 10000.) + self.parent.assemblys[self._key]["z-order"]
            shp.zorder = zorder

            # Add common group label
            shp.group_label = self.parent.assemblys[self._key]["group_label"]

            # Add labels
            for lbl in self.parent.assemblys[self._key]["labels"]:
                shp.addlabel = lbl

        ### Move
        mpto = self.parent.assemblys[self._key]["mpto"]
        #if mpto:
        #    self.parent.parent.move_list_shapes( mpto, shps)

        # Add labels
        for lbl in self.parent.assemblys[self._key]["labels"]:
            self.parent.parent.add_label_to_list_shapes(shps, lbl)

    #############################################

    def add_element(self, text, thickness = "thin", separation = None):

        self.parent.assemblys[self._key]["element"].append([text, thickness, separation])

    '''
    @property
    def l1(self):

        return self.parent.assemblys[self._key]["l1"]

    @l1.setter
    def l1(self, value):

        self.parent.assemblys[self._key]["l1"] = value
    '''
    #############################################

    @property
    def id(self):
        return self._key

    @property
    def action(self):

        return self.parent.assemblys[self._key]["action"]

    @action.setter
    def action(self, value):

        self.parent.assemblys[self._key]["action"] = value

    @property
    def group(self):
        return self.parent.assemblys[self._key]["group"]

    @group.setter
    def group(self, value):
        self.parent.assemblys[self._key]["group"] = int(value)

    @property
    def zorder(self):
        return self.parent.assemblys[self._key]["z-order"]

    @zorder.setter
    def zorder(self, value):
        self.parent.assemblys[self._key]["z-order"] = float(value)

    @property
    def _labels(self):
        return self.parent.assemblys[self._key]["labels"]

    @property
    def labels(self):
        return copy.deepcopy(self.parent.assemblys[self._key]["labels"])

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
                if not value in self.parent.assemblys[self._key]["labels"]:
                    self.parent.assemblys[self._key]["labels"].append(value)
                return True
            else:
                self.parent.addlabel = value
                if not value in self.parent.assemblys[self._key]["labels"]:
                    self.parent.assemblys[self._key]["labels"].append(value)
                return True

    def dellabel(self, value):
        if value in self.parent.labels:
            if value in self.parent.assemblys[self._key]["labels"]:
                newlst = [x for x in self.labels if x != value]
                self.parent.assemblys[self._key]["labels"] = newlst
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

        return "assembly key:%s group=%i Num assemblys:%i" % (self.id, self.group, len(self.parent.assemblys))

    @property
    def grouplabel(self):
        return self.parent.assemblys[self._key]["group_label"]

    @group.setter
    def grouplabel(self, value):
        self.parent.assemblys[self._key]["group_label"] = int(value)

    #############################################
