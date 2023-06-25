---
title: My AoC Template, Version 2

tags: 
  - name: My AoC Template
    link: /python/my-aoc-template
  - name: Logging
    link: /python/logging
  - name: Using Colours
    link: /python/colours
  - name: Reusable Code
    link: /python/reusable_code
---
Since I initially showed you my AoC template, we have:

- Created a reusable library of code that will be useful for solving AoC problems
- Established how to add colour to our logging

So let's update the template to make use of these things:

```python
"""
Author: Darren
Date: 01/12/2022

Solving https://adventofcode.com/2022/day/1

Solution overview:

"""
import logging
from pathlib import Path
import time
import common.type_defs as td

SCRIPT_NAME = Path(__file__).stem
SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")
OUTPUT_FILE = Path(SCRIPT_DIR, "output/output.png")

logger = logging.getLogger(SCRIPT_NAME)
logger.setLevel(logging.DEBUG)
logger.addHandler(td.stream_handler)

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    logger.debug(data)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %.3f seconds", t2 - t1)
```

If we run this template code, the output looks like this:

<img src="{{'/assets/images/template2-output.png' | relative_url }}" alt="Template output" width="420px" />
