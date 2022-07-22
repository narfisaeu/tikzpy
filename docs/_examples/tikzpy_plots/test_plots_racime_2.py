#!/usr/bin/python

### Load tikzpy library
import os, sys
import numpy as np
import tikzpy as py_tikZ

class pic_scatter_prop(object):

    def __init__(self):

        self.tik = py_tikZ.pytikz()

    def run(self):

        self.tik.scale = 1.00
        self.tik.scale_text = 1.20

        self.points()
        self.drawing_comp()

        ### Make drawing
        path = os.path.dirname(os.path.abspath(__file__))
        name = os.path.basename(os.path.abspath(__file__))
        name = os.path.splitext(name)[0]
        self.tik.save_pdf(path, name, as_png = True)

    def points(self):

        self.p0 = self.tik.pto.pto(0,0,0)
        self.p1 = self.tik.pto.pto(1,1,0)

        xserie = [4.19, 14.86, 28.96, 39.25, 50.31]
        xserie1 = [4, 15.2, 26.4, 37.6, 48.8, 60]

        self.names = ["-C1", "-C2", "-C3", "-C4", "-C5", "-C6"]

        self.WI_avg = [719.4, 769.6, 837.8, 822.2, 685.1]
        self.WI_std = [73.3016565, 48.3582111, 30.71350422, 49.4786026, 45.27070637]

        self.WJ_avg = [623.1, 629.8, 670.1, 707.9, 671.3, 589.5]
        self.WJ_std = [48.49166303, 39.85523282, 41.96451536, 35.58120776, 54.91708268, 33.78103112]

        self.WM_avg = [739.9, 725.1, 698.2, 700.7, 755.6, 709.2]
        self.WM_std = [46.37049136, 44.43828625, 48.93533058, 27.24455085, 76.17562546, 96.96469509]

        self.WJ_avg_ten = [862.9127972, 885.3821492, 864.2301528, 853.1920925, 886.1908006]
        self.WJ_std_ten = [34.12315274, 20.53210185, 37.15676289, 31.62798934, 27.26881549]

        self.WM_avg_ten = [856.7283735, 828.5132667, 799.5322142, 829.2538277, 850.4567135]
        self.WM_std_ten = [30.88654937, 25.27209811, 22.05096108, 34.11512839, 20.77847733]

        self.WJ_avg_ILSS = [32.44955411, 34.68039656, 39.34979163, 40.93728194, 32.55181904]
        self.WJ_std_ILSS = [1.876029752, 0.653081672, 1.677962676, 1.965138951, 1.705132996]

        self.WM_avg_ILSS = [35.32078312, 32.60281401, 31.040988, 33.62553998, 36.70709027]
        self.WM_std_ILSS = [0.890769464, 1.083362528, 1.217875935, 1.007511884, 1.06591193]

    def drawing_comp(self, option = 0):

        shps = []

        vals = [1, 5, 3, 0.5, 8.]
        [sep, l1, l2, l3,thick] = vals

        def draw(p, avg, std, name, txt, shps, vals, separation=[], thickness=[]):

            [sep, l1, l2, l3,thick] = vals

            ## Calc
            rac = self.tik.plots.racime(group = 0)
            rac.l1 = l1
            rac.l2 = l2
            rac.l3 = l3
            rac.separation = sep
            rac.origin = self.p0

            cov_tot = 0
            for i in range(0,len(avg)):
                cov = std[i]*100./avg[i]
                cov_tot = cov_tot + cov

            for i in range(0,len(avg)):

                cov = std[i]*100./avg[i]
                if separation == []:
                    rac.add_element("\\textbf{%s%s}, COV %.1f" %(txt,name[i],cov), thickness = thick*cov/cov_tot)
                else:
                    rac.add_element("\\textbf{%s%s}, COV %.1f" %(txt,name[i],cov), thickness = thickness[i], separation=separation[i])

            rac.move(p)
            rac.addlabel="patatin"
            shps.append(rac)

            return rac

        WI_avg, WI_std = self.WI_avg, self.WI_std
        WJ_avg, WJ_std = self.WJ_avg, self.WJ_std
        WM_avg, WM_std = self.WM_avg, self.WM_std

        p = self.p0
        racWI = draw(p, WI_avg, WI_std, self.names, "Plate A", shps, vals)

        p.y = p.y + racWI.total_height + 1.5* sep
        racWJ = draw(p, WJ_avg, WJ_std, self.names, "Plate B", shps, vals)

        p.y = p.y + racWJ.total_height + 1.5* sep
        racWM = draw(p, WM_avg, WM_std, self.names, "Plate C", shps, vals)

        p = racWI.p_vertex[0]
        def plate_calcs(avg, std):
            mean = np.mean(avg)
            sq_sum = np.sum(np.asarray(std)**2.) #/ (len(std)**2.)
            std = sq_sum**0.5
            return mean, std

        vals = [1, 3.9, 3, 0.5, 8.]
        [sep, l1, l2, l3,thick] = vals
        meanWI, stdWI = plate_calcs(WI_avg, WI_std)
        meanWJ, stdWJ = plate_calcs(WJ_avg, WJ_std)
        meanWM, stdWM = plate_calcs(WM_avg, WM_std)
        avg = [meanWI, meanWJ, meanWM]
        std = [stdWI, stdWJ, stdWM]
        names = ["\\textbf{Plate A}","\\textbf{Plate B}","\\textbf{Plate C}"]
        separation = [racWI.total_height/2. + 1.5* sep+ racWJ.total_height/2.,racWJ.total_height/2. + 1.5* sep+ racWM.total_height/2.,0]
        thickness = [racWI.end_thickness,racWJ.end_thickness,racWM.end_thickness]

        racplate = draw(p, avg, std, names, "", shps, vals, separation=separation, thickness=thickness)

        meanPlates, stdPlates = plate_calcs(avg, std)
        #meanPlates, stdPlates = plate_calcs(self.WI_avg+self.WJ_avg+self.WM_avg, self.WI_std+self.WJ_std+self.WM_std)
        COVplates = stdPlates*100./meanPlates

        pp = racplate.p_vertex[0]
        p = racplate.p_vertex[0]
        p.x = p.x + l2*1.5
        l1 = self.tik.shp.line(pp,p,layer=0)

        if thickness: l1.thick = racplate.end_thickness
        shps.append(l1)

        p = racplate.p_vertex[0]
        p.x = p.x + l2*1.5/2.
        p.y = p.y + 0.4
        l = self.tik.shp.text(p, "\\textbf{Plates A,B,C}, COV %.1f" % COVplates,0)
        l.align = 0
        l.position = "above"
        shps.append(l)

if __name__ == "__main__":

    obj = pic_scatter_prop()

    obj.run()
