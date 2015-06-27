import py_tikz as pytikz
import os

def test_points():

    tik = pytikz.pytikz()
    
    id1 = tik.pto.addpoint(1.,2)
    id2 = tik.pto.addpoint(5.,6)
    
    print  "Val id1 x ", tik.pto[id1].x, "Val id2 x ", tik.pto[id2].x
    print "Is id1 coordinates equal to id1 ", tik.pto[id1] == tik.pto[id1]
    print "Is id1 coordinates not equal to id1 ", tik.pto[id1] != tik.pto[id1]
    print "Is id1 coordinates equal to id2 ", tik.pto[id1] == tik.pto[id2]
    
    id1 = id2
    print  "Val id1 x ", tik.pto[id1].x, "Val id2 x ", tik.pto[id2].x
    
def aux_points():
    tik = pytikz.pytikz()
    
    id1 = tik.pto.addpoint(1.,2)
    p1 = tik.pto[id1]
    p2 = tik.pto.auxpoint()
    
    print p1
    p1.x = 1.5
    print p1
    p1 = tik.pto[id1]
    print p1
    print p2
    p2.x = 5
    p2.y = 6
    print p2
    id2 = p2.save()
    p2.y = 6.5
    print p2
    p2 = tik.pto[id2]
    print p2

def operators():    
    tik = pytikz.pytikz()
    
    id1 = tik.pto.addpoint(1.,2)
    p1 = tik.pto[id1]    
    p2 = tik.pto.auxpoint(5,6)
    
    print p1
    print p2
    print p1+p2
    print p2+p1
    print p1+1
    print p1+p2
    print p1-p2
    print p1-1
    print 1-p1
    print p1*p2
    print p2*p1
    print p1*2.
    print 2.*p1

def lines():    
    tik = pytikz.pytikz()
    
    tik.scale = 0.9
    
    p1 = tik.pto.pto(1,2)
    p2 = tik.pto.pto(2,5)
    
    l2 = tik.shp.line(0)
    l3 = tik.shp.line(0)
    
    l2.addpto = p1
    l2.addpto = p2
    l2.arrow = "<->"
    l2.thick = "thin"
    l2.thick = 0.2
    l2.type = "random_2_2"
    l2.color = "red!30"
    l2.fill = "black!30"
    
    l3.addpto = p1
    l3.addpto = p2    
    
    path = os.path.dirname(os.path.abspath(__file__))
    tik.save_pdf(path, "test")
    #tik.save_tikz_stanalone(path, "test")
    
    
if __name__ == "__main__":

    #test_points()
    #aux_points()
    #operators()
    lines()