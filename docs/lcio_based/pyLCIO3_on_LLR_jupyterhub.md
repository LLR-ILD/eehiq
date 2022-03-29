# pyLCIO3 on LLR jupyterhub

## Usage

- In a terminal:
  ```sh
  ssh -N -L20443:polui01.in2p3.fr:443 -L7001:polui.in2p3.fr:7001 kunath@llrgate01.in2p3.fr &
  ```
  - If you are in the LLR network, this step is not necessary.
    You can directly point you web browser to: [https://polui01.in2p3.fr](https://polui01.in2p3.fr).
- Open in a web browser: [https://localhost:20443](https://localhost:20443).
- Open a notebook. If you followed **Setup**, the pyLCIO kernel should appear under `Kernel > Change kernel`.

## Setup

On polui, it should not actually be necessary for you to create the `pyroot` conda environment
and to link it with LCIO. It suffices to use the reference installation at `/home/llr/ilc/kunath/bin/LCIO/setup.sh`.

The simplest way to expose the python environment/kernel to jupyter is:
```bash
source /home/llr/ilc/kunath/bin/LCIO/setup.sh  # To activate the conda environment.
python -m ipykernel install --user
```

The output of the last command tells you where the new kernelspec is installed.
In may case, the folder name is `/grid_mnt/vol_home/llr/ilc/kunath/.local/share/jupyter/kernels/python3`.
Then, a small change to the `kernel.json` in that folder is necessary:

```json
{
 "argv": [
  "bash",
  "-c",
  "source /home/llr/ilc/kunath/bin/LCIO/setup.sh' && exec /home/llr/ilc/kunath/miniconda3/envs/pyroot/bin/python -m ipykernel_launcher -f '{connection_file}' "
 ],
 "display_name": "pyLCIO",
 "language": "python",
 "metadata": {
  "debugger": true
 }
}
```

Optionally, we can change the `display_name`
All that we needed to change the `argv` field. By default, it contained:

```json
 "argv": [
  "/home/llr/ilc/kunath/miniconda3/envs/pyroot/bin/python",
  "-m",
  "ipykernel_launcher",
  "-f",
  "{connection_file}"
 ],
```

### pyROOT

When working with ROOT, I prefer setting up a conda python environment.
This requires having set up the [conda](https://docs.conda.io/en/latest/miniconda.html) package/environment management system.

`mamba create -n pyroot -c conda-forge root cmake ipykernel numpy matplotlib pandas uproot`

- `mamba`: A faster depency solver system than default conda. Can be installed with:
  `conda activate base; conda install -c conda-forge mamba`.
  Alternatively, just replace `mamba` by `conda` in the line above.
- `root`: Installs CERN ROOT with python bindings. Is much faster than an installation from source.
- `cmake`: Is needed for the build of LCIO (The default cmake version on polui is too old).
- `ipykernel`: Makes this environement available to `jupyter`
- `python=3.10`: Could be added if you want a specific version of python.
- `numpy matplotlib pandas uproot`: Some python packages that I already know that I will need for my analysis. More could be added here.
  Later, packages can be added via `conda activate pyroot; conda install $PACKAGE_NAME`.

### LCIO

```bash
mkdir -p ~/bin
cd ~/bin
git clone https://github.com/iLCSoft/LCIO.git
cd LCIO
git checkout v02-17  #  Optional: Use a specific version.
conda activate pyroot
mkdir build
cd build
cmake -DBUILD_ROOTDICT=ON -D CMAKE_CXX_STANDARD=17 ..
make -j 4 install
cd ..
```

Two changes should be performed on `~/bin/LCIO/setup.sh`
1. Add a line that activates the conda environment.
2. Change `lib` to `lib64` in `LD_LIBRARY_PATH`.

The altered setup script then should look like this:

```bash
#!/bin/sh
# Next line is new.
source '/home/llr/ilc/kunath/miniconda3/bin/activate' '/home/llr/ilc/kunath/miniconda3/envs/pyroot'
export LCIO='/home/llr/ilc/kunath/bin/LCIO'
export PATH=$LCIO/bin:$LCIO/tools:$PATH
export LD_LIBRARY_PATH=$LCIO/lib64:$LD_LIBRARY_PATH  # Currently `lib` in LCIO. Must be changed to lib64.
export PYTHONPATH=$LCIO/src/python:$PYTHONPATH
alias pylcio='python $LCIO/src/python/pylcio.py'
```

and can be used as
```sh
source /home/llr/ilc/kunath/bin/LCIO/setup.sh
```
