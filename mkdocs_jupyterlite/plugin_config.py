
from pathlib import Path
from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin
import mkdocs
import yaml
import hashlib



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
