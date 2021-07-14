"""https://stackoverflow.com/a/47166787"""


import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from generate_figures import read_mat_data

font = {"family": "serif",
        "weight": "bold",
        "size": 20}

matplotlib.rc("font", **font)


len_runoff, noo, RII = read_mat_data()

names = [str(idx + 1) for idx in range(len(noo))]
noo_str = [str(idx) for idx in noo]
# print(names)
# import pdb; pdb.set_trace()

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
fig, ax = plt.subplots()
sc = plt.scatter(len_runoff,
                 RII,
                 s=23* noo,
                 c=noo,
                 cmap=cmap,
                 vmin=min(noo) - .5,
                 vmax=max(noo) + .5)
plt.gca().invert_yaxis()
fontsize = 27

ax.get_xaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda len_runoff, p: format(int(len_runoff), ',')))

ax.set_xlabel("LAI [m\u00b2]", fontsize=fontsize, fontweight='bold')
ax.set_ylabel("ARI [-]", fontsize=fontsize, fontweight='bold')
ax.tick_params(labelsize=fontsize)

cbar = plt.colorbar(sc, ticks=list(range(min(noo), max(noo) + 1)))
cbar.ax.tick_params(labelsize=fontsize)
cbar.ax.set_ylabel("Outlets", fontsize=fontsize, fontweight='bold')
# ax = plt. gca()
# ax. xaxis. label. set_size(20)
# ax. yaxis. label. set_size(20)

# annot = ax.annotate("",
#                     xy=(0, 0),
#                     xytext=(20, 20),
#                     textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# fig.canvas.mpl_connect("motion_notify_event", hover)
# plt.show()

# Bold a certain point.
points = [
     359,
     871,
     935,
     951,
    1023]

# points = [
#      935,
# ]

for point in points:
    ax.scatter(len_runoff[point-1], RII[point-1], s=175, c="r")
print(len_runoff[point-1], RII[point-1])

blue = [len_runoff[2-1], RII[2-1]]
text = "1"
ax.scatter(len_runoff[2-1], RII[2-1], s=175, c="blue")

from matplotlib.lines import Line2D
font = 20

legend_elements = [Line2D([0], [0], marker='o', color='blue', label='1',
                              markerfacecolor='blue', markersize=10),
                       Line2D([0], [0], marker='o', color='red', label='2,3,4,5,6',
                              markerfacecolor='red', markersize=10)]

ax.legend(handles=legend_elements, loc='upper left', fontsize=20)

plt.show()
# 103,
#      231,
#      359,
#      375,
#      487,
#      615,
#      631,
#      639,
#      679,
#      695,
#      703,
#      743,
#      759,
#      767,
#      871,
#      887,
#      935,
#      951,
#      959,
#      999,
#     1015,
#     1023