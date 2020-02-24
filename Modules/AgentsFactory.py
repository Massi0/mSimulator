#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 20:32:45 2020

@author: massimacbookpro
"""

class AgentsFactory:
    def __init__(self):
        self._agentsManagers = {}

    def register_manager(self, key, manager):
        self._agentsManagers[key] = manager

    def create (self, mKey, *args,**kwargs):
        manager = self._agentsManagers.get(mKey)
        if not manager:
            raise ValueError(mkey)

        return manager.get_agent(*args,**kwargs)

    def __call__(self, mKey, *args,**kwargs):
        return self.create(mKey, *args,**kwargs)

