import fnmatch
from pathlib import Path
import jupytext


def convert_notebooks(notebook_dir, notebook_pattern, kernel_mapping, outdir_markdown, outdir_ipynb):
    notebook_dir = Path(notebook_dir)
    if not notebook_dir.exists():
        raise ValueError(f"{notebook_dir} does not exist")
    

    outdir_markdown.mkdir(parents=True, exist_ok=True)
    outdir_ipynb.mkdir(parents=True, exist_ok=True)

    notebooks = []
    # iterate all files in examples dir
    for item in notebook_dir.iterdir():
        print(f"check item: {item} against {notebook_pattern}")
        if fnmatch.fnmatch(item.name, notebook_pattern):
            print(f"adding {item} to notebooks")
            notebooks.append(item)
        else:
            print(f"skipping {item}")
    

    # convert notebooks to markdown
    for notebook in notebooks:
        extension = notebook.suffix
        #remove leading dot
        extension = extension[1:]

        print("get kernel name for extension", extension)
        kernel_name = kernel_mapping[extension]
        print("kernel_name", kernel_name)
        print(f"converting {notebook} to markdown")
        with open(notebook, 'r') as f:
            nb = jupytext.read(f, as_version=4)
            markdown = jupytext.writes(nb, fmt='md')
            out_path = outdir_markdown / notebook.with_suffix(f".md").name
            out_path.write_text(markdown)

            # rename file to have correct extension 
            new_name = out_path.with_suffix(f".{extension}.md")
            out_path.rename(new_name)
    
    # convert notebooks to ipynb
    for notebook in notebooks:
        print(f"converting {notebook} to ipynb")
        with open(notebook, 'r') as f:
            nb = jupytext.read(f, as_version=4)

            nb.metadata["kernel_info"] = {}
            nb.metadata["kernel_info"]["name"] = kernel_name


            ipynb = jupytext.writes(nb, fmt='ipynb')
            out_path = outdir_ipynb / notebook.with_suffix(".ipynb").name
            out_path.write_text(ipynb)
    return notebooks
