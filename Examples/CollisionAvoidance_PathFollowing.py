#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 20:40:21 2020

@author: massimacbookpro
"""

from Examples import Controller, np


class CollisionAvoidance_PathFollowing(Controller):
    def __init__(self,world, distination,detection_radius=1,r=.3,activate_CA=True):
        self.x_f = np.squeeze(distination)
        self.world = world
        self.detection_radius = detection_radius
        self.r = r
        self.activate_CA = activate_CA
    def get_all_agents(self):
        agents = self.world.get_all_agents()
        if len(agents) == 0:
            return None
        return agents

    def compute_u(self,_,t,ego_agent):
        u_collisios = 0
        norm = lambda x: np.linalg.norm(x,ord=2)
        x, _ = ego_agent.get_state()
        theta = x[-1]
        x = x[:-1]
        R = self.detection_radius
        r = self.r
        u_collision = 0
        if self.activate_CA:
            for _, agent in self.get_all_agents().items():
                if agent == ego_agent:
                    continue

                y,_ = agent.get_state()
                y = y[:-1]
                d_xy = norm(x-y)
                u_collision += 0 if d_xy>R else -(y-x)/(d_xy-r)**2
        
        ss = self.x_f
        u_target = (self.x_f - x)

        u = .4*u_collision+ .6*u_target

        return norm(u),-5*(theta-np.arctan2(u[1],u[0]))



