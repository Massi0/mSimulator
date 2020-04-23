#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 19:21:39 2020

@author: massimacbookpro
"""

import numpy as np
from scipy.integrate import ode

from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib import colors as mcolors
from IPython.core.debugger import set_trace
import matplotlib.animation as manimation

import sys

import importlib
#from .Physics import Physics 
#
#from .World import World 


to_import = ["Physics", "World", "Controller", 
             "ControllerFactory", "Agent","AgentsFactory","Render"]

#to_import = ["Physics"]

thismodule = sys.modules[__name__]

for module in to_import:
#    set_trace()
    mod = importlib.import_module(".{}".format(module),"Modules")
    setattr(thismodule,module,getattr(mod,module))
    
#    importlib.__import__(module,fromlist=(".{}".format(module)))
    
   

#from .AgentsFactory import AgentsFactory
#
#from .ControllerFactory import ControllerFactory
#



