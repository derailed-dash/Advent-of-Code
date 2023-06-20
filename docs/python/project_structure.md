---
title: Project Structure
---

## Why?

It is a good idea for any Python project to have a clear folder structure. This makes it easier for you to maintain.  But it also helps others to easily understand your project.

## A Good General Project Structure

Here is a generic folder structure that you can generally use for Python projects.

```bash
.                            # Root - the name of your project
├── README.md                   # The top-level project README, describing project purpose, who to use it, etc
├── LICENSE                     # How this project is licensed, i.e. what others are allowed to do this code
├── requirements.txt            # The packages that are required in order for your code to run
├── .gitignore                  # Used to tell git which resources should not be under git source control
├── .pylintrc                   # Optional configuration for pylint, if you use it
├── .env                        # For environment variables, e.g. PYTHONPATH
|
├── src/                     # Where the source code lives 
├── tests/                   # For storing tests, e.g. unit tests 
├── docs/                    # Where documentation is stored 
└── scripts/                 # For any scripts or automation, e.g. for project setup 
```

## My Advent of Code Project Structure

Here's how I've set up my AoC repo:

```bash
Advent-of-Code             # Root of my project
├── README.md                # Repo documentation
├── LICENSE   
├── requirements.txt         # pip requirements
├── .gitignore
├── .pylintrc                # Pylint configuration
├── .env                     # PYTHONPATH=src
├── .AoC-env/                # Python virtual env
|
├── src/                     # Top level of src code
|   ├── Aoc_2015/              # Source for AoC 2015
|   |   ├── d01/                 # Day 1
|   |   |   ├── input/             # Input files
|   |   |   └── d01_whatever.py    # Solution code
|   |   ├── d02/                 # Day 2
|   |   |   ├── input/             # Input files
|   |   |   └── d02_whatever.py    # Solution code
|   |   └── ...                  # Day n
|   ├── Aoc_2016/              # Source for AoC 2016 
|   ├── ...                    # And so on... 
|   ├── Aoc_2022/              # Source for AoC 2022 
|   ├── common/                # A package containing some reused code 
|   |   └── type_defs.py         # Some reused classes and other definitions
|   └── template_folder/       # A package containing some reused code 
|       ├── input/               # Input files
|       └── template.py          # My solution template
|
├── tests/                   # For storing tests, e.g. unit tests 
|   └── test_type_defs.py      # Unit tests for the type_defs module
|
├── docs/                    # Where documentation is stored 
|   ├── 2015/                  # Walkthroughs for 2015 
|   ├── 2016/                  # Walkthroughs for 2016 
|   ├── ...                    # And so on... 
|   ├── 2022/                  # Walkthroughs for 2022 
|   └── python/                # For the Python journey pages 
|
└── scripts/                 # Useful scripts
    └── create_year.ps1        # Windows PowerShell script for generating template files for a year
```