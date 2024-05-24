import urllib
IFRAME_TEMPLATE = """

<iframe id="__repl__" src="./{env}/lite/repl/index.html?kernel={kernel}&code={source}&theme={theme}&toolbar={toolbar}" width={width} height={height}>
</iframe>

"""

def repl_validator(language, inputs, options, attrs, md):
    print(f"in repl_validator with {language=}, {inputs=}, {options=}, {attrs=}, {md=}")
    for k,v in inputs.items():
        print(f"inputs: {k} = {v}")
        options[k] = v
    return True

def repl_formater(source, language, css_class, options, md, classes=None, id_value='', attrs=None, **kwargs):
    print(f"in repl_formater with source: {source}  {language=}, {css_class=}, {options=}, {md=}, {classes=}, {id_value=}, {attrs=}, {kwargs=}")

    code_block=urllib.parse.quote_plus(source)
    repl_args = dict(
        env=urllib.parse.quote_plus(options.get("env", "JupyterLab Light")),
        kernel=urllib.parse.quote_plus(options.get("kernel", "xpython")),
        width=urllib.parse.quote_plus(options.get("width", "100%")),
        height=urllib.parse.quote_plus(options.get("height", "'500px'")),
        theme=urllib.parse.quote_plus(options.get("theme", "light")),
        toolbar=urllib.parse.quote_plus(options.get("toolbar", "1")),
        source=code_block
    )

    

    iframe =  IFRAME_TEMPLATE.format(**repl_args)
    return iframe