
# python3

import math
import numbers
import tikzpy.obj_data as obj_data
import copy

import tikzpy.plots.cls_racime as asse_rac
import tikzpy.plots.cls_bars_vertical as bars_vertical
import tikzpy.plots.cls_arrow_vertical as arrow_vertical

def log(txt):

    print(txt)

class _plots(object):

    """**Plots class:**

    .. _plots_cls:

    :platform: Unix, Windows
    :synopsis: buld-in plots based on tikzpy

    :Available plots:
        * Racime
        * Vertical bars plots

    **Chracteristics of a plot object**

        * Each plot object has different properties depending on the nature of the plot.

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

            * See :doc:`plots examples </_examples/tikzpy_plots/test_gen>`, :ref:`example 1 <ex_plots_racime_1>`, :ref:`example 2 <ex_plots_racime_2>`

        """

        rac = self._additem("racime", group = group)

        rac._handler.load_data_ini(rac)

        return rac

    def bars_vertical(self, group = 0):

        """
        .. _bars_vertical_plot:

        **Synopsis:**
            * Returns a vertical bars plot object

        **Args:**
            * None

        **Optional parameters:**
            * group = 0: group id

        **Returns:**
            * A vertical bars plot object

        **Usage**

            * See :doc:`plots examples </_examples/tikzpy_plots/test_gen>`, :ref:`example 3 <ex_plots_bars_vertical_1>`, :ref:`example 4 <ex_plots_bars_vertical_2>`
            * See :ref:`vertical plot object <bars_vertical_cls>`

        """

        rac = self._additem("bars_vertical", group = group)

        rac._handler.load_data_ini(rac)

        return rac

    def arrow_vertical(self, group = 0):

        """
        .. _arrow_vertical_plot:

        **Synopsis:**
            * Returns a vertical arrow plot object

        **Args:**
            * None

        **Optional parameters:**
            * group = 0: group id

        **Returns:**
            * A vertical arrow plot object

        **Usage**

            * See :doc:`plots examples </_examples/tikzpy_plots/test_gen>`, :ref:`example 1 <ex_plots_arrow_vertical_1>`
            * See :ref:`vertical plot object <arrow_vertical_cls>`

        """

        rac = self._additem("arrow_vertical", group = group)

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

        if not self.parent.assemblys[key]:

            self.parent.assemblys[self._key]["action"] = ""
            self.parent.assemblys[self._key]["group"] = 0
            self.parent.assemblys[self._key]["z-order"] = 0.
            self.parent.assemblys[self._key]["labels"] = []
            self.parent.assemblys[self._key]["group_label"] = ""
            self.parent.assemblys[self._key]["mpto"] = None
            self.parent.assemblys[self._key]["_draw"] = False

        if type == "racime":
            self._handler = asse_rac._racime(self.parent)
        elif type == "bars_vertical":
            self._handler = bars_vertical._bars_vertical(self.parent)
        elif type == "arrow_vertical":
            self._handler = arrow_vertical._arrow_vertical(self.parent)
        else:
            raise Error

        #Setter and getter properties dynamically add
        for ele in self._handler.lst_data_conf:
            self.addProperty(ele)

        #Add methods
        #self._handler.load_methods(self,key)

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
        if mpto:
            #self.parent.parent.move_list_shapes( mpto, shps)
            self.parent.parent.shp.translate(shps, x=mpto.x, y=mpto.y, z=mpto.z)

        # Add labels
        for lbl in self.parent.assemblys[self._key]["labels"]:
            self.parent.parent.add_label_to_list_shapes(shps, lbl)

    ############# declared methods functions

    def add_element(self, *args, **kwargs):

        return self._handler.add_element(*args+(self,), **kwargs)

    def load_data_buffer(self, data_buff):

        """
        .. _assem_load_load_data_buffer:

        **Synopsis:**
            * Loads a data buffer file into the plot to be plot in case is required

        **Args:**
            * data_buff object (see :ref:`Data buffer class <dbuffer_cls>`)

        **Optional parameters:**
            * units = None (by default the tikzpy units will be use)

        **Returns:**
            * None

        **Usage**
            * See :ref:`example 3 <ex_plots_bars_vertical_1>`

        """

        self._handler.load_data_buffer(self, data_buff)

    def draw_plot(self, units = None):

        """
        .. _assem_draw_plot:

        **Synopsis:**
            * Draw / load the plot. The elements that compose the plot become accessible. Once is draw it can not be draw again.

        **Args:**
            * None

        **Optional parameters:**
            * units = None (by default the tikzpy units will be use)

        **Returns:**
            * None

        **Usage**
            * See :ref:`example 3 <ex_plots_bars_vertical_1>`

        """
        if self.parent.assemblys[self._key]["_draw"] == False:

            plots = self.parent.parent.plots.getitem(self._key)

            if units is None: units = self.parent.parent.units
            plots.draw_group_elements(plots, units = units)

            self.parent.assemblys[self._key]["_draw"] = True

    #def _add_element(self, text, thickness = "thin", separation = None):

    #    print self.element
    #    #self.parent.assemblys[self._key]["element"].append([text, thickness, separation])
    #    self.element.append([text, thickness, separation])
    #    print self.element

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
