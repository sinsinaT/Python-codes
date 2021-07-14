"""https://stackoverflow.com/a/47166787"""

import matplotlib.pyplot as plt
import numpy as np

from generate_figures import read_mat_data

len_runoff, noo, slope, sr = read_mat_data()
with open("./data.tsv", "w") as record_file:
    for idx in range(len(slope)):
        record_file.write(f"{len_runoff[idx]}\t{slope[idx]}\t{sr[idx]}\n")

names = [str(idx + 1) for idx in range(len(slope))]
noo_str = [str(idx) for idx in noo]

n_dims = 3


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

if n_dims == 2:
    fig, ax = plt.subplots()
    sc = plt.scatter(len_runoff,
                     slope,
                     s=4 * noo,
                     c=noo,
                     cmap=cmap,
                     vmin=min(noo) - .5,
                     vmax=max(noo) + .5)
    plt.gca().invert_yaxis()
    plt.xlabel("Total Length Runoff")
    plt.ylabel("Total Slope [-]")

    cbar = plt.colorbar(sc, ticks=list(range(min(noo), max(noo) + 1)))
    cbar.ax.set_ylabel("Outlets")

    annot = ax.annotate("",
                        xy=(0, 0),
                        xytext=(20, 20),
                        textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    fig.canvas.mpl_connect("motion_notify_event", hover)
    plt.show()

else:  # three-dimensional plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(len_runoff,
                    slope,
                    sr,
                    s=4. * noo,
                    c=noo,
                    cmap=cmap,
                    vmin=min(noo) - .5,
                    vmax=max(noo) + .5)

    ax.set_xlabel("Total Length Runoff")
    ax.set_ylabel("Total Slope [-]")
    ax.set_zlabel("SR")

    cbar = plt.colorbar(sc, ticks=list(range(min(noo), max(noo) + 1)))
    cbar.ax.set_ylabel("Outlets")

    # Bold a certain point.
    points = [103,
         231,
         359,
         375,
         487,
         615,
         631,
         639,
         679,
         695,
         703,
         743,
         759,
         767,
         871,
         887,
         895,
         935,
         951,
         959,
         999,
        1015,
        1023]
    for point in points:
        ax.scatter(len_runoff[point-1], slope[point-1], sr[point-1], s=180, c="r")

    plt.show()
