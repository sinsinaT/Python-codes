"""Create fancy plots for Cna."""

import numpy as np; np.random.seed(0)
import seaborn as sns; sns.set_theme()
import matplotlib.pyplot as plt
from scipy.io import loadmat

# uniform_data = np.random.rand(10, 12)
# ax = sns.heatmap(uniform_data)
# print(uniform_data)

sns.set()
HPI = loadmat("./reilience_part2/HPI.mat")["HPI"]
x_axis_labels = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15] # labels for x-axis

HPI_transpose = HPI.transpose()
ax = sns.heatmap(HPI_transpose, cmap="YlGnBu",cbar_kws={'label': 'HPI'},xticklabels=x_axis_labels)
ax.invert_yaxis()
plt.title("HPI under design storm event when subjected to structural failure (blockages) of pipes", fontsize =10)
plt.xlabel("largest pipes blocked at downstream one by one in order ")
plt.ylabel("number of loops at downstream")
plt.savefig(f"./png/percentage.png", dpi=1200)

# def read_mat_data() -> Tuple["ndarray"]:
#     """Read data for plots from Matlab files."""
#     HPI = loadmat("./reilience_part2/HPI.mat")["HPI"][0]
#     return HPI


# HPI = loadmat("./reilience_part2/HPI.mat")["HPI"]
# print(HPI.size)



#
# def main():
#     HPI = read_mat_data()
#     sns.heatmap(HPI)
#
# if __name__ == "__main__":
#     main()
