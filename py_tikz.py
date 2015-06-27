import os, sys
import cls_points
import cls_shapes
import cls_labels
import cls_groups
import obj_data
import subprocess

def log(txt):
    
    print txt
    
class pytikz(object):
   
    def __init__(self):
        
        ### Data
        self.pto = cls_points._points(self)
        self.shp = cls_shapes._shapes(self)
        self.lbl = cls_labels._labels(self)
        self.grp = cls_groups._groups(self)
        
        self.opt = obj_data._clsdata(type = None)
        
        ### options
        self.opt.units = ""
        self.opt.scale = 1.
        self.opt.scaletext = 1.
        self.opt.description = "Created with pytikz" 
        self.opt.extension = ".tikz.tex"
        self.opt.dpi = 300
    
    ###########################
    
    def move_list_shapes(self, vector, lst):
    
        for shp in lst:
            
            shp.move(vector)
        
        
    def copy_list_shapes(self, lst):
        
        lst_out = []
        for shp in lst:
            
            lst_out.append( shp.copy() )
        
        return lst_out
        
    def add_label_to_list_shapes(self, lst, label):
        
        self.shp.addlabel = label
        
        for shp in lst:
            
            shp.addlabel = label
            
    def del_label_to_list_shapes(self, lst, label):
        
        for shp in lst:
            
            shp.dellabel(label)
    
    ###########################    
    
    def save_pdf(self, path, name):
        
        ### Default extension .tikz.tex
        #route_png = os.path.join(path, name + ".png")
        route_pdf = os.path.join(path, name + ".tikz.pdf")
        route_tik = os.path.join(path, name + self.extension)
        
        self._write_tikz(route_tik, True)
        
        ### Convert  
        """
        lst = ["cd",path]
        p = subprocess.Popen(lst, stdout=subprocess.PIPE, shell=True)        
        out, err = p.communicate()
        log(out)        
        """
        lst = ["pdflatex", route_tik]
        p = subprocess.Popen(lst, stdout=subprocess.PIPE, shell=True)        
        out, err = p.communicate()
        #log(out)
        """
        lst = ["convert","-density","%i" % self.dpi,route_pdf,route_png]
        p = subprocess.Popen(lst, stdout=subprocess.PIPE, shell=True)        
        out, err = p.communicate()
        log(out)         
        """
        
        return route_pdf
        
    def save_tikz_stanalone(self, path, name):
        
        ### Default extension .tikz.tex
        route = os.path.join(path, name + self.extension)
        
        self._write_tikz(route, True)
        
    def save_tikz(self, path, name):
        
        ### Default extension .tikz.tex
        route = os.path.join(path, name + self.extension)
        
        self._write_tikz(route)
        
    ###########################
    
    def _write_tikz(self, path, intex = False):
    
        with open(path, 'w') as f:
            
            self._header_open(f, intex)
            
            self._add_lines(f)
            
            self._close(f, intex)
            
        f.close()
    
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
            
            txt = r"\usetikzlibrary{shapes,arrows,decorations,decorations.pathmorphing,arrows.meta,patterns,decorations.markings}"
            self._wline(f,txt,0)              
            self._wline(f,"",0)              
            
            txt = r"\begin{document}"
            self._wline(f,txt,0)
            
        txt = r"%% Use \usepackage{tikz}"
        self._wline(f,txt,0)  
        txt = r"%% Use \usetikzlibrary{shapes,arrows,decorations, decorations.pathmorphing,arrows.meta,patterns}"                        
        self._wline(f,txt,0) 
        txt = r"\begin{tikzpicture}[scale=%.4f]" % self.scale
        self._wline(f,txt,0)
        txt = r"\tikzstyle{every node}=[scale=%.4f]" % self.scale_text
        self._wline(f,txt,1)
        self._wline(f,"",1)
        
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
    
    ###########################
    
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
        