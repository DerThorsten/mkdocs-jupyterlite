# Repl

A jupyterlite repl can be included in a markdown file using the following syntax:

````{.md option="Repl"}
```{.repl kernel="xpython" env="my_env"}
print('hello world')
```
````


## Options

The `repl` directive supports the following options:
<!-- table -->

| Option | Description | Default |
|--------|-------------|---------|
| `env`     | The environment to use for the repl.  |-|
| `kernel`  | The kernel to use for the repl.       |-|
| `width`   | The width of the repl.                |`100%`|
| `height`  | The height of the repl.               |`500px`|
| `theme`   | The theme to use for the repl.        |`JupyterLab Light`|
| `toolbar` | Whether to show the toolbar.          |1|


!!! note

    At the moment, it is recommended to
    install the theme package in the **host** environment
    and not in then `emscripten-wasm32` environment.


## Example
````{.md option="Repl"}
```{.repl kernel="xpython" env="themes_env" theme="JLDracula"}
print('hello world')
```
````

This will render the following:

```{.repl kernel="xpython" env="themes_env" theme="JLDracula"}
print('hello dracular')
```