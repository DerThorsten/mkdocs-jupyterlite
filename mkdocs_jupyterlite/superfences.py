import urllib
IFRAME_TEMPLATE = """

<iframe src="{env}/lite/repl/index.html?kernel={kernel}&code={source}" width="100%" height="500px">
</iframe>

"""

def repl_formater(source, language, css_class, options, md, classes=None, id_value='', attrs=None, **kwargs):
    print(f"in repl_formater with source: {source} and options: {options}")

    env = options.get("env", "my_env")
    kernel = options.get("kernel", "xpython")
    
    code_block = urllib.parse.quote_plus(source)
    return IFRAME_TEMPLATE.format(env=env, kernel=kernel, source=code_block)