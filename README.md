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
    recipe = infi.recipe.python
    version = v2.7.8.2

    [scripts]
    dependent-scripts = true
    recipe = infi.recipe.console_scripts
    eggs = ipython
    interpreter = python

Checking out the code
=====================

To run this code from the repository for development purposes, run the following:

    easy_install -U infi.projector
    projector devenv build

Python 3 support is experimental and not fully tested.
