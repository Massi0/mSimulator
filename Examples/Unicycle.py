#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 20:39:31 2020

@author: massimacbookpro
"""


from Examples import Agent,np

class Unicycle(Agent):
    #state = [x,y,z]
    def __init__(self,name,*args,**kwargs):
        super(Unicycle,self).__init__(name, dim=3, dim_u=2,*args,**kwargs)
        
    def dynamics(self,u,t):
        u = np.squeeze(u)
        x,y,th = np.squeeze(self.state)
        xd = u[0]*np.cos(th)
        yd = u[0]*np.sin(th)
        thd = u[1]

        return np.squeeze([xd,yd,thd])
    
    
    def get_destination(self):
        return self.controller.get_destination()