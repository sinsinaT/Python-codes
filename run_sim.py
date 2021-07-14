from pyswmm import Simulation, Links

inp_file = './test.inp'

sim = Simulation(inp_file)

for _ in sim:
    pass

for p in Links(sim):
    print('\n', p.connections, p.conduit_statistics['peak_velocity'])
