#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 19:52:13 2020

@author: massimacbookpro
"""


from Modules import  np, ode, Physics




class World(Physics):
    def __init__(self,keep_global_state=False,*args,**kwargs):
        # self.n_dim = n_dim;
        # self.states = []
        # self.sampling_time = dt
        # self.times = []
        # self.max_state_history = max_state_history
        # self.solver = None
        self.keep_global_state = keep_global_state
        self.agents = {}
        self.initialized = False
        super(World,self).__init__(n_dim=0, dt=1e-2, max_state_history=1e4)


    def get_agent(self, name, AgentClass, x_init,*args,**kwargs):
        if not self.initialized:
            raise Exception("{} need to be initialized first".format(type(self).__name__))

        if self.agents.get(name) is not None:
            return self.agents.get(name)
        

        agent = AgentClass(name=name,*args,**kwargs)

        x_init = np.squeeze(x_init)
        if (x_init.shape[0] != agent.dim):
            raise ValueError(x_init)

            
        agent.set_init(x_init,self.times[-1])
        
        if self.keep_global_state :
            if len(self.states)>0:
                x = list(np.squeeze(self.states[-1]))
                x.extend(x_init)
                self.states[-1] = np.squeeze(x)
            else:
                self.states.append(x_init)

        self.agents[name] = agent
        self.n_dim = sum([self.agents[key].dim for key in self.agents]) #np.squeeze(self.states[-1]).shape[0] 

        return agent

    def _serialize_states(self):
        state = []
        for _,agent in self.agents.items():
            x,_ = agent.get_state()
            x = list(x)
            state.extend(x)
        
        return np.array(state)   

    def get_all_agents(self):
        return self.agents 

    def update_state_for_all_agents(self,state,t,save=True):
        state = np.squeeze(state)
        for agent,x in zip(self.agents,np.split(state,len(self.agents))):
                self.agents[agent].update_state(x,t,save=save)

        
    def phy_equation(self,t,x):
        f_x= []
        self.update_state_for_all_agents(x,t,save=False)
        for _,agent in self.agents.items():
            dx = agent(z=x,t=t)
            f_x.extend(np.squeeze(dx))
        
        return f_x


    def initialize(self, init_time=0, ode_solver="lsoda", ode_dt=1e-2, max_state_history=1e4):
        if not self.initialized:
            self.times.append(init_time)
            self.sampling_time = ode_dt
            self.max_state_history = max_state_history
            f = self.phy_equation
            self.solver = ode(f).set_integrator(ode_solver, with_jacobian=False)
            # self.solver.set_initial_value(init_state, init_time)
            self.initialized = True

        return self.initialized



    def solve_ode_forward(self,t):


        init_state = self._serialize_states()
        time = init_time = self.times[-1]

        self.solver.set_initial_value(init_state, init_time)
        while (time+self.sampling_time<=t):
            self.solver.integrate(time+self.sampling_time)
            if not self.solver.successful():
                raise Exception("Solver failed at t={}".format(time))
            
            # set_trace()
            time, state = self.solver.t, self.solver.y


        time, state = self.solver.t, self.solver.y
        self.update_state_for_all_agents(state,time,save=True)

        self.times.append(time)

        return time


    def play(self,t,num_of_snapshot):
        if t<self.times[-1]: 
            raise Exception("{} is smaller than the current time".format(t))

        dt = (t-self.times[-1])/num_of_snapshot

        if dt < self.sampling_time:
            raise Exception("Number of snapshots should be larger than {}".format((t-self.times[-1])/self.sampling_time))


        while self.times[-1]<t:
            self.solve_ode_forward(self.times[-1]+dt)

    def __call__(self,t,num_of_snapshot):
        return self.play(t,num_of_snapshot)

