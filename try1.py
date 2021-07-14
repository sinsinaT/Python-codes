# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 15:00:00 2021

@author: c8451316
"""

#from pyswmm import Simulation, Nodes
#with Simulation('01.inp') as sim:
    #for node in Nodes(sim):
      #print (node.depth)
      
#from pyswmm import Simulation
#with Simulation ('01.inp')as sim:
    #print (sim.flow_units)
      
from pyswmm import Simulation, Nodes
with Simulation('02.inp') as sim:
    print (sim.start_time)
    sim.step_advance(300)
    for node in Nodes(sim):
        print (node.nodeid)
    for step in sim:
        for node in Nodes(sim):
          print (node.flooding)

from pyswmm import Simulation, RainGages
with Simulation ('01.inp')as sim:
    sim.step_advance (3600)
    for step in sim :
        for raingage in RainGages(sim):
            print (raingage.total_precip)
          #sim.report()
     
     

#from pyswmm import Simulation, Nodes
#with Simulation ('test.inp') as sim:
    #for node in Nodes(sim):
        #print (node.nodeid)
 