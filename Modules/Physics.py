#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 19:20:55 2020

@author: massimacbookpro
"""

from Modules import ode,np 

class Physics():
    def __init__(self, n_dim=1, dt=1e-2, max_state_history=1e4):
        self.n_dim = n_dim;
        self.states = []
        self.sampling_time = dt
        self.times = []
        self.max_state_history = max_state_history
        self.solver = None


    def phy_equation(self,t,x):
        pass


    def append_state(self,t,x):
        if len(self.states)>self.max_state_history or len(self.times)>self.max_state_history:
            raise Exception("Size of states history exeed {}".format(self.max_state_history))

        self.times.append(t)
        self.states.append(x)

    def init_world(self,init_state,init_time, ode_solver="lsoda"):
        self.append_state(init_time, init_state)
        f = self.phy_equation
        self.solver = ode(f).set_integrator(ode_solver, with_jacobian=False)
        self.solver.set_initial_value(init_state, init_time)


    def solve_forward(self,t):

        while (self.times[-1]+self.sampling_time<=t):
            self.solver.integrate(self.times[-1]+self.sampling_time)
            if not self.solver.successful():
                raise Exception("Solver failed at t={}".format(self.times[-1]))
            self.append_state(self.solver.t,self.solver.y)
        
        return self.times,self.states

    
    def get_states(self):
        return  np.array(self.times), np.array(self.states)
