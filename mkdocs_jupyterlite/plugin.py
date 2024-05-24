import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import yaml
import fnmatch
import tempfile
import json
from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin
import mkdocs
import urllib.parse

from .lite import build_jupyterlite

import shutil
from appdirs import AppDirs
mkdocs_lite_dirs = AppDirs("mkdocs-jupyterlite", "mkdocs-jupyterlite")

import hashlib
# import logging
# log = logging.getLogger(f"mkdocs.plugins.{__name__}")
# logging.basicConfig(level=logging.INFO)

import pprint
import jupytext

from .notebooks import convert_notebooks

IFRAME_TEMPLATE = """
<iframe src="{env}/lite/repl/index.html?kernel={kernel_name}&code={code}" width="100%" height="500px">
</iframe>
"""




class MountConfig(Config):
    host = config_options.Dir(exists=True)  # required
    target = config_options.Type(str)

class LiteConfig(Config):
    env_file  = config_options.File(exists=True)  # required
    mounts = config_options.ListOfItems(config_options.SubConfig(MountConfig), default=[])
    build = config_options.Type(int, default=0)
    notebook_dir = config_options.Dir(default=None)
    notebook_pattern = config_options.Type(str, default="*")
    notebook_doc_path = config_options.Type(str, default="examples")
    kernel_mapping = config_options.DictOfItems(config_options.Type(str), default={'py': 'xpython'})

    def hash(self, name):
        # load content of env_file as yaml
        with open(self.env_file, 'r') as stream:
            env_content = yaml.safe_load(stream)
            
        # dump content as string
        env_content_str = yaml.dump(env_content)

        # mounts as comma separated string
        mounts_str = ",".join([f"{mount.host}:{mount.target}" for mount in self.mounts])
        
        full_str = f"{name}{env_content_str}{mounts_str}{self.build}"

        return hashlib.sha256(full_str.encode()).hexdigest()



class JupyterlitePluginConfig(Config):
    environments =  config_options.DictOfItems(config_options.SubConfig(LiteConfig))  # required


class JupyterlitePlugin(BasePlugin[JupyterlitePluginConfig]):


    def __init__(self):
        self.enabled = True
        self.total_time = 0

        self.cache_dir = Path(mkdocs_lite_dirs.user_cache_dir)
        self._env_notebook_files = {}

    # def on_serve(self,server, config, builder):
    #     return server

    # def on_pre_build(self, config):
    #     return

    def _env_cache_dir(self, lite_env_name):
        return self.cache_dir / lite_env_name
    
    def _env_lite_cache_dir(self, lite_env_name):
        return self._env_cache_dir(lite_env_name) / "lite"
    
    def _env_notebook_markdown_dir_root(self, lite_env_name):
        return self._env_cache_dir(lite_env_name) / "notebooks_markdown"

    def _env_notebook_markdown_dir(self, lite_env_name):
        docs_path = self._docs_path(lite_env_name)
        return self._env_notebook_markdown_dir_root(lite_env_name)/ docs_path

    def _env_notebook_ipynb_dir(self, lite_env_name):
        return self._env_cache_dir(lite_env_name) / "notebooks_ipynb"
    
    def _docs_path(self, lite_env_name):
        doc_path_str =  self.config['environments'][lite_env_name]["notebook_doc_path"]
        doc_path_parts = doc_path_str.split("/")
        doc_path = Path(os.path.join(*doc_path_parts))
        return doc_path


    def on_files(self, files, config):
        collect_all_files = []
        lite_envs = self.config.get("environments")
        for lite_env_name, lite_env_config in lite_envs.items():
            
            nbdir = self._env_notebook_markdown_dir(lite_env_name)
          
            for item in  self._env_notebook_files[lite_env_name]:
                print("item", item)

                # file_name is <some name>.py
                file_name = item.name
                
                # extract original extension, in this case py
                # (note that we need to remove the leading dot)
                extenstion = item.suffix
                extenstion = extenstion[1:]

                kernel_name = lite_env_config.kernel_mapping[extenstion]

                # get <some name>
                item_name = Path(file_name).stem

                # markdown path
                markdown_path = nbdir / f"{item_name}.{extenstion}.md"


                # read the file
                with open(markdown_path, 'r') as f:
                    content = f.read()
                    # append new line to content
                    content = content + "\n"

                    n_parts = len(self._docs_path(lite_env_name).parts)
                    # for each part we need to go up one level
                    go_up = ""
                    for i in range(n_parts):
                        go_up = go_up + "../"


                    content = content + f"[run notebook]({go_up}{lite_env_name}/lite/lab/index.html?path={item_name}.ipynb&kernel={kernel_name})"
                
                # write the file
                with open(markdown_path, 'w') as f:  
                    f.write(content)

                print("markdown_path", markdown_path)

                # create an entry for each markdown file
                file = mkdocs.structure.files.File(
                    path=self._docs_path(lite_env_name) /  f"{item_name}.{extenstion}.md",
                    src_dir=self._env_notebook_markdown_dir_root(lite_env_name),
                    dest_dir=Path(config.get('site_dir')),  
                    use_directory_urls=False)

                files.append(file)



        return files


    
    def on_config(self, config):

        lite_envs = self.config.get("environments")

        self._env_notebook_files = {}

        for lite_env_name, lite_env_config in lite_envs.items():
            env_cache_dir = self.cache_dir / lite_env_name

            notebook_dir = self.config['environments'][lite_env_name].get("notebook_dir")
            notebook_pattern = self.config['environments'][lite_env_name].get("notebook_pattern")
            kernel_mapping = self.config['environments'][lite_env_name].get("kernel_mapping")

            notebooks = convert_notebooks(notebook_dir=notebook_dir, notebook_pattern=notebook_pattern, 
                              kernel_mapping=kernel_mapping,
                              outdir_markdown=self._env_notebook_markdown_dir(lite_env_name),
                              outdir_ipynb=self._env_notebook_ipynb_dir(lite_env_name))

            self._env_notebook_files[lite_env_name] = notebooks

        for lite_env_name, lite_env_config in lite_envs.items():
            env_cache_dir = self.cache_dir / lite_env_name
            build_jupyterlite(config=config, lite_env_name=lite_env_name, 
                              lite_env_config=lite_env_config,
                              out_dir=env_cache_dir / "lite",
                              content_dir=self._env_notebook_ipynb_dir(lite_env_name))
        

        return config
    

    def on_post_build(self, config):

        for lite_env_name, lite_env_config in lite_envs.items():
            env_cache_dir = self.cache_dir / lite_env_name
            build_jupyterlite(config=config, lite_env_name=lite_env_name, 
                              lite_env_config=lite_env_config,
                              out_dir=env_cache_dir / "lite",
                              content_dir=self._env_notebook_ipynb_dir(lite_env_name))

            
            # copy jupterlite deployment to site_dir
            lite_dir = self._env_lite_cache_dir(lite_env_name)
            page_lite_dir = Path(config.get('site_dir')) /  lite_env_name / "lite"
            shutil.copytree(lite_dir, page_lite_dir)
            
        return config



    # we need to fix the relative path 
    # to the lite deployment depending on the
    # location of the markdown file
    def on_page_content(self, html, page, config, files):
        if 'iframe id="__repl__"' in html:
            path = Path(page.file.src_path)
            if str(path) != "index.md":
                go_n_back = len(path.parts)
                go_back_str = ""
                for i in range(go_n_back):
                    go_back_str = go_back_str + "../"
                return html.replace('<iframe id="__repl__" src="./',f'<iframe id=codeframe src="{go_back_str}')
        return html