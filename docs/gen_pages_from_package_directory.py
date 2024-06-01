"""Generate code reference pages and navigation.

Based on the recipe of mkdocstrings:
https://github.com/mkdocstrings/mkdocstrings

Credits:
Timothée Mazzucotelli
https://github.com/pawamoy
"""

from pathlib import Path

import mkdocs_gen_files

PKG_SRC_DIR = "pymesh"
PKG_FILE_SRCH_PAT = "*.py"

DOC_SRC_DIR = "auto-doc-pages"
DOC_SUMMARY_FILE = "SUMMARY.md"

nav = mkdocs_gen_files.Nav()
for path in sorted(Path(PKG_SRC_DIR).rglob(PKG_FILE_SRCH_PAT)):

    # Get path in module, documentation and absolute
    path_no_ext = path.relative_to(PKG_SRC_DIR).with_suffix("")
    path_md = path.relative_to(PKG_SRC_DIR).with_suffix(".md")
    path_md_full = Path(DOC_SRC_DIR, path_md)

    # Handle edge cases
    parts = (PKG_SRC_DIR,) + tuple(path_no_ext.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
        path_md = path_md.with_name("index.md")
        path_md_full = path_md_full.with_name("index.md")
    elif parts[-1] == "__main__":
        continue
    nav[parts] = path_md.as_posix()  # TODO remove "pymesh" from nav keys

    # Write docstring documentation to disk via parser
    with mkdocs_gen_files.open(path_md_full, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: {ident}")

    # Update parser
    mkdocs_gen_files.set_edit_path(path_md_full, path)
    print(f"Doing docs for {path}")

with mkdocs_gen_files.open(DOC_SRC_DIR + "/" + DOC_SUMMARY_FILE, "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
