
import subprocess
import logging
from pathlib import Path
import shutil

def mount_to_comma_separated_string(mounts_config):
    return ",".join([f"{mount.host}:{mount.target}" for mount in mounts_config])





def needs_build(lite_hash, lite_env_name, out_dir):
    # has hash file
    hash_file_path = out_dir / ".hash"
    print(f"hash file: {hash_file_path}")
    if hash_file_path.exists():
        with open(hash_file_path, 'r') as f:
            hash_str = f.read()
        
        print(f"comparing {hash_str} to {lite_hash}")
        if hash_str == str(lite_hash):
            print("hashes match")
            return False 
        else:
            print("hashes do not match")
            return True
    else:
        print("hash file does not exist")
        return True


def build_jupyterlite(config, lite_env_name, lite_env_config, out_dir,content_dir):
    print(f"building {lite_env_name}")


    mounts = mount_to_comma_separated_string(lite_env_config.mounts)
    out_dir.mkdir(parents=True, exist_ok=True)

    # ensure dirs exists
    out_dir.mkdir(parents=True, exist_ok=True)

    lite_hash = lite_env_config.hash(lite_env_name)
    nb = needs_build(lite_hash=lite_hash,
                     lite_env_name=lite_env_name, 
                     out_dir=out_dir)
    if nb:

        cmd = ["jupyter", "lite", "build", "--XeusAddon.environment_file", str(lite_env_config.env_file),
                "--XeusAddon.mounts", mounts, "--output-dir", str(out_dir), "--contents", str(content_dir)]
        
        subprocess.run(cmd, check=True)

        hash_file_path = out_dir / ".hash"
        with open(hash_file_path, 'w') as f:
            print(f"{lite_hash} hash file: {hash_file_path}")
            f.write(str(lite_hash))
    else:
        print(f"{lite_env_name} is up to date")

  


    return