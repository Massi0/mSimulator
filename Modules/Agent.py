#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 20:32:03 2020

@author: massimacbookpro
"""


from Modules import np

class Agent:
    def __init__(self,name,dim=1,dim_u=0,controller=None,save_history=False,*args,**kwargs):
        self.name = name
        self.state = []
        self.controller = []
        self.dim = dim
        self.dim_u = dim_u
        self.t = 0
        self.save_history = save_history
        self.history = {"t":[],
                        "x":[]} 

        self.controller = controller

    def set_init(self,x_init,t0):
        self.update_state(x_init,t0)
        

    def dynamics(self,u,t,*vargs,**kwargs):
        pass

    def __call__(self,z=None,t=None,*args,**kwargs):

        if self.controller is None:
            u = z
        else:
            u = self.controller(x=z,
                                t=t,
                                ego_agent=self,*args,**kwargs)

        u = np.squeeze(u)
        if u.shape[0] != self.dim_u or len(u.shape)!=1:
            raise ValueError(u)


        return self.dynamics(u,t,*args,**kwargs)


    def update_state(self,x,t,save=True):
        x = np.squeeze(x)
        if x.shape[0] != self.dim or len(x.shape) != 1:
            raise ValueError(x)
        
        self.state = x
        self.t = t

        if self.save_history and save:
            self.history["t"].append(t)
            self.history["x"].append(x)

    def get_state(self):
        return self.state, self.t
