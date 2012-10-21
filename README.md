Overview
========
Buildout recipe for retching isolated python builds.

Usage
=====

Here's an example for a buildout.cfg file that uses this recipe:

    [buildout]
    include-site-packages = false
    unzip = true
    parts = python scripts
    python = python

    [python]
    recipe = infi.recipe.python:download
    executable = parts/python/bin/python
    download-base = ftp://ci.infinidat.com/workspace/python
    version = v2.7.2.5

    [scripts]
    dependent-scripts = true
    recipe = infi.vendata.console_scripts
    eggs = ipython
    interpreter = python

Checking out the code
=====================

This project uses buildout and infi-projector, and git to generate setup.py and __version__.py.
In order to generate these, first get infi-projector:

    easy_install infi.projector

    and then run in the project directory:

        projector devenv build
