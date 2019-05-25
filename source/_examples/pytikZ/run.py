import os
import sys

txt = "test_pytikz_01.tikz"

def run_latex(name):
       
    ### latex
    txt = "latex %s" % (name)
    os.system(txt)      
    
    ### bibtex
    txt = "bibtex %s" % (name)    
    os.system(txt)    
    
    ### nomenclature
    txt = "makeindex %s.nlo -s nomencl.ist -o %s.nls" % (name,name)    
    os.system(txt)     
    
    ### ps    
    txt = "dvips %s.dvi -o %s.ps" % (name,name)
    os.system(txt)
    
    ### dvi to pdf
    #txt = "dvipdf %s.dvi %s.pdf" % (name,name)
    #os.system(txt)
    
    ### ps to pdf
    txt = "ps2pdf %s.ps %s_ps.pdf" % (name,name)
    os.system(txt)
   
def run_latex_pdf(name):
       
    ### latex
    txt = "pdflatex %s" % (name)
    os.system(txt)      
    
    ### bibtex
    txt = "bibtex %s" % (name)    
    os.system(txt)    
    
    
run_latex(txt)
#run_latex(txt)

#run_latex_pdf(txt)
