---
title: My AoC Template
---
I like to start each AoC challenge using this template file. It brings together everything we've covered in the [Python Journey]({{'/python' | relative_url }}) so far.

```python
"""
Author: Darren
Date: 01/12/2021

Solving https://adventofcode.com/2021/day/1

Solution overview:

"""
from pathlib import Path
import logging
import time

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/sample_input.txt")
# INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        data = f.read().splitlines()
        
    logger.debug(data)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
```

A couple of things I haven't discussed so far:

- I'm using a _docstring_ block at the top of each program, as a way to docuemnt the code. The module _docstring_ should go at the very top of the file, and should always be enclosed by triple-quotes.
- I put all the main code inside a function called `main()`. To define a function, we just use the `def` keyword.
- When the program is launched, I test whether the file being executed (e.g. `my_prog.py`) is being executed as a standalone script, or whether it has been imported into another script.  Well, it is generally being executed as a standalone script, which causes the script's  `__name__` to evaluate to `__main__`.  As a result, we know that the following statement evaluates to True: \
`if __name__ == "__main__"`  
- This causes the program to run the `main()` function. We've wrapped the `main()` function with `time.perf_counter()` calls, so that we can finally print the overall time taken by the script to execute.