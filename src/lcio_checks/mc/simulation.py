import awkward as ak
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..util import load_or_make

is_vars = [
    "isCreatedInSimulation",
    "isBackscatter",
    "vertexIsNotEndpointOfParent",
    "isDecayedInTracker",
    "isDecayedInCalorimeter",
    "hasLeftDetector",
    "isStopped",
    "isOverlay",
]


def add_simulation_info(mc):
    rebased = (mc.mcsst + 2**32) // 2**23 - 256
    mc["isCreatedInSimulation"] = rebased // 128 % 2 == 1
    mc["isBackscatter"] = rebased // 64 % 2 == 1
    mc["vertexIsNotEndpointOfParent"] = rebased // 32 % 2 == 1
    mc["isDecayedInTracker"] = rebased // 16 % 2 == 1
    mc["isDecayedInCalorimeter"] = rebased // 8 % 2 == 1
    mc["hasLeftDetector"] = rebased // 4 % 2 == 1
    mc["isStopped"] = rebased // 2 % 2 == 1
    mc["isOverlay"] = rebased // 1 % 2 == 1
    return mc


@load_or_make(["simulation_status_is", "simulation_status_counts.csv"])
def plot_simulation_info(mc):
    if not hasattr(mc, is_vars[0]):
        mc = add_simulation_info(mc)
    fig, axs = plt.subplots(figsize=(12, 6), nrows=2, ncols=4, sharex=True, sharey=True)
    bins = np.arange(6) - 0.5
    is_counts = {}
    for is_var, ax in zip(is_vars, axs.flatten()):
        try:
            ax.bar((bins[1:] + bins[:-1]) / 2, is_counts["isAny"], width=1)
        except KeyError:
            is_counts["isAny"] = ax.hist(ak.flatten(mc.mcgst), bins=bins)[0]
        is_counts[is_var] = ax.hist(
            ak.flatten(mc[getattr(mc, is_var)].mcgst),
            bins=bins,
            label="True",
            color="C1",
        )[0]
        ax.text(
            1,
            1.01,
            is_var,
            horizontalalignment="right",
            verticalalignment="bottom",
            transform=ax.transAxes,
        )
    axs[0][0].legend()
    fig.text(0.5, 0.04, "generatorStatus", ha="center")
    df = pd.DataFrame(is_counts).astype(int)
    df.index.name = "generatorStatus"
    return fig, df
