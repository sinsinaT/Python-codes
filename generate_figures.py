"""Create fancy plots for Cna."""

from typing import TYPE_CHECKING, Tuple

import matplotlib.pyplot as plt
from scipy.io import loadmat

if TYPE_CHECKING:
    from numpy import ndarray

# Set typeface for publication.
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]


def read_mat_data() -> Tuple["ndarray", "ndarray", "ndarray"]:
    """Read data for plots from Matlab files."""
    len_runoff = loadmat("./data/len_runoff.mat")["len_runoff"][0]
    noo = loadmat("./data/n_o_o.mat")["number_of_outfalls"][0]
    slope = loadmat("./data/slope.mat")["Reliability_index"][0]
    sr = loadmat("./data/SR.mat")["SR"][0]
    return len_runoff, noo, slope, sr


def plot_slope(xx: "ndarray", yy: "ndarray", scale: "ndarray") -> None:
    """Slope scatter plot from (xx,yy) data points."""
    # Define discrete color map for plot.
    cmap = plt.get_cmap("viridis", max(scale) - min(scale) + 1)

    fig = plt.scatter(
        xx,
        yy,
        s=1 * scale,  # scale manually
        c=scale,
        cmap=cmap,
        vmin=min(scale) - .5,
        vmax=max(scale) + .5)
    plt.gca().invert_yaxis()

    plt.xlabel("Total Length Runoff")
    plt.ylabel("Total Slope [-]")

    cbar = plt.colorbar(fig, ticks=list(range(min(scale), max(scale) + 1)))
    cbar.ax.set_ylabel("Outlets")

    plt.savefig("./eps/slope.eps", format="eps")
    plt.close()


def plot_noo(xx: "ndarray", yy: "ndarray") -> None:
    """Outlet candidates scatter plot from (xx,yy) data points."""
    # Define single color for plot.
    cmap = plt.get_cmap("viridis", 1)

    plt.scatter(xx, yy, c=len(yy) * [1.], cmap=cmap)

    plt.xlabel("Total Length Runoff")
    plt.ylabel("Outlet Candidates")

    plt.savefig("./eps/noo.eps", format="eps")
    plt.close()


def main():
    """Main plotting pipeline."""
    len_runoff, noo, slope, _ = read_mat_data()
    plot_slope(len_runoff, slope, noo)
    plot_noo(len_runoff, noo)


if __name__ == "__main__":
    main()
