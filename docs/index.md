# Quicksart

## Lite environment
To use the JupyterLite plugin, you need to have a `*.yaml` file
describing the environment you want to use. This file should look like this:

```{.yaml title="my_env.yaml"}
name: xeus-lite-wasm
channels:
  - https://repo.mamba.pm/emscripten-forge
  - conda-forge
dependencies:
  - xeus-python
  - numpy
```
The usual `mkdocs.yml` needs should look needs to have the custom `pymdownx.superfences` with
a custom superfence named `repl` that uses the `mkdocs_jupyterlite.superfences.repl_formater` formatter
and the `jupyterlite-plugin` with the environments you want to use.

## Mkdocs configuration

```{.yaml title="mkdocs.yml"}
site_name: mkdocs-jupyterlite


markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: repl
          class: iframe
          format: !!python/name:mkdocs_jupyterlite.superfences.repl_formater
plugins:
  - jupyterlite-plugin:
      environments:
        my_env:
          build: 9
          env_file: my_env.yaml
          notebook_dir: notebooks
          notebook_pattern: "*.py"
          notebook_doc_path: "examples/notebooks"
          kernel_mapping:
            py: xpython
          mounts:
            - host: lite_envs/with_numpy/mounts/some_mount
              target: "/some/target/dir"
```

## Usage

To include a repl in your markdown file, you can use the following syntax:


````{.md option="Repl"}
```{.repl kernel="xpython" env="my_env"}
print('hello world')
```
````

This will render the following:

```{.repl kernel="xpython" env="my_env"}
print('hello world')
```


