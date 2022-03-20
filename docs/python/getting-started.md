---
title: Getting Started with Python
main_img:
  name: Argand Plot
  link: /assets/images/python.png
tags: 
  - name: Python Beginner's Guide
    link: https://wiki.python.org/moin/BeginnersGuide/Download
  - name: The Python Handbook
    link: https://www.freecodecamp.org/news/the-python-handbook
  - name: The Official Python Tutorial
    link: https://docs.python.org/3/tutorial/index.html
  - name: Getting started with Python in VS Code Tutorial
    link: https://code.visualstudio.com/docs/python/python-tutorial
  - name: Git
    link: https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control
---
If you're new to Python, then you'll want to start here.  If you're already comfortable using Python, then feel free to dive straight into the AoC walkthroughts, using the links above.

## Why Python?

If you're a **newbie** to programming, then Python is a great language to start with. If you have **a lot of programming experience**, then guess what?  Python is an amazing language to learn, and you'll love it.

Many years ago, I used to write software for a living. Back then, my preferred languages were Java and C#. These days, I don't write code in my job, though I do still need to know my way around. Now I write code as a hobby.  But I can honestly say: _of all the programming languages I've ever used, Python is my favourite._

For those of you coming from a background with languages like C, C#, Java, Javascript... You may find Python's syntax and structure a bit jarring.  But trust me: once you get your head around the differences, you'll love it, just like I do.

Here are some of Python's strengths:

- It's extremely readable.  It's syntax tends to be aligned to natural language.
- It's highly portable.  Your Python programs will run on just about any operating system.
- It's really easy to install and use.
- It's open source: free to use, and free to distribute.
- It's extremely versatile.  You can use it for console applications, web applications, automation, APIs, data science, machine learning, maths and statistics, graphs, visualisation, writing games, and so much more.
- There are a massive number open source libraries available, to do just about any task.

## My Recommendations for Getting Started

I recommend working through the following, to get started:

