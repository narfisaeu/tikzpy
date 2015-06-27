import math
import numbers
import obj_data
import copy
import cls_racime

def log(txt):
    
    print txt

class _groups(object):

    def __init__(self, parent):
    
        self.parent = parent
        
        ### Types
        self.racimes = cls_racime._racimes(self)
        