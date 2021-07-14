from generate_figures import read_mat_data
import matplotlib.pyplot as plt

len_runoff, noo, slope, RII = read_mat_data()

cmap = plt.get_cmap("viridis")
plott = plt.scatter(len_runoff, slope,
                    s=4 * noo,
                    c=noo,
                    cmap=cmap,
                    vmin=min(noo) - .5,
                    vmax=max(noo) + .5)
plt.gca().invert_yaxis()
plt.xlabel("Total Length Runoff")
plt.ylabel("Total Slope [-]")

plt.show()
