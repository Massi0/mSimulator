#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 19:24:04 2020

@author: massimacbookpro
"""

from Modules import *
from Examples import *

if __name__ == "__main__":
    print("Running .... ")
    

    
    world = World()

    agents_generator = AgentsFactory()
    controllers_handler = ControllerFactory(world=world)
    
    
    agents_generator.register_manager("unicycle_Collision_Avoidance",world)
    
    controllers_handler.register_controller(name = "CollisionAvoidance",
                                            controller=CollisionAvoidance_PathFollowing)
    
    
    
    
    
    
    world.initialize(init_time=0,
                     ode_solver='lsoda',
                     ode_dt=1e-2)
    
     
    
    Collision_Activated = True
    CA_controller_1 = controllers_handler.get_controller(name = "CollisionAvoidance",
                                                         distination = [5,5],
                                                         detection_radius=4,
                                                         r=.1,
                                                         activate_CA=Collision_Activated)
    
    CA_controller_2 = controllers_handler.get_controller(name = "CollisionAvoidance",
                                                         distination = [5,0],
                                                         detection_radius=4,
                                                         r=.1,
                                                         activate_CA=Collision_Activated)
    
    
    agent_1 = agents_generator("unicycle_Collision_Avoidance",
                                name="A1", 
                                AgentClass=Unicycle, 
                                x_init=[0,0,0],
                                save_history = True,
                                controller=CA_controller_1)
    
    agent_2 = agents_generator("unicycle_Collision_Avoidance",
                                name="A2", 
                                AgentClass=Unicycle, 
                                x_init=[0,2,0],
                                save_history=True,
                                controller=CA_controller_2)
    
    
    
    
    world(40,100)
    
    render = Render(world=world)
    kwargs = {"axis":"equal",
              "grid":None}
    # kwargs = {}
    fig,ax = render.plot(**kwargs)

