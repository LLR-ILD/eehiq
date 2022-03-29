# Technical comments

The setup for this part is described in the repository's
[README](https://github.com/LLR-ILD/eehiq/README.md).

## Data source

This section assumes that you already have access to the `.slcio` file
and want to extract the `lctuple_DST` information into a `.root` file.
Obtaining the `.slcio` file is described
[in the LCIO based technical comments](../lcio_based/technical_comments.md).

Follow the steps outlined in
[this gist](https://gist.github.com/kunathj/d87d6c8b1821cf7d1f80876d6884577c)
to build a `.root` file through the LCTuple processor.
For completeness the current version of that gist's README is attached
as the [next section](./BuildMyLCTuple.md).

Afterwards you can point the code towards the location of your rootfile through
the `data_dir` field in the `lcio_checks` section of your
[`setup.cfg`](https://github.com/LLR-ILD/eehiq/setup.cfg).