1. [Install Python](#getting-and-installing-python)
1. Get a [development environment / editor](#development-environment--editor)
1. [Get Git](#git)
1. [Learn the Python basics](#python-basics)

## Getting and Installing Python

To execute Python programs, you need to install Python on your machine.  It's possible you already have Python installed.  To check, open your command prompt (or shell) and run:

```> python --version```

If you get a response that shows you have any Python 3.x version installed, then you're good to go.  E.g.

![Verify Python Installation]({{'/assets/images/python-version.png' | relative_url }}){:style="width: 600px"}

If you haven't got Python installed, you'll want the latest available Python 3 version, which you can download from [here](https://www.python.org/downloads/){:target="_blank"}.  It's really quick and easy to install.  It should only take a couple of minutes.  Take a look [here](https://wiki.python.org/moin/BeginnersGuide/Download){:target="_blank"} if you need any guidance on installing Python.

Once you've installed it, check the installation as described above.

## Development Environment / Editor

You can write and run Python programs without a development environment. But it's a much better - and more effective - experience, if you have one.

A **development environment** adds a wealth of features, such as:

- The ability to conveniently organise files and folders into **projects**.
- **Syntax colouring**.
- **Linting** - flagging of problems in your code, such as syntax errors, warnings, stylistic errors, or something potentially dangerous.
- **Autocompletion** - the ability to offer likely completion of what you're typing.
- **Refactoring** - the ability to rename symbols, extract methods, etc.
- **Debugging** - the ability to step through code, show the current value of variables, stop at break points, etc.
- **Keyboard commands and shortcuts** that greatly improve productivity.
- Integration with **terminals / consoles / shells**.
- The ability install a number of freely available **extensions and plugins**, e.g. to integrate git, Docker, Jupyter Notebooks, enhanced visualisation of certain file types and formats, and so on.

### Visual Studio Code

My favourite development environment is **Visual Studio Code** - aka **VS Code** - which can be downloaded and installed from [here](https://code.visualstudio.com/){:target="_blank}.  (Note: VS Code is not the same as _Visual Studio_, which is a different product.)

Some benefits of VS Code:

- It is **open source and free**.
- It is **platform-agnostic**.  I.e. you can run it on a wide variety of operating systems, including Windows, Linux and Mac.
- Unlike some development environments, VS Code is a very **lightweight and fast** editor.
- It is **language-agnostic**. You can use it write much more than just Python.  E.g. if you want to write HTML, Javascript, markdown, yaml... No problem!
- It is supported by a massive library of **free extensions and plugins**.
- Really swish **Git integration**, out-of-the-box.
- It **looks great**.
- It is highly **configurable**.

![Visual Studio Code]({{'/assets/images/vs-code-screenshot.png' | relative_url }})

### Installing and Setting Up VS Code

Check out the following useful links:

- [Obtaining and Installing VS Code](https://code.visualstudio.com/){:target="_blank"}
- [VS Code Documentation Pages](https://code.visualstudio.com/docs){:target="_blank"}
- [VS Code Getting Started Videos](https://code.visualstudio.com/docs/getstarted/introvideos){:target="_blank"}
- [Setting Up VS Code](https://code.visualstudio.com/docs/setup/setup-overview){:target="_blank"}
- [Python in VS Code](https://code.visualstudio.com/docs/languages/python){:target="_blank"}
- **[Getting started with Python in VS Code Tutorial](https://code.visualstudio.com/docs/python/python-tutorial){:target="_blank"}**

### Install Useful Extensions

Now you'll want to install some extensions that will make your Python - and general development - experience better. In VS Code, click on the **Extensions** button in the left hand panel of buttons. I'd recommend installing the following:

- **Python (Microsoft)** - provides rich support for the Python language, including features such as IntelliSense (provided through Pylance), linting, debugging, code navigation, code formatting, refactoring, variable explorer, test explorer, and more.  Note that when you install this extension, it automatically installs **Pylance** and **Jupyter** (for Jupyter Notebook support).
- **Better Comments** - a cool plugin that enhances your comments.
- **Git Graph** - for visualing your Git repos.
- **Python Docstring Generator** - a cool plugin that helps with the creation of _docstrings_.  If you don't know what these are, then don't worry about this just yet!
- **Rainbow CSV** - Colourises any CSV files you open in VS Code.

Note: if you've followed the [Getting started with Python in VS Code Tutorial](https://code.visualstudio.com/docs/python/python-tutorial){:target="_blank"}, this will have guided you through installing some of these extensions.

## Git

Git is an extremely popular **version control system** (VCS). A VCS provides capabilities like these:

- The ability to store and track all the changes to your code or project.
- The ability to revert to your project to any point in its history. E.g. to get your code back to a previous state, before you made some catastrophic error!
- The ability to share and collaborate with others.
- The ability to obtain code from others.
- The ability branch code, e.g. for experimenting, building new features, fixing bugs, etc.
- The ability to integrate with other tools, like bug tracking and CI/CD pipelines.

### So Why Git?

Git is an open source VCS, created by the legendary Linus Torvalds.  You know... The guy that created Linux.

Git is:

- Really easy to use.
- Platform-agnostic.
- Extremely fast.
- Distributed! This means that you always have a complete copy of a proejct's history on your own machine! But you can (and should) make use of a centralised, cloud-based repo service, like [GitHub](https://github.com/){:target="_blank"}. In fact, all of my [AoC source code]({{ site.github.repository_url }}){:target="_blank"} is stored on **GitHub**, which is how I make it available to you.

### Installing Git

- Download and install [git](https://git-scm.com/downloads){:target="_blank"}.
- See the [Git Getting Started](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control){:target="_blank"} documentation.
- [Git Installation Guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git){:target="_blank"}
- [Git Initial Setup](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup){:target="_blank"}

## Python Basics

Finally, if you're completely new to Python, you might want to learn some basics before you begin with AoC.  Here's a list of some decent learning material to help you get started:

- [The Python Handbook](https://www.freecodecamp.org/news/the-python-handbook/){:target="_blank"}
- [The Official Python Tutorial](https://docs.python.org/3/tutorial/index.html){:target="_blank"}
- [The w3schools Python Tutorial](https://www.w3schools.com/python/default.asp){:target="_blank"}
- [Google's Python Class](https://developers.google.com/edu/python/){:target="_blank"}


