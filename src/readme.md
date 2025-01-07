# Welcome to the source for my Advent of Code Solutions

If you'd like to peruse this code along with my solution walkthroughs, then take a look [here](https://derailed-dash.github.io/Advent-of-Code/).

## Setting Up Your Environment

With Conda:

```bash
conda env list # see environments and current active env

export AOC_ENV="aoc-conda-env"

# Create and activate an environment
conda create --name $AOC_ENV
conda activate $AOC_ENV

# Install some core packages
# Before trying to run any Python code or Jupyter cells in this env
conda install -y -c conda-forge python jupyter jupyterlab

# Additional packages - or we could install these from (say) a Jupyter notebook
conda install pandas hvplot mathjax matplotlib networkx numpy plotly scipy

# Export the current environment config - for source control
conda env export > $AOC_ENV.yml
```
