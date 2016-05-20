#!/usr/bin/python
import os, sys
import numpy as np

pparent = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
pparent = os.path.abspath(pparent)
sys.path.append(pparent) #parent

import header_main
  