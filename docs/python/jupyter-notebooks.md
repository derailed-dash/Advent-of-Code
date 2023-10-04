---
title: Jupyter Notebooks
tags: 
  - name: Jupyter
    link: https://jupyter.org/
  - name: Jupyter Project Documentation
    link: https://docs.jupyter.org/en/latest/index.html
  - name: Jupyter Lab Documentation
    link: https://jupyterlab.readthedocs.io/en/stable/
  - name: Installing Jupyter
    link: https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html
  - name: Notebook Tips and Tricks
    link: https://www.dataquest.io/blog/jupyter-notebook-tips-tricks-shortcuts/
  - name: Anaconda
    link: https://learning.anaconda.cloud/get-started-with-anaconda?source=install
---
## Page Contents

- [What are Jupyter Notebooks?](#what-are-jupyter-notebooks)
- [A Few Benefits of Notebooks](#a-few-benefits-of-notebooks)
- [Ideal Scenarios for Using Notebooks](#ideal-scenarios-for-using-notebooks)
- [Installing](#installing)
- [You Can Also Run Jupyter Notebooks In the Cloud!](#you-can-also-run-jupyter-notebooks-in-the-cloud)

## What are Jupyter Notebooks?

In the realm of programming, the environment you choose to work in is the foundation that supports the structure of your code. Traditional Integrated Development Environments (IDEs) have been the go-to choice for developers seeking a dedicated space to write, test, and debug their code. However, as data science and machine learning began gaining traction, the need for a more interactive and data-centric environment became evident. Enter Jupyter Notebooks: a web-based application that has redefined the way we interact with code and data.

Unlike traditional IDEs, **Jupyter Notebooks allow for code, data, and multimedia to coexist in a shared space**. With its cell-based structure, users can write and execute code in small chunks, making it easier to test ideas and see results in real-time. This attribute alone sets it apart from the linear approach of traditional coding environments, making Jupyter Notebooks a beloved tool among data scientists and analysts.

## A Few Benefits of Notebooks

- **Interactive computing:** Real-time feedback on code execution, facilitating a more iterative and exploratory approach to problem-solving. Code is organised into _cells_. Cells can be executed and re-executed.  The output of those cells (such as the values assigned to variables) are available to all subsequent cells in the Notebook.  This is useful, since we can run a cell, and then experiment with changes to the cells that come _after_ the cell.
- **Documentation and sharing:** You have the ability to intertwine code, text, and multimedia. You can place markdown or HTML content alongside your code. This greatly improves your ability to document your solutions and share insights.  And you can structure your Notebook using chapters.
- **Images and visualisation**: You can include images and visualsations, alongside your code.
- **Reproducibility:** Encourages reproducible research by packaging code, data, and narrative into a single document.
- **Extension ecosystem:** A vast array of extensions and libraries are available, enhancing functionality and integration with other tools.
- **Run shell commands:** You can run shell commands from within the Notebook! This is useful for running file system commands, or - for example - to pre-install packages with `pip`.

Here's an example of a Notebook, with chapter structure, and with a markdown introduction:

![Notebook Example](/assets/images/notebook-md.png)

And here's an example, where we're dynamically generating an image with code, and showing it after the cell:

![Markdown, Cells, and Graphical Output](/assets/images/notebook-generating-image.png)

## Ideal Scenarios for Using Notebooks

- **Data Analysis and Visualization:** Whether it's cleaning data, performing statistical analysis, or creating visualizations, Jupyter Notebooks provide an interactive environment that fosters insight discovery.
- **Machine Learning and Model Development:** Building and testing models become streamlined with the ability to execute code incrementally and visualize results on the fly.
- **Educational Purposes:** An excellent tool for teaching coding and data science concepts, given its interactive nature and the ability to annotate code with rich text.
- **Collaborative Research:** Facilitates collaborative efforts by allowing multiple users to interact with the notebook and share their findings seamlessly.

## Installing

There are a few ways to install and run a Jupyter Notebook.

- As a standalone tool, using `pip`:\
  ```pip install notebook```
- As part of [Anaconda](https://learning.anaconda.cloud/get-started-with-anaconda?source=install){:target="_blank"}. _Ananconda_ is a bundled set of tools, packages and libraries for data science.
- As a Docker container. This is my preferred way to run Jupyter Notebooks.  It has the advantage that you can wrap Jupyter with a set of pre-installed packages and libraries, but it is isolated as a Docker container, so there's no risk of the install messing up your Python environment. If you're interested, I actually have my own [Miniconda Custom Image](https://github.com/derailed-dash/dazboconda){:target="_blank"}, which pre-installs a minimal set of data science packages.

## You Can Also Run Jupyter Notebooks In the Cloud!

You don't even need to run Jupyter Notebooks locally!  You can make use of a pre-configured cloud service. They are often free, unless you reach a point where you need more power (e.g. with GPUs) or features.

Options include:

[Anaconda Notebooks in the Cloud](https://nb.anaconda.cloud/){:target="_blank"}:

![Anaconda Cloud](/assets/images/anaconda_cloud.png)

[Google Collaboratory](https://colab.research.google.com/){:target="_blank"}

![Anaconda Cloud](/assets/images/collab.png)
