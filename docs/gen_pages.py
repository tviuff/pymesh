from pathlib import Path

import mkdocs_gen_files


with mkdocs_gen_files.open("foo.md", "w") as f:
    print("This page is auto-generated using the mkdocs-gen-files plugin!", file=f)
