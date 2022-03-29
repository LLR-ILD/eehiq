# eehiq

![GitHub repo size](https://img.shields.io/github/repo-size/LLR-ILD/eehiq)
[Website](https://llr.in2p3.fr/~kunath/eehiq).


## Setup

It is recommended to use a fresh python installation.

```bash
python -m pip install -r requirements-dev.txt
python -m pip freeze > requirements-dev-frozen.txt
python -m pip install -e .
python -m ipykernel install --user --name eehiq --display-name "Python (eehiq)"
pre-commit install  # Only if you want to contribute back to the repo. Enforces code style.
# The following requires assumes that you are on polui with the corresponding access rights:
ln -s /data_ilc/flc/kunath/local_only/eehiq data
```

## (Re-)building the book

To declutter the book, all code cells are hidden.
To add the required metadata to new cells, run `hide_all_code.py`.
Be sure to have saved all notebooks before running this, as it will overwrite the files.
``
```bash
./scripts/hide_all_code.py  # Be sure to have saved all notebooks.
jupyter-book clean docs  # Necessary if _toc.yml was changed.
jupyter-book build docs
rsync -aP docs/_build/html/ llrweb1.in2p3.fr:~/www/eehiq
```

### Deleting removed files on destination

The `rsync` command shown above does not delete files that are no longer used.
Over time, this can lead to a bloat in folder size on the web server.

If you are sure that you specified the correct destination,
you can add the `--delete` flag to the command.
This will take care of removing files that are no longer needed.
Be careful:
The command can have fatal consequences (data loss) if the wrong destination is specified.

```bash
rsync -aP --delete docs/_build/html/ llrweb1.in2p3.fr:~/www/eehiq
```

## Code tips

### `@load_or_make` decorator

To speed up the running of the notebooks, the `load_or_make` decorator has been defined in [lcio_checks/util.py](./src/lcio_checks/util.py).
This decorator caches the return values (figures or DataFrames).
To force the re-running of a function with this decorator, remove one of the
return values from the cache.
Alternatively, add `redo=True` to the function call.

All figures will be wrapped in an `IPython.display.Image`.
To obtain the unwrapped figure, add `redo=True, no_save=True`.
