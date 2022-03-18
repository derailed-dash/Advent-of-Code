---
title: Packages and Environments
tags: 
  - name: Python Package Index
    link: https://pypi.org/
  - name: Python Packaging Authority
    link: https://www.pypa.io/en/latest/
  - name: Pip documentation
    link: https://pip.pypa.io/en/stable/
  - name: Python Environments in VS Code
    link: https://code.visualstudio.com/docs/python/environments
---
## The Need for Packages

Frequently we will need to import a package that is not part of the core Python installation. For example, my Advent of Code solutions often make use of installable packages like:

- _imageio_ - for reading and writing image files
- _matplotlib_ - for plotting charts and graphical data; for creating visualisations
- _numpy_ - for data science and manipulating multidimensional array data
- _pandas_ - for working with tabular data
- _scipy_ - for applying mathematical algorithms
- _Pillow_ - for manipulating images
- _parsimonious_ - for parsing grammars, extracting tokens

## Package Managers

To install packages like these, we need to use a **Package Manager**. A package manager provides the ability to install and uninstall packages.  But in addition, a package manager resolves dependencies.  This means that if you want to install package `x`, but package `x` depends on package `y`, then the package manager will automatically install both `x` and `y`, in the right order.

## Pip

Python comes pre-installed with its own package manager, called **pip**. To use pip, simply type `pip <command>`, e.g.

```python
# install matplotlib
pip install matplotlib

# uninstall matplotlib
pip uninstall matplotlib

# upgrade matplotlib
pip install --upgrade matplotlib

# upgrade pip itself
pip install --upgrade pip
```

Although you can just use `pip <command>` as shown above, it's generally recommended to instead use this syntax:

```python
py -m pip <command>
```

This syntax ensures that pip installs the package to the currently active Python runtime or environment.

## Virtual Environments

### What is a Virtual Environment?

Virtual environments are isolated Python contexts in which we can install Python packages. In short, virtual environments isolate dependencies of Python projects. 

Say what?

Well, you might be working on project `a` that requires packages `x`, and package `x` depends on package `y`. And then you might start working on project `b`, which needs package `z`. But package `z` won't work if you have package `y` installed. So your two projects have incompatible package requirements.

The answer? Virtual environments!  You simply create a dedicate virtual environment for each project.

Here are some reasons why virtual environments are a good thing:

- Multiple projects may have conflicting dependencies.
- Projects may conflict with operating system dependencies. Particularly on Linux systems, installing packages outside of a virtual environment could break the OS, given that the OS may have specific version dependencies.
- There may be a need to test code against different Python and library versions.
- There may be a need to distribute your project, along with specific environment dependencies.  E.g. for standalone applications.

### Creating a Virtual Environment

1. Create your project folder, as usual.
1. Within your project folder, create a virtual enviroment. You do this using the `venv` command.  For example, to create a virtual environment called `.my-proj-venv`: \
`py -m venv .my-proj-venv`
1. Add `.my-proj-venv` to your project's `.gitignore`, since we don't want it included in version control.

### Using Your Virtual Environment

You need to **activate** the virtual environment, every time you want to use it.  I.e. every time you're working in an associated Python project.

Once activated, any `pip` installs you perform will be done _within_ the virtual environment.

Fortunately, if you're using VS Code, then VS Code will automatically detect your virtual environment the next time you open your project folder. From then onwards, it will automatically activate the virtual environment for you.

### Tips for Working with Virtual Environments

Here are my general thoughts on how to work with virtual environments:

- They are not portable. They are machine specific. They should be recreated on any given machine.
- Don't put them under version control. Thus, exclude your virtual environment folder in your `.gitignore` file.
- Don't keep your virtual environment folder in a synchronised folder.  E.g. don't put them in Google Drive!
- Create a `requirements.txt` file that captures all your installed packages for a given project. Whenever you install / update / remove any packages from your virtual environment, refresh this file. To create / refresh your `requirements.txt`, just run this: \
`py -m pip freeze > path/to/your/requirements.txt`
- Your `requirements.txt` _should_ be under version control.
- To install the same packages on a different machine, set up a virtual environment on the other machine, and then replicate the package configuration on that machine, as follows: \
`py -m pip install -r path/to/your/requirements.txt`

