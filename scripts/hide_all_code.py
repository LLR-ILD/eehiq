#!/usr/bin/env python3
import glob
import os

import nbformat


def hide_all_code(iter_notebooks, hide_tag="hide-input"):
    """Hide all code cells of the jupyter book.

    Ensure that there is a `hide-input` cell tag in the metadata of any cell
    in any notebook that contributes to the book.
    """
    for nb_path in iter_notebooks:
        ntbk = nbformat.read(nb_path, nbformat.NO_CONVERT)
        has_made_changes = False
        for cell in ntbk.cells:
            cell_tags = cell.get("metadata", {}).get("tags", [])
            if hide_tag not in cell_tags:
                cell_tags.append(hide_tag)
                has_made_changes = True
            if len(cell_tags) > 0:
                cell["metadata"]["tags"] = cell_tags
        if has_made_changes:
            print("Hide code in", nb_path)
            nbformat.write(ntbk, nb_path)


def resize_images(iter_notebooks):
    for nb_path in iter_notebooks:
        ntbk = nbformat.read(nb_path, nbformat.NO_CONVERT)
        has_made_changes = False
        for cell in ntbk.cells:
            if cell["cell_type"] != "code":
                continue
            has_ipython_display = False
            for op in cell["outputs"]:
                if "data" not in op:
                    continue
                plain_text = op["data"].get("text/plain", "")
                if "<IPython.core.display.Image object>" in plain_text:
                    has_ipython_display = True
                    break
            if not has_ipython_display:
                continue
            meta_ipython_display = op.get("metadata", {})
            img_width = meta_ipython_display.get("image/png", {}).get("width", 400)
            img_width = str(min(100, int(49 * float(img_width) / 400))) + "%"
            cell_render = cell.get("metadata", {}).get("render", {})
            if cell_render.get("image", {}).get("width", "") == img_width:
                continue
            has_made_changes = True
            cell_render["image"] = {"width": img_width}
            cell["metadata"]["render"] = cell_render
        if has_made_changes:
            print("Resize images in", nb_path)
            nbformat.write(ntbk, nb_path)


if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    iter_notebooks = list(glob.glob(os.path.join(repo_root, "docs/**/*.ipynb")))
    resize_images(iter_notebooks)
    hide_all_code(iter_notebooks)
