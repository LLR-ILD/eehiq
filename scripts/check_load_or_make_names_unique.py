#!/usr/bin/env python3
import glob
import os
import tokenize
from io import StringIO

import nbformat

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def yield_nb(root_path=os.path.join(repo_root, "docs")):
    glob_pattern = os.path.join(root_path, "**", "*.ipynb")
    for nb_path in glob.iglob(glob_pattern, recursive=True):
        if "_build" in nb_path.split(os.sep):
            continue
        yield nb_path


def yield_py(root_path=repo_root):
    glob_pattern = os.path.join(root_path, "**", "*.py")
    for py_path in glob.iglob(glob_pattern, recursive=True):
        if "_build" in py_path.split(os.sep):
            continue
        yield py_path


def yield_calls_to_decorator(code_string, decorator_name):
    g = tokenize.generate_tokens(StringIO(code_string).readline)
    previous_token = None
    decorator_call = []
    n_open_brackets = 0
    for token_info in g:
        if len(decorator_call) > 0:
            if token_info.string in "([":
                n_open_brackets += 1
            elif token_info.string in ")]":
                n_open_brackets -= 1
            elif n_open_brackets == 0:
                yield decorator_call
                decorator_call = []
            else:
                decorator_call.append(token_info)
        elif token_info.string != decorator_name:
            previous_token = token_info
        elif previous_token.string == "@":
            decorator_call.extend([previous_token, token_info])


def yield_decorator_instances_py(yield_py, decorator_name="load_or_make"):
    for py_path in yield_py():
        with open(py_path) as f:
            code_string = f.read()
        for token_list in yield_calls_to_decorator(code_string, decorator_name):
            # First 2 tokens are @ and `decorator_name`
            signature = "".join(map(lambda x: x.string, token_list[2:]))
            yield signature, py_path, str(token_list[0].start[0]), token_list[0]


def yield_decorator_instances_nb(yield_nb, decorator_name="load_or_make"):
    for nb_path in yield_nb():
        ntbk = nbformat.read(nb_path, nbformat.NO_CONVERT)
        for i_cell, cell in enumerate(ntbk.cells):
            if cell["cell_type"] != "code":
                continue
            code_string = cell["source"]

            i_start_call = code_string.find("@load_or_make")
            if i_start_call == -1:
                continue
            i_start_call_line = max(0, code_string[:i_start_call].rfind("\n"))
            code_string = code_string[i_start_call_line:]
            for token_list in yield_calls_to_decorator(code_string, decorator_name):
                # First 2 tokens are @ and `decorator_name`
                signature = "".join(map(lambda x: x.string, token_list[2:]))
                cell_lines_before_seach = code_string[:i_start_call_line].count("\n")
                cell_line = token_list[0].start[0] + cell_lines_before_seach
                yield signature, nb_path, f"{i_cell};{cell_line}", token_list[0]


def yield_decorator_instances(decorator_name="load_or_make"):
    yield from yield_decorator_instances_py(yield_py, decorator_name)
    yield from yield_decorator_instances_nb(yield_nb, decorator_name)


def find_double_names():
    all_names = {}
    duplicates = []
    # Last field fast list of all tokens. ood for debugging.
    for signature, file, line, _ in yield_decorator_instances("load_or_make"):
        names = signature.split(",")
        for name in names:
            # print(f"{name:<35} {os.path.basename(file)} ({line})")
            if name in all_names:
                file0, line0 = all_names[name]
                duplicates.append(
                    "\n".join(
                        [
                            f"{name}",
                            f"    Already in  {file0} ({line0}).",
                            f"    Now used in {file} ({line}).",
                        ]
                    )
                )
            else:
                all_names[name] = (file, line)
    if len(duplicates) > 0:
        prefix = "Duplicate resource names in `@load_or_make`\n"
        raise Exception(prefix + "\n".join(duplicates))


if __name__ == "__main__":
    find_double_names()
