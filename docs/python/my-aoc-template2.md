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
Date: 01/12/2023

Solving https://adventofcode.com/2023/day/1

Part 1:

Part 2:

"""
import logging
import time
import common.type_defs as td

locations = td.get_locations(__file__)
logger = td.retrieve_console_logger(locations.script_name)
logger.setLevel(logging.DEBUG)
# td.setup_file_logging(logger, locations.output_dir)

def main():
    with open(locations.sample_input_file, mode="rt") as f:
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
