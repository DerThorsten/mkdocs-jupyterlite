
from setuptools import setup, find_packages


setup(
    name='mkdocs-jupyterlite',
    version='0.1.0',
    description='A MkDocs plugin',
    long_description='',
    keywords='mkdocs',
    url='',
    author='Your Name',
    author_email='your email',
    license='MIT',
    python_requires='>=2.7',
    install_requires=[
        'mkdocs>=1.0.4',
        'jupyterlite>=0.3.0',
        'jupyterlite-core>=0.3.0',
        'jupyter_server',
        "appdirs",
        "jupytext",
        'jupyterlite-xeus>=0.1.8',
        # micromamba is atm requried.... 
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'jupyterlite-plugin = mkdocs_jupyterlite.plugin:JupyterlitePlugin'
        ]
    }
)
