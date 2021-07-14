"""https://stackoverflow.com/a/47166787"""

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from generate_figures import read_mat_data

font = {"family": "serif",
        # "weight": "bold",
        "size": 20}

matplotlib.rc("font", **font)

len_runoff, noo, RII, slope = read_mat_data()
print(RII)

names = [str(idx + 1) for idx in range(len(slope))]
noo_str = [str(idx) for idx in noo]

n_dims = 2


def update_annot(ind):
    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "idx: {}, noo: {}".format(
        " ".join([names[n] for n in ind["ind"]]),
        " ".join([noo_str[n] for n in ind["ind"]]))
    annot.set_text(text)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()


cmap = plt.get_cmap("viridis", max(noo) - min(noo) + 1)
plt.style.use('seaborn')

if n_dims == 2:

    fig, ax = plt.subplots()
    sc = plt.scatter(slope,
                     RII,
                     s=23 * noo,
                     c=noo,
                     cmap=cmap,
                     vmin=min(noo) - .5,
                     vmax=max(noo) + .5)
    fontsize = 27

    plt.gca().invert_yaxis()
    plt.xlabel("NSI [-]", fontsize=fontsize, fontweight='bold')
    plt.ylabel("ARI [-]", fontsize=fontsize, fontweight='bold')
    plt.xticks(fontsize=fontsize, fontweight='bold')
    plt.yticks(fontsize=fontsize, fontweight='bold')

    cbar = plt.colorbar(sc, ticks=list(range(min(noo), max(noo) + 1)))
    cbar.ax.tick_params(labelsize=fontsize)
    cbar.ax.set_ylabel("Outlet Candidates", fontsize=fontsize, fontweight='bold')

    annot = ax.annotate("",
                        xy=(0, 0),
                        xytext=(20, 20),
                        textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    fig.canvas.mpl_connect("motion_notify_event", hover)
    points = [1484,
              1519,
              1528,
              1535,
              2015,
              2047]
    for idx, point in enumerate(points):
        red = [slope[point - 1], RII[point - 1]]
        ax.scatter(red[0], red[1], s=230, c="r")
        ax.text(red[0]+0.1, red[1]+0.1, s=f"{idx+2}", size=20, zorder=1, color='k')

    blue = [slope[2 - 1], RII[2 - 1]]
    text = "1"
    ax.scatter(blue[0], blue[1], s=230, c="blue")

    from matplotlib.lines import Line2D

    font = 20

    legend_elements = [Line2D([0], [0], marker='o', color='blue', label='1',
                              markerfacecolor='blue', markersize=10),
                       Line2D([0], [0], marker='o', color='red', label='2,3,4,5,6,7',
                              markerfacecolor='red', markersize=10)]

    # Create the figure
    ax.legend(handles=legend_elements, loc='upper right', fontsize=20)

    plt.show()


else:  # three-dimensional plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(len_runoff,
                    slope,
                    RII,
                    s=15. * noo,
                    c=noo,
                    cmap=cmap,
                    vmin=min(noo) - .5,
                    vmax=max(noo) + .5)

    plt.style.use('seaborn')
    ax.set_xlabel("LAI [m\u00b2]", labelpad=27)
    ax.set_ylabel("ARI [-]", labelpad=27)
    ax.set_zlabel("NSI [-]", labelpad=27)

    cbar = plt.colorbar(sc, ticks=list(range(min(noo), max(noo) + 1)))
    cbar.ax.tick_params(labelsize=22)
    cbar.ax.set_ylabel("Outlet Candidates", fontsize=22, fontweight='bold')

    # Bold a certain point.
    points = [1484,
        1519,
        1528,
        1535,
        2015,
        2047]
    for idx, point in enumerate(points):
        red = [len_runoff[point-1], slope[point-1], RII[point-1]]
        ax.scatter(red[0], red[1], red[2], s=350, c="r")
        ax.text(red[0], red[1], red[2], s=f"{idx+2}", size=20, zorder=1, color='k')

    blue = [len_runoff[2-1], slope[2-1], RII[2-1]]
    text = "1"
    ax.scatter(blue[0], blue[1], blue[2], s=130, c="blue")
    # ax.text(blue[0], blue[1], blue[2], s=text, size=30, zorder=1, color='k')
    # for spine in ax.spines.values():
    #     spine.set_visible(False)
    #
    # plt.tight_layout()
    from matplotlib.lines import Line2D
    font = 20

    legend_elements = [Line2D([0], [0], marker='o', color='blue', label='1',
                              markerfacecolor='blue', markersize=10),
                       Line2D([0], [0], marker='o', color='red', label='2,3,4,5,6,7',
                              markerfacecolor='red', markersize=10)]

    # Create the figure
    ax.legend(handles=legend_elements, loc='upper right', fontsize=20)

    plt.show()

