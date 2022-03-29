# Technical comments

:::{note}
We are not aware of an array-based way for extracting the particles from `.slcio` files.
Thus, we will restrict ourselves to low events numbers, or overview level variables.
More quantitative studies will follow in the `ROOT BASED` part.
:::

Of course, this would not be an issue when directly working in C++.

## Data source

The `.slcio` file is part of the MC2020 ILC-250GeV campaign of ILD.
It can be found on the grid (VO-ILC) or on the DESY or KEK file systems.
For this analyis, the specific file that is used here was also copied to the
LLR servers/polui.
This book was built on a polui machine.
At other machines, it will be necessary to change the data folder.


## LCIO

The code in this part directly uses the
(py-)[LCIO](https://github.com/iLCSoft/LCIO) framework.
The LCIO library can be accessed in (python3) jupyter notebook through LCIO's
python bindings.

A procedure for setting up such a kernel on the polui jupyterhub is described
[later on](./pyLCIO3_on_LLR_jupyterhub.md).
