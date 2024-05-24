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
| `theme`   | The theme to use for the repl.        |`light`|
| `toolbar` | Whether to show the toolbar.          |1|


!!! note

    The theme needs to
    be in the environment specified in the `env` option. 


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