#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 20:33:47 2020

@author: massimacbookpro
"""

class ControllerFactory:
    def __init__(self,world):
        self._controllers = {}
        self._world = world

    def register_controller(self, name, controller, *args,**kwargs):
        self._controllers[name] = controller

    def get_controller(self,name,*args,**kwargs): 
        controller = self._controllers.get(name)
        if not controller:
            raise ValueError(name)

        return controller(world=self._world, *args,**kwargs)