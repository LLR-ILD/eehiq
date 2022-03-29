import awkward as ak
import matplotlib.pyplot as plt
import numpy as np

from ..util import load_or_make


@load_or_make(["count_mc_per_generator_status"])
def count_mc_per_generator_status(mc):
    fig, [ax1, ax2] = plt.subplots(ncols=2, figsize=(8, 4), sharey=True)
    bins1 = np.arange(0, ak.max(ak.num(mc.mcgst, axis=1)), 5) - 0.5
    bins2 = np.arange(0, 50, 1) - 0.5
    txt_kw = dict(ha="left", va="bottom")
    ax1.text(0.01, 0.005, "bin size: 5", transform=ax1.transAxes, **txt_kw)
    ax2.text(0.01, 0.005, "bin size: 1", transform=ax2.transAxes, **txt_kw)
    txt_kw["ha"] = "center"
    fig.text(0.5, 0.03, "#MC particles per generatorStatus per event", **txt_kw)
    for i, gen_status in enumerate(range(5)):
        kw = dict(color=f"C{i}", alpha=0.5)
        x = ak.num(mc[mc.mcgst == gen_status].mcgst)
        ax1.hist(x, bins=bins1, label=f"{gen_status}: {ak.sum(x):> 9}", **kw)
        ax2.hist(x, bins=bins2, **kw)
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax2.set_yscale("log")
    ax1.legend(title="generatorStatus")
    return (fig,)


@load_or_make(["vertex_in_z_per_generator_status"])
def vertex_in_z_per_generator_status(mc):
    var = "mcvtz"
    vals = getattr(mc, var)
    bins1 = np.arange(0, ak.max(np.abs(vals)), 100)
    bins2 = np.linspace(-1, 1, 100)
    fig, [ax1, ax2] = plt.subplots(ncols=2, figsize=(8, 4))
    for i, gen_status in enumerate(range(5)):
        kw = dict(color=f"C{i}", alpha=0.5)
        x = ak.flatten(vals[mc.mcgst == gen_status])
        ax1.hist(np.abs(x), bins=bins1, label=f"{gen_status}: {len(x):> 9}", **kw)
        ax2.hist(
            x, bins=bins2, label=f"{gen_status}: {np.sum(np.abs(x) < 1):> 9}", **kw
        )
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.legend(title="generatorStatus")
    ax2.legend(title="generatorStatus")
    fig.text(0.5, 0.03, "vertex position in z [mm]", ha="center")
    return (fig,)
