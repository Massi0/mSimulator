#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 20:34:29 2020

@author: massimacbookpro
"""

class Controller:
    def __init__(self,world=None):
        self.world = None

    def compute_u(self,x,t):
        pass

    def __call__(self,x,t,*args,**kwargs):
        return self.compute_u(x,t,*args,**kwargs)