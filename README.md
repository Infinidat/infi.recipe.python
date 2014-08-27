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
    version = v2.7.6.15

    [scripts]
    dependent-scripts = true
    recipe = infi.vendata.console_scripts
    eggs = ipython
    interpreter = python

Checking out the code
=====================

Run the following:

    easy_install -U infi.projector
    projector devenv build
