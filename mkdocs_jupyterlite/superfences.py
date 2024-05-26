import urllib

from .content_collector import content_collector
from .notebooks import convert_code_to_ipynb


REPL_IFRAME_TEMPLATE = """

<iframe id="__repl__" src="./{env}/lite/repl/index.html?kernel={kernel}&code={source}&theme={theme}&toolbar={toolbar}" width={width} height={height}>
</iframe>

"""

NOTEBOOK_IFRAME_TEMPLATE = """
<iframe id="__repl__" src="./{env}/lite/notebooks/index.html?kernel={kernel}&theme={theme}&toolbar={toolbar}&path={path}" width={width} height={height}>
</iframe>
"""




def _pass_trough_validator(language, inputs, options, attrs, md):
    for k,v in inputs.items():
        options[k] = v
    return True




def notebook_validator(language, inputs, options, attrs, md):
    print(f"in notebook_validator with {language=}, {inputs=}, {options=}, {attrs=}, {md=}")
    return _pass_trough_validator(language, inputs, options, attrs, md)





def notebook_formater(source, language, css_class, options, md, classes=None, id_value='', attrs=None, **kwargs):

    try:    

        # convert the annotated code to a notebook
        env=options["env"]
        kernel=options["kernel"]
        name=options["name"]

        ipynb = convert_code_to_ipynb(source, kernel=kernel)


        # call collector
        collector = content_collector()
        collector.add(
            env=env,
            path=f"{name}.ipynb",
            content=ipynb
        )


        print(options)

        name = options["name"]

        notebook_args = dict(
            env=options.get("env", "JupyterLab Light"),
            kernel=kernel,
            width=options.get("width", "100%"),
            height=options.get("height", "500pxs"),
            theme=options.get("theme", "light"),
            toolbar=options.get("toolbar", "1"),
            path=options.get("path", f"{name}.ipynb"),
        )
        for k,v in notebook_args.items():
            notebook_args[k] = urllib.parse.quote_plus(v)

        return NOTEBOOK_IFRAME_TEMPLATE.format(**notebook_args)
    except Exception as e:
        # print traceback
        import traceback
        traceback.print_exc()
        import sys
        sys.exit(1)




def repl_validator(language, inputs, options, attrs, md):

    return _pass_trough_validator(language, inputs, options, attrs, md)



def repl_formater(source, language, css_class, options, md, classes=None, id_value='', attrs=None, **kwargs):
    repl_args = dict(
        source=source,
        env=options.get("env", "JupyterLab Light"),
        kernel=options.get("kernel", "xeus-python"),
        width=options.get("width", "100%"),
        height=options.get("height", "500pxs"),
        theme=options.get("theme", "light"),
        toolbar=options.get("toolbar", "1"),
    )
    for k,v in repl_args.items():
        repl_args[k] = urllib.parse.quote_plus(v)


    iframe =  REPL_IFRAME_TEMPLATE.format(**repl_args)
    return iframe