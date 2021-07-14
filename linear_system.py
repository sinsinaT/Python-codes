from pyswmm import Simulation, Nodes, Links
import numpy as np
from misc_light import swmm_input_read
from scipy.optimize import linprog

fill_lvl = .9
roughness = .013
v_max = 8.
inp_file = './test.inp'

node_id = []
pipe_id = []
sim = Simulation(inp_file)

for n in Nodes(sim):
    node_id.append(n.nodeid)

for l in Links(sim):
    pipe_id.append(l._linkid)

print('\n%i nodes with %i pipes total.' % (len(node_id), len(pipe_id)))
__import__('pdb').set_trace()

_, inp = swmm_input_read(open(inp_file, 'r'))

A = np.zeros((len(pipe_id), len(node_id)))
b = np.zeros((len(pipe_id), 1))

for p in pipe_id:
    radius = float([x[2] for x in inp['XSECTIONS'] if x[0] == p][0])/2
    n = Links(sim)[p].connections
    n0_coord = [x[1:] for x in inp['COORDINATES'] if x[0] == n[0]][0]
    n1_coord = [x[1:] for x in inp['COORDINATES'] if x[0] == n[1]][0]
    proj_len = ((float(n0_coord[0])-float(n1_coord[0]))**2
                + (float(n0_coord[1])-float(n1_coord[1]))**2)**(1/2)
    d_x = Nodes(sim)[n[0]].invert_elevation
    d_y = Nodes(sim)[n[1]].invert_elevation

    # Hydraulic radius, cf. https://is.gd/Za1UkY
    theta = 2*np.arccos(2*fill_lvl - 1)
    Area = np.pi*radius**2 - radius**2*(theta-np.sin(theta))/2
    P = 2*np.pi*radius - radius*theta
    R_h = Area/P

    C = R_h**(4/3)/roughness**2/proj_len
    print('Manning for pipe', n, 'is %.2f' % (R_h**(2/3) /
                                                       roughness*(d_x - d_y)**(1/2)/proj_len**(1/2)))

    A[pipe_id.index(p), node_id.index(n[0])] = 1.
    A[pipe_id.index(p), node_id.index(n[1])] = -1.
    b[pipe_id.index(p)] = v_max**2/C - (Nodes(sim)[n[0]].invert_elevation
                                        - Nodes(sim)[n[1]].invert_elevation)

res = linprog(np.ones(len(node_id)), A_ub=A, b_ub=b)
print('nodes:', node_id)
print('shift:', [round(x, 3) for x in res['x']])

for p in pipe_id:
    radius = float([x[2] for x in inp['XSECTIONS'] if x[0] == p][0])/2
    n = Links(sim)[p].connections
    n0_coord = [x[1:] for x in inp['COORDINATES'] if x[0] == n[0]][0]
    n1_coord = [x[1:] for x in inp['COORDINATES'] if x[0] == n[1]][0]
    proj_len = ((float(n0_coord[0])-float(n1_coord[0]))**2
                + (float(n0_coord[1])-float(n1_coord[1]))**2)**(1/2)
    d_x = Nodes(sim)[n[0]].invert_elevation + res['x'][node_id.index(n[0])]
    d_y = Nodes(sim)[n[1]].invert_elevation + res['x'][node_id.index(n[1])]

    # Hydraulic radius, cf. https://is.gd/Za1UkY
    theta = 2*np.arccos(2*fill_lvl - 1)
    Area = np.pi*radius**2 - radius**2*(theta-np.sin(theta))/2
    P = 2*np.pi*radius - radius*theta
    R_h = Area/P

    C = R_h**(4/3)/roughness**2/proj_len
    print('Manning after optimization', n, 'is %.2f' % (R_h**(2/3) /
                                                                 roughness*(d_x - d_y)**(1/2)/proj_len**(1/2)))
