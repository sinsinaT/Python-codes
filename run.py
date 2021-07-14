"""Run benchmarks with SWMM on various network configurations."""

import os
from glob import glob
from subprocess import call

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import swmmio
from joblib import Parallel, delayed
from pyswmm import Simulation


def force_symlink(rain: int) -> None:
    """Create symlink to rainfall data."""
    slink = "rain.dat"
    if os.path.isfile(slink):
        call(["rm", slink])
    call(["ln", "-s", f"RP_{rain}.dat", slink])


def fix_rain_path(inp: str) -> None:
    """Replace Windows relative path with correct file path."""
    call([
        "sed", "-i", "-e",
        "s/Raingage VOLUME 0:05 1.0 FILE .* 1 MM/Raingage VOLUME 0:05 1.0 FILE rain.dat 1 MM/g",
        f"{inp}"
    ])


def run_swmm_from(inp: str) -> None:
    """Run SWMM simulation for single .inp file."""
    fix_rain_path(inp)
    sim = Simulation(inp)
    sim.execute()


def get_value_from(rpt: str) -> float:
    """Return percentage of nodes not flooded."""
    sc_runoff = swmmio.utils.dataframes.dataframe_from_rpt(
        rpt, "Subcatchment Runoff Summary")
    node_flood = swmmio.utils.dataframes.dataframe_from_rpt(
        rpt, "Node Flooding Summary")
    return 100 * (1 - node_flood["TotalFloodVol"].sum() /
                  sc_runoff["TotalRunoffMG"].sum())


def main() -> None:
    """Main calculation loop."""
    # for city in ["1.Gotzens", "2.Innsbruck", "3.South_innsbruck"]:
    for city in ["3.South_innsbruck"]:
        df = pd.DataFrame(columns=["rain", "structure", "direction of added loops", "number of loops", "HPI (%)"])
        bench_result = pd.DataFrame(columns=["rain", "structure", "HPI (%)"])
        # for rain in [2, 5, 20]:
        for rain in [10]:
            for type_ in ["centralized", "decentralized"]:
                # Compute percentage for benchmark network.
                bench_inp = f"./{city}/{type_}/benchmark.inp"

                run_swmm_from(bench_inp)  # benchmark network
                bench_result.loc[len(bench_result)] = [
                rain, type_,
                get_value_from(bench_inp[:-3] + "rpt")
                ]

                for direction in ["upstream", "downstream"]:
                    # Symbolic link to rainfall data.
                    force_symlink(rain)
                    # List of all .inp files in current working directory.
                    # import pdb;pdb.set_trace()
                    files = sorted(glob(f"./{city}/{type_}/{direction}/*.inp"))

                    if not files:
                        break

                    # Run SWMM in parallel.
                    Parallel(n_jobs=6)(delayed(run_swmm_from)(inp)
                                       for inp in files)
                    for inp in files:
                        net_id = int(os.path.basename(inp)[:-4])
                        df.loc[len(df)] = [
                            rain, type_, direction, net_id,
                            get_value_from(inp[:-3] + "rpt")
                        ]

            # Plot results.
            fig, ax = plt.subplots()
            plt.title(f"{city[2:]} Rain {rain}")
            # sns.set_theme();sns.set_style("ticks");sns.set_context("talk");sns.set_color_codes("dark")
            sns.set_style("darkgrid")
            sns.violinplot(x="structure",
                           y="HPI (%)",
                           hue="direction of added loops",
                           data=df,
                           split=True, palette=["g", "red"], scale="count",inner="quartile")
            sns.swarmplot(x="structure",
            y="HPI (%)",
            hue="direction of added loops",
            data=df,
            palette="Set2",
            size=4)
            sns.swarmplot(x="structure",
                        y="HPI (%)",
                        data=bench_result,
                        size=6,
                        color="blue")
            plt.legend(loc='lower right')

            plt.savefig(f"./png/{city[2:]}_rain{rain}.png", dpi=1200)
            plt.close()

            # Annotation of flood percentages.
            sns.relplot(x="number of loops",
                        y="HPI (%)",
                        col="rain",
                        hue="direction of added loops",
                        style="structure",
                        data=df, palette=["g", "red"], size="HPI (%)").set(title='')

            plt.savefig(f"./png/{city[2:]}_rain{rain}_percentage.png",dpi=1200)
            plt.close()


if __name__ == "__main__":
    main()
