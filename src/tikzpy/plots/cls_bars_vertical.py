# python3

import os,sys
import math
import numbers
import tikzpy.obj_data
import copy
import types
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import cls_plots

def log(txt):

    print(txt)

class _bars_vertical(object):

    """**Vertical bars plot:**

    .. _bars_vertical_cls:

    Creates a vertical bars plot.

    :ivar p0: initial point of the plot
    :ivar sep_L: height of the bars
    :ivar width: width of the longer bar
    :ivar width: width of the longer bar
    :ivar lst_title: shapes conform the title
    :ivar title: text of the title
    :ivar lbl_axis0: label to use in the data buffer for bars values
    :ivar lbl_label1: label to use in the data buffer for bars text column 2
    :ivar lbl_label2: label to use in the data buffer for bars text column 3
    :ivar lst_text2: shapes conform the vertical text column 2
    :ivar lst_text3: shapes conform the vertical text column 3
    :ivar lst_path0: shapes conform the bars
    :ivar shps: all the shapes that conform the plot

    :Functions:
        * :ref:`draw_plot() <assem_draw_plot>`
        * :ref:`load_data_buffer(data_buff) <assem_load_load_data_buffer>`

    **Usage**

        * See :doc:`plots examples </_examples/tikzpy_plots/test_gen>`, :ref:`example 1 <ex_plots_bars_vertical_1>`, :ref:`example 2 <ex_plots_bars_vertical_2>`

    """

    def __init__(self, parent):

        self._parent = parent
        self._tik = self._parent.parent

        ### List of data properties and setup
        self.lst_data_conf = ["p0","sep_L","width", "lst_title", "title", "lst_text2", "lst_text3", "lst_path0"]
        ### List of labels from databuffer to define the axis
        self.lst_data_conf += ["data_buff","shps"]
        self.lst_data_conf += ["lbl_axis0", "lbl_label1", "lbl_label2"]

    def load_data_ini(self, assem):
        ### Initialize properties
        _key = assem.id

        self._parent.assemblys[_key]["data_buff"] = None
        self._parent.assemblys[_key]["shps"] = []

        self._parent.assemblys[_key]["p0"] = None
        self._parent.assemblys[_key]["sep_L"] = 1
        self._parent.assemblys[_key]["width"] = 5
        self._parent.assemblys[_key]["lst_title"] = []
        self._parent.assemblys[_key]["title"] = ""
        self._parent.assemblys[_key]["lst_text2"] = []
        self._parent.assemblys[_key]["lst_text3"] = []
        self._parent.assemblys[_key]["lst_path0"] = []

    def set_property(self, attribute, value, _key):
        ### Properties setter bottleneck
        if attribute == "p0":
            self._parent.assemblys[_key][attribute] = value.copy()
        else:
            self._parent.assemblys[_key][attribute] = value

    def get_property(self, attribute, _key):
        ### Properties getter bottleneck

        return self._parent.assemblys[_key][attribute]

    ############# declare methods functions

    def add_element(self, text, handler, thickness = "thin", separation = None):

        #handler.parent.assemblys[handler._key]["element"].append([text, thickness, separation])
        handler.element.append([text, thickness, separation])

    def load_data_buffer(self, handler, data_buff):

        if data_buff is None: self._tik.error("data_buffer is a None object", ref = "ver_bar")

        handler.data_buff = data_buff

    ############# Main draw function

    def draw_group_elements(self, units, assem):
        ### Draw group of shapes function call from main drawer functions
        ### Common heander
        tik = self._tik
        _key = assem.id
        shps = []
        ##

        # Loop elements
        for ii in range(0,len(assem.data_buff[assem.lbl_axis0])):

            # Normalize data
            max_length = np.max(assem.data_buff[assem.lbl_axis0])
            aux_lbl_axis0 = assem.lbl_axis0 + tik.dbuffer.aux_def + "0"
            assem.data_buff[aux_lbl_axis0] = assem.width * assem.data_buff[assem.lbl_axis0] / (1.0 * max_length)

            # Add paths
            l1 = tik.shp.path([], layer = 0)
            if ii == 0: p0 = assem.p0
            else: p0 = p3.copy()
            l1.addpto = p0
            p1=p0.copy()
            p1.x = p1.x + assem.data_buff[aux_lbl_axis0][ii] / 2.
            l1.addpto = p1
            p2=p1.copy()
            p2.y = p2.y + assem.sep_L
            l1.addpto = p2
            p3=p2.copy()
            p3.x = p3.x - assem.data_buff[aux_lbl_axis0][ii] / 2.
            l1.addpto = p3
            p4=p3.copy()
            p4.x = p4.x - assem.data_buff[aux_lbl_axis0][ii] / 2.
            l1.addpto = p4
            p5=p4.copy()
            p5.y = p5.y - assem.sep_L
            l1.addpto = p5
            l1.addpto = p0

            l1.zorder = assem.zorder
            l1.addlabel = assem.labels
            assem.lst_path0.append(l1)

            # Add text3
            ptxt3 = p0.copy()
            ptxt3.y = ptxt3.y + assem.sep_L/2.
            txt3 = tik.shp.text(ptxt3, assem.data_buff[assem.lbl_label1][ii], layer=0, color='', fill='', rotate_text=0, position='', align='center')
            txt3.zorder = assem.zorder + 1e-6
            txt3.addlabel = assem.labels

            assem.lst_text3.append(txt3)

            # Add text2
            ptxt2 = p1.copy()
            ptxt2.y = ptxt2.y + assem.sep_L/2.
            ptxt2.x = ptxt2.x
            txt2 = tik.shp.text(ptxt2, assem.data_buff[assem.lbl_label2][ii], layer=0, color='', fill='', rotate_text=0, position='right', align='right')
            txt2.zorder = assem.zorder + 1e-6
            txt2.addlabel = assem.labels

            assem.lst_text2.append(txt2)

            # Title
            if ii == 0:
                pto_title = p0.copy()
                pto_title.y = pto_title.y - assem.sep_L/2.
                tit = tik.shp.text(pto_title, assem.title, layer=0, color='', fill='', rotate_text=0, position='', align='center')
                tit.zorder = assem.zorder + 1e-6
                tit.addlabel = assem.labels
                assem.lst_title.append(tit)

        assem.shps = assem.shps + assem.lst_path0 + assem.lst_text3 + assem.lst_text2 + assem.lst_title
        ### Common return
        return assem.shps

    def is_number(self, s):
        try:
            if s is None: return False
            float(s)
            return True
        except ValueError:
            return False
