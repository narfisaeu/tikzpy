#!/usr/bin/python
# FLC 2013

import os, sys
import cls_points
import cls_shapes
import cls_labels
import cls_plots
import cls_colors
import cls_canavas
import buffer_data.cls_data_buffer as cls_data_buff
import obj_data
import subprocess
import files_crawl as libfile

def log(txt):

    print txt

def load():

    return pytikz()

class pytikz(object):

    """Python class to build your tikZ drawings

       :platform: Unix, Windows
       :synopsis: Python class to build your tikZ drawings

       :ivar dpi=300: dots per inch property of the drawings
       :ivar extension=".tikz.tex": extension property use to build TikZ drawings
       :ivar description: drawing header description, by default "Created with pyTikZ"
       :ivar unit="": general units use in TikZ drawing, no units by default
       :ivar scale=1.: scale value of the TikZ drawing
       :ivar scale_text=1.: scale value for the nodes text the TikZ drawing
       :ivar rot_x=0.: angle (in degrees) through which the coordinate frame is rotated about the x axis
       :ivar rot_y=0.: angle (in degrees) through which the coordinate frame is rotated about the y axis
       :ivar rot_z=0.: angle (in degrees) through which the coordinate frame is rotated about the z axis

    """

    """
        For the furture:
            * Include distribution of Latex in directory
            * Include distribution of Magic in directory
            * Review 3D view. Idea use global rotate of all the points wit (rot_x, rot_y, rot_z) = 0
            -------------- Done -------------------
            * Add 3D view -- July 2016

        Install latex ubuntu:
            * sudo apt-get install texlive-full
            * sudo apt-get install xzdec
            * sudo tlmgr install pgf
            * sudo tlmgr install tikz-cd

    """

    def __init__(self):

        ### Data
        self.pto = cls_points._points(self)
        self.shp = cls_shapes._shapes(self)
        self.lbl = cls_labels._labels(self)
        self.plots = cls_plots._plots(self)
        self.col = cls_colors._colors(self)
        self.grp = cls_canavas._canavas(self)
        self.dbuffer = cls_data_buff._data_buff(self)

        self.opt = obj_data._clsdata(type = None)

        self.folderpath = os.path.dirname(os.path.abspath(__file__))

        ### options
        self.opt.units = ""
        self.opt.scale = 1.
        self.opt.scaletext = 1.
        self.opt.description = "Created with pyTikZ"
        self.opt.extension = ".tikz.tex"
        self.opt.dpi = 300
        self.opt.rot_x = 0.
        self.opt.rot_y = 0.
        self.opt.rot_z = 0.

    ########################### Functions

    def add_label_to_list_shapes(self, lst, label):

        self.shp.addlabel = label

        for shp in lst:

            shp.addlabel = label

    def del_label_to_list_shapes(self, lst, label):

        for shp in lst:

            shp.dellabel(label)

    ###########################

    def save_eps(self, path, name):

        """

        .. _save_eps:

        **Synopsis:**
            * Save TikZ drawing as a eps file for visualization purposes
            * File is save with .tikz.eps extension

        **Args:**
            * path: path to directory where the pdef files will be save
            * name: name of the eps file to be save

        **Returns:**
            * route: the complete path to the eps file

        .. note::

            * Dependent on the local latex instalation, use latex to dvi and dvips to eps (ubuntu: apt-get install texlive-full / windows: miktex.org)
            * See example

        """

        ### Default extension .tikz.tex
        #route_png = os.path.join(path, name + ".png")
        route_dvi = os.path.join(path, name + ".tikz.dvi")
        route_eps = os.path.join(path, name + ".tikz.eps")
        route_jpg = os.path.join(path, name + ".tikz.jpg")
        route_tik = os.path.join(path, name + self.extension)

        self._write_tikz(route_tik, True)

        ### Convert
        lst = ["latex", route_tik]
        if os.name == "nt":
            p = subprocess.Popen(lst, stdout=subprocess.PIPE, shell=True)
            out, err = p.communicate()
        else:
            subprocess.check_call(lst)

        lst = ["dvips", "-o", route_eps, route_dvi]
        if os.name == "nt":
            p = subprocess.Popen(lst, stdout=subprocess.PIPE, shell=True)
            out, err = p.communicate()
        else:
            subprocess.check_call(lst)

        #if as_jpg:
        #   ### Uses PIL and requeres ghostscript
        #   self._save_as_jpg(route_eps, route_jpg)

        return route_eps

    def _save_as_jpg(self, route_eps, route_jpg):
        from PIL import Image
        im = Image.open(route_eps)
        im.load(scale=2)
        im.save(route_jpg, "JPEG")

    def save_pdf(self, path, name, as_png = True, as_eps = True):

        """

        .. _save_pdf:

        **Synopsis:**
            * Save TikZ drawing as a pdf file for visualization purposes
            * File is save with .tikz.pdf extension

        **Args:**
            * path: path to directory where the pdef files will be save
            * name: name of the pdf file to be save

        **Optional parameters:**
            * as_png = True: convert the pdf to a png file
            * as_eps = True: convert the pdf to a eps file

        **Returns:**
            * route_pdf: the complete path to the pdf file

        .. note::

            * Dependent on the local latex installation, use **pdflatex** to generate a pdf (ubuntu: apt-get install texlive-full / windows: miktex.org)
            * To save pdfs as png files requires **ImageMagick** to be installed (also ghostscript in Windows), uses convert command
            * To save pdfs as eps pdftops is used
            * See example

        """

        ### Default extension .tikz.tex
        #route_png = os.path.join(path, name + ".png")
        route_pdf = os.path.join(path, name + ".tikz.pdf")
        route_png = os.path.join(path, name + ".tikz.png")
        route_eps = os.path.join(path, name + ".tikz.eps")
        route_tik = os.path.join(path, name + self.extension)

        self._write_tikz(route_tik, True)

        ### Convert
        lst = ["pdflatex", route_tik]
        if os.name == "nt":
            p = subprocess.Popen(lst, stdout=subprocess.PIPE, shell=True)
            out, err = p.communicate()
        else:
            subprocess.check_call(lst)

        ### Create png
        if as_png:
            ### ImageMagick call "%PROGRAMFILES%\ImageMagick\Convert"
            if os.name == "nt":
                #pathmagick = os.path.join("ImageMagick","magick.exe")
                #pathmagick = os.path.join(self.folderpath,pathmagick)
                #lst = [pathmagick, "-density", "%i" % self.dpi, route_pdf, "-quality", "95",route_png]
                pathmagick = os.path.join("xpdftools_bin32","pdftopng.exe")
                pathmagick = os.path.join(self.folderpath,pathmagick)
                lst = [pathmagick,"-r","300",route_pdf,route_png]

                p = subprocess.Popen(lst, stdout=subprocess.PIPE, shell=True)
                out, err = p.communicate()

                if os.path.isfile(route_png+"-000001.png"):
                    if os.path.isfile(route_png): os.remove(route_png)
                    os.rename(route_png+"-000001.png", route_png)

            else:
                lst = ["convert", "-density", "%i" % self.dpi, route_pdf, "-quality", "95",route_png]
                subprocess.check_call(lst)

        ### Create eps, pdftops
        if as_eps:
            if os.name == "nt":
                pathmagick = os.path.join("xpdftools_bin32","pdftops.exe")
                pathmagick = os.path.join(self.folderpath,pathmagick)
                lst = [pathmagick, "-eps", route_pdf, route_eps]
                p = subprocess.Popen(lst, stdout=subprocess.PIPE, shell=True)
                out, err = p.communicate()
            else:
                lst = ["pdftops", "-eps", "-r 600", route_pdf, route_eps]
                subprocess.check_call(lst)

        return route_pdf

    def _rename_png(sef,path):
        pass

    def save_tikz_stanalone(self, path, name):

        """

        .. _save_tikz_stanalone:

        **Synopsis:**
            * Save TikZ drawing as a TikZ file, including the necessary headers
            * File is save with .tikz.tex extension

        **Args:**
            * path: path to directory where the pdef files will be save
            * name: name of the tikz format file to be save

        **Returns:**
            * route: the complete path to the output file

        .. note::

            * See example

        """

        ### Default extension .tikz.tex
        route = os.path.join(path, name + self.extension)

        self._write_tikz(route, True)

        return route

    def save_tikz(self, path, name):

        """

        .. _save_tikz:

        **Synopsis:**
            * Save TikZ drawing as a TikZ file, without the headers, ready to be embedded in latex
            * File is save with .tikz.tex extension

        **Args:**
            * path: path to directory where the pdef files will be save
            * name: name of the tikz format file to be save

        **Returns:**
            * route: the complete path to the output file

        .. note::

            * See example

        """

        ### Default extension .tikz.tex
        route = os.path.join(path, name + self.extension)

        self._write_tikz(route)

        return route

    ########################### Outputting TikZ

    def _write_tikz(self, path, intex = False):

        with open(path, 'w') as f:

            self._header_open(f, intex)

            self._add_plots()

            self._add_lines(f)

            self._close(f, intex)

        f.close()

        self.log("pyTikZ number points %i, number shapes %i" % (self.pto.counters["points"], self.shp.counters["shapes"]))

    def _add_colors(self, f):

        lst = self.col._colors_to_define_lst_text()

        if len(lst) > 0:

            for l in lst:

                self._wline(f,l,1)

    def _add_plots(self):

        for key in self.plots.keys():

            plots = self.plots.getitem(key)

            if plots.parent.assemblys[key]["_draw"] == False:

                plots.draw_group_elements(plots, units = self.units)

    def _add_lines(self, f):
        ### [str,self.group,self.zorder,self.id,self.comment]

        ###Check max z
        lstzorder = []
        diczorder = {}

        for key in self.shp.keys():

            shp = self.shp.getitem(key)
            if not shp.zorder in lstzorder:
                lstzorder.append(shp.zorder)
                diczorder[shp.zorder] = []

            diczorder[shp.zorder].append(key)

        lstzorder.sort()

        ### Write lines
        lst_active = self.lbl.list_active_labels(active = True)
        for z in lstzorder:

            for key in diczorder[z]:

                shp = self.shp.getitem(key)

                lst_active_shp = shp._labels
                check = len([i for i in lst_active if i in lst_active_shp])

                if check > 0:

                    txt = shp.comment
                    if txt != "": self._wline(f,txt,1)

                    txt = shp.build_tik_string(units = self.units)

                    self._wline(f,txt,1)
        """
        ###Check max z
        for key in self.shp.keys():

            shp = self.shp.getitem(key)

            txt = shp.comment
            if txt != "": self._wline(f,txt,1)

            txt = shp.build_tik_string(units = self.units)

            self._wline(f,txt,1)
        """

    def _wline(self,f,txt,level = 0):

        txt = "\t"*level + txt + "\n"
        f.write(txt)

    def _header_open(self, f, intex = False):

        if intex:
            txt = r"\documentclass[convert={density=%i,outext=.png}]{standalone}" % self.dpi
            self._wline(f,txt,0)

            txt = r"\usepackage{tikz}"
            self._wline(f,txt,0)

            if self._add_3D():
                txt = r"\usepackage{tikz-3dplot}"
                self._wline(f,txt,0)

            txt = r"\usetikzlibrary{shapes,arrows,decorations,decorations.pathmorphing,arrows.meta,patterns,decorations.markings}"
            self._wline(f,txt,0)
            self._wline(f,"",0)

            txt = r"\begin{document}"
            self._wline(f,txt,0)

        txt = r"%% Use \usepackage{tikz}"
        self._wline(f,txt,0)
        if self._add_3D():
            txt = r"%% Use \usepackage{tikz-3dplot}"
            self._wline(f,txt,0)
        txt = r"%% Use \usetikzlibrary{shapes,arrows,decorations, decorations.pathmorphing,arrows.meta,patterns}"
        self._wline(f,txt,0)

        if self._add_3D():
            txt = r"\tdplotsetmaincoords{%.2f}{%.2f}" % (self.rot_x, self.rot_z)
            self._wline(f,txt,0)
            txt = r"\begin{tikzpicture}[scale=%.4f,tdplot_main_coords]" % self.scale
        else:
            txt = r"\begin{tikzpicture}[scale=%.4f]" % self.scale
        self._wline(f,txt,0)

        txt = r"\tikzstyle{every node}=[scale=%.4f]" % self.scale_text
        self._wline(f,txt,1)

        self._wline(f,"",1)

        self._add_colors(f)

        txt = "%%" + self.description
        self._wline(f,txt,1)
        self._wline(f,"",1)

    def _close(self, f, intex = False):

        self._wline(f,"",0)
        txt = r"\end{tikzpicture}"
        self._wline(f,txt,0)

        if intex:
            txt = r"\end{document}"
            self._wline(f,txt,0)

    ########################### Properties

    @property
    def dpi(self):
        return self.opt.dpi

    @dpi.setter
    def dpi(self, value):
        self.opt.dpi = value

    @property
    def extension(self):
        return self.opt.extension

    @extension.setter
    def extension(self, value):
        self.opt.extension = value

    @property
    def description(self):
        return self.opt.description

    @description.setter
    def description(self, value):
        self.opt.description = value

    @property
    def units(self):
        return self.opt.units

    @units.setter
    def units(self, value):
        self.opt.units = value

    @property
    def scale(self):
        return self.opt.scale

    @scale.setter
    def scale(self, value):
        self.opt.scale = value

    @property
    def scale_text(self):
        return self.opt.scaletext

    @scale_text.setter
    def scale_text(self, value):
        self.opt.scaletext = value

    #### 3D perspective
    def _add_3D(self):
        if self.rot_x == 0 and self.rot_y == 0 and self.rot_z == 0:
            return False
        else:
            return True

    @property
    def rot_x(self):
        return self.opt.rot_x

    @rot_x.setter
    def rot_x(self, value):
        self.opt.rot_x = value

    @property
    def rot_y(self):
        return self.opt.rot_y

    @rot_y.setter
    def rot_y(self, value):
        self.opt.rot_y = value

    @property
    def rot_z(self):
        return self.opt.rot_z

    @rot_z.setter
    def rot_z(self, value):
        self.opt.rot_z = value

    ###########################
    def log(self, txt, ref = ""):
        print txt

    def error(self, txt, ref = ""):
        raise ValueError("%s-%s" % (ref,txt))
