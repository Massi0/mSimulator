#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 04:39:27 2020

@author: massimacbookpro
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 20:40:21 2020

@author: massimacbookpro
"""

from Examples import Controller, np


class ECC_CollisionAvoidance_PathFollowing(Controller):
    def __init__(self,world, distination,gain_CA,detection_radius=1,r=.3,activate_CA=True,max_velocity=-1):
        self.x_f = np.squeeze(distination)
        self.world = world
        self.detection_radius = detection_radius
        self.r = r
        self.activate_CA = activate_CA
        self.looms = {} #Keep a loom history of each obstable within our sight
        self.rhos = {}
        self.gamma = r/detection_radius+.01
        self.norm = lambda x: np.linalg.norm(x,ord=2)
        self.t_old = -1
        self.gain_CA = gain_CA
        self.prev_u = None
        self.max_velocity = max_velocity
        
        
    def get_destination(self):
        return self.x_f
    
    def get_all_agents(self):
        agents = self.world.get_all_agents()
        if len(agents) == 0:
            return None
        return agents

    def compute_u(self,_,t,ego_agent):
        if (t-self.t_old) >1e-9:
            self.t_old = t
        else:
            self.t_old = t
            return self.prev_u
        
        u_collisios = 0
        norm = lambda x: np.linalg.norm(x,ord=2)
        x, _ = ego_agent.get_state()
        theta = x[-1]
        x = x[:-1]
        R = self.detection_radius
        r = self.r
        
        u_collision = 0
        
        if self.activate_CA:
            u_collision = self.collisionAvoidance_u(t,ego_agent)
        
        ss = self.x_f
        u_target = (self.x_f - x)

        u = 0.5*u_collision+ .5*u_target

        u_theta = (theta-np.arctan2(u[1],u[0]))
        v = norm(u) if norm(u)<self.max_velocity else self.max_velocity
        
        self.prev_u = (v,-5*u_theta)
        
        return v,-5*u_theta
    
    
    
    def is_sight(self,x_ego,x_obs):
        """
            emulate a detection sensor behavior
            retrun True if the obstacle is within the sight of the ego
        """
        return self.norm(x_ego-x_obs)<=self.detection_radius
    
    def get_loom(self,x_ego,x_obs,t,rhos):
        """
            emulate a Time-to-collision sensor behavior
            retrun the loom = 1/TTC
        """
        if len(rhos)<2:
            rhos.append((t,self.norm(x_obs-x_ego)))
            return 0
        
        
        drho = (rhos[-1][1]-rhos[-2][1])/(rhos[-1][0]-rhos[-2][0])
        rhos.append((t,self.norm(x_obs-x_ego)))
        
        return drho/rhos[-1]
        
    
    def collisionAvoidance_u(self,t,ego):
        x, _ = ego.get_state()
        theta = x[-1]
        x_ego = x[:-1]
        R = self.detection_radius
        r = self.r
        u_collision_2D= np.array([0.,0.])
        
        agents_in_sight = list(self.get_all_agents().items())
        for _, agent in self.get_all_agents().items():
            
            if agent == ego:
                continue

            
            x_obs,_ = agent.get_state()
            x_obs = x_obs[:-1]
            
            if not self.is_sight(x_ego,x_obs):
                if agent in agents_in_sight:
                    agents_in_sight.remove(agent)
                    self.looms.remove(agent)
                    self.rhos.remove(agent)
                    
                continue
                
            if self.looms.get(agent) is None:
                self.looms[agent] = []
                
            if self.rhos.get(agent) is None:
                self.rhos[agent] = []
            
            
            
            loom = self.get_loom(x_ego,x_obs,t,self.rhos[agent])
                
            
            if self.looms.get(agent) is None:
                self.looms[agent] = []
                
            self.looms[agent].append((t,loom))
            
            
            zeta = sum([l*(t1-t0) for (t0,_),(t1,l) in zip(self.looms[agent][:-1],self.looms[agent][1:])])#estimate the intergral
            
            zeta = np.exp(zeta)
            D = zeta/(zeta**2-self.gamma**2)
            
            xy = x_obs-x_ego
            xy /= self.norm(xy)
#             los_angle = np.arctan2(xy[1],u[0])
            
            u_collision_2D += -self.gain_CA*D*xy
        
        
#         u = u_collision_2D
        return u_collision_2D
        
        
        
        
        
        
        



