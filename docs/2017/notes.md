# Using Jupyter Notebook

## In Google Colab

### Overview

- Launch https://colab.research.google.com/
- Name the Notebook
- Save
  - The file is saved in Google Drive.
  - But you can also save a copy in to your GitHub repo.
- How to share:
  - You can use a Colab link that points directly to a notebook file in Drive. E.g. if the notebook is yours and you want to edit on the-fly. E.g. `https://colab.research.google.com/drive/some_unique_id`
  - Or you can use a link that points to a notebook file in GitHub. E.g. if you have committed your notebook to GitHub, and now you want to share it to others. E.g. \
  [Open GitHub notebook in Colab](https://colab.research.google.com/github/derailed-dash/Advent-of-Code/blob/master/src/AoC_2017/Dazbo's_Advent_of_Code_2017.ipynb) \
  `https://colab.research.google.com/github/profile/repo/blob/master/path/to/some_notebook.ipynb`

### Challenges

- Colab doesn't natively support Jupyter Lab.
- Which means the development environment is not a swish and there's no GUI debugger.
- You can run JupyterLab from Colab, and then use soemthing like `ngrok` to expose it with a public URL.
  - But it still doesn't run a kernel that supports the visual debugger.

## In Anaconda Cloud

- This is a great cloud based Jupyter Lab solution.  But the free version doesn't offer much daily CPU, so it might not be enough.

## Locally

- The easiest way is to install Anaconda.
- Then you can run Jupyter Lab locally.
- To run a notebook in GitHub, clone the repo or download the notebook.  Then open it in your Jupyter Lab environment.
