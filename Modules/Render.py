#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 20:35:19 2020

@author: massimacbookpro
"""

from Modules import Line2D,plt,mcolors,np

class Render:
    def __init__(self,world):
        self._world = world
        self.obj_colors = {}
        self.obj_markers = {}

    def get_agents(self):
        return self._world.get_all_agents()
    
    def get_color(self,obj):
        color = self.obj_colors.get(obj)
        # color_list = list(mcolors.CSS4_COLORS.values())
        colors_list = ["k","b","y","g","m"]
        random_color = np.random.choice(colors_list)

        if color is None:
            while random_color in self.obj_colors.values():
                random_color = np.random.choice(colors_list)
            self.obj_colors[obj] = random_color

        return self.obj_colors[obj]
        

    def get_marker(self,obj):
        marker = self.obj_markers.get(obj)
        # markers_list = list(Line2D.markers.keys())
        markers_list = ["*","+","v","1","2","3","4","s","h"]
        rand_marker = np.random.choice(markers_list)
        if marker is None :
            while rand_marker in self.obj_markers.values():
                rand_marker = np.random.choice(markers_list)
            self.obj_markers[obj] = rand_marker

        return self.obj_markers[obj]


    def plot_agent(self,agent,ax,color='b',marker='+', marker_size=30):
        states = agent.history["x"]
        x = np.array(states)
        ax.plot(x[:,0],x[:,1],
                color=color,
                linestyle='dashed')
        p = .2
        steps = int(np.shape(x)[1]*p)
        steps = steps if steps>0 else 1
        ax.scatter(x[0,0],x[0,1],
                   c=color,
                   marker='o',
                   s=marker_size)
        
        ax.scatter(x[-1,0],x[-1,1],
                   c=color,
                   marker=marker,
                   s=marker_size)

    
    def plot(self,**kwargs):
        fig, ax = plt.subplots()
        for _,agent in self.get_agents().items():
            marker = self.get_marker(agent)
            marker = "P"
            color = self.get_color(agent)
            self.plot_agent(agent,ax,color=color,marker=marker,marker_size=100)
        for key,val in kwargs.items():
            if hasattr(ax,key):
                attr = getattr(ax,key)
                if callable(attr):
                    attr(val)

        return fig,ax