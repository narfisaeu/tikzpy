
import pyTikZ.cls_points as cls_points
import pyTikZ.obj_data as obj_data
import copy

class clsdata(object):

    def __init__(self):

        self.pto = cls_points._points(self)

        self.options = obj_data._clsdata(type = {})
