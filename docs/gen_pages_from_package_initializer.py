import csv
from pathlib import Path

import mkdocs_gen_files

src_dir = Path("pymesh")
init_file = src_dir / "__init__.py"

doc_folder = "auto-doc-pages"
doc_nav_file = "SUMMARY.md"
nav = mkdocs_gen_files.Nav()

class_paths = []
with open(init_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=" ")
    for line in reader:
        module_path = Path(*line[1].split("."))
        class_path = module_path / Path(line[-1])
        class_paths.append(class_path)

for class_path in sorted(class_paths):
    doc_path = class_path.relative_to(src_dir).with_suffix(".md")
    full_doc_path = Path(doc_folder, doc_path)
    nav_keys = list(class_path.relative_to(src_dir).parent.parts)
    nav_keys[-1] = class_path.parts[-1]

    # print(doc_path.as_posix())
    # print("  ", f"::: {".".join(class_path.parts)}")
    # print("    ", ".".join(nav_keys))

    nav[nav_keys] = doc_path.as_posix()
    with mkdocs_gen_files.open(full_doc_path, "w") as f:
        f.write(f"::: {'.'.join(class_path.parts)}")

with mkdocs_gen_files.open(Path(doc_folder, doc_nav_file), "w") as f:
    f.writelines(nav.build_literate_nav())
