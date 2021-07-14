"""Compute node depth with min cover depth and min slopes constraints."""
import numpy as np
from pyswmm import Links, Nodes, Simulation
from scipy.optimize import linprog

from misc_light import swmm_input_read


def main(inp_file):
    min_slope = .003
    max_slope = .1
    min_cover = 1.5

    node_id = []
    pipe_id = []
    sim = Simulation(inp_file)

    for n in Nodes(sim):
        node_id.append(n.nodeid)

    for l in Links(sim):
        pipe_id.append(l._linkid)

    print('\n%i nodes with %i pipes total.' % (len(node_id), len(pipe_id)))

    _, inp = swmm_input_read(open(inp_file, 'r'))

    A = np.zeros((len(node_id)+2*len(pipe_id), len(node_id)))
    b = np.zeros(A.shape[0])

    # Minimum cover depth constraints.
    A[:len(node_id), :] -= np.eye(len(node_id))
    b[:len(node_id)] = -min_cover

    # Minimum/maximum pipe slope constraints.
    for p in pipe_id:
        n = Links(sim)[p].connections
        n0_coord = [x[1:] for x in inp['COORDINATES'] if x[0] == n[0]][0]
        n1_coord = [x[1:] for x in inp['COORDINATES'] if x[0] == n[1]][0]
        proj_len = ((float(n0_coord[0])-float(n1_coord[0]))**2
                    + (float(n0_coord[1])-float(n1_coord[1]))**2)**(1/2)
        # pipe_len = float(inp['CONDUITS'][pipe_id.index(p)][3])
        invert_elev0 = Nodes(sim)[n[0]].invert_elevation
        invert_elev1 = Nodes(sim)[n[1]].invert_elevation

        # Minimum slope.
        A[len(node_id)+pipe_id.index(p), node_id.index(n[0])] = 1
        A[len(node_id)+pipe_id.index(p), node_id.index(n[1])] = -1
        b[len(node_id)+pipe_id.index(p)] = -np.tan(min_slope) * \
            proj_len+invert_elev0-invert_elev1

        # Maximum slope.
        A[len(node_id)+len(pipe_id)+pipe_id.index(p), node_id.index(n[0])] = -1
        A[len(node_id)+len(pipe_id)+pipe_id.index(p), node_id.index(n[1])] = 1
        b[len(node_id)+len(pipe_id)+pipe_id.index(p)
          ] = np.tan(max_slope)*proj_len-invert_elev0+invert_elev1

    # Define minimum invert elevation as cost function.
    c = np.ones(len(node_id))
    return linprog(c=c, A_ub=A, b_ub=b), node_id, pipe_id


def compute_new_values(inp_file, res, node_id):
    sim = Simulation(inp_file)
    _, inp = swmm_input_read(open(inp_file, 'r'))
    # New inverted elevation.
    inv_elev = []
    for id_, n in enumerate(node_id):
        inv_elev.append([n, Nodes(sim)[n].invert_elevation-res['x'][id_]])

    # New pipe length.
    pipe_len_swmm = []
    for p in pipe_id:
        n = Links(sim)[p].connections
        n0_coord = [x[1:] for x in inp['COORDINATES'] if x[0] == n[0]][0]
        n1_coord = [x[1:] for x in inp['COORDINATES'] if x[0] == n[1]][0]
        proj_len = ((float(n0_coord[0])-float(n1_coord[0]))**2
                    + (float(n0_coord[1])-float(n1_coord[1]))**2)**(1/2)
        pipe_len_swmm.append([p, proj_len])
    return inv_elev, pipe_len_swmm


if __name__ == "__main__":
    inp_file = './inp/Got1.inp'
    res, node_id, pipe_id = main(inp_file)
    print(res)
    inv_elev, pipe_len_swmm = compute_new_values(
        inp_file, res, node_id)
    # Write results to file.
    with open('./results/res.csv', 'w') as f:
        for id_, r in enumerate(res['x']):
            f.write('{:s},{:f}\n'.format(node_id[id_], r))
    with open('./results/inv_elev.csv', 'w') as f:
        for l in inv_elev:
            f.write(','.join([str(x) for x in l])+'\n')
    with open('./results/pipe_len_swmm.csv', 'w') as f:
        for l in pipe_len_swmm:
            f.write(','.join([str(x) for x in l])+'\n')
    # compute_slopes(inp_file, res, node_id, pipe_id)
    # for id_ in range(len(node_id)):
    #     print('{:s} {:.2f}'.format(node_id[id_], res['x'][id_]))
