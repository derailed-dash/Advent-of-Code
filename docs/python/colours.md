---
title: Colours

main_img:
  name: "Terminal Colours"
  link: /assets/images/term_colors.png
tags: 
  - name: Enum
    link: /python/enumerate
  - name: Colorama (PyPI)
    link: https://pypi.org/project/colorama/
---
## Page Contents

- [Creating Our Own Colours Class](#creating-our-own-colours-class)
- [Colorama](#colorama)
- [Logging with Colour](#logging-with-colour)

## Creating Our Own Colours Class

Sometimes we want to add a bit of colour to our terminal output. One way we can do this is by by using ANSI escape sequences. Here, I've created a `Colours` class by extending `Enum`:

```python
from enum import Enum

class Colours(Enum):
    """ ANSI escape sequences for coloured console output. E.g.
    print(Colours.GREEN.value + "str" + Colours.RESET.value).
    But actually, just use Colorama, which does this for you. 
    """
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    
print("Normal")
print(Colours.RED.value + "Some red text" + Colours.RESET.value)
print(Colours.BOLD.value + Colours.RED.value + "Some red text" + Colours.RESET.value)
print(Colours.CYAN.value + "Some red text")
print("... the previous colour was not reset." + Colours.RESET.value)
print("Finished")
```

The output looks like this:

<img src="{{'/assets/images/ansi-console-output.png' | relative_url }}" alt="ANSI colours" width="400px" />

## Colorama

But it turns out we don't need to create our own class, because there's already a package that does this for us: **Colorama**. First, we need to install it:

```bash
py -m pip install colorama
```

Here's a sample application:

```python
from colorama import Fore, Back, Style

print(Fore.RED + 'Red text')
print("Continuing")
print(Back.GREEN + 'red with a green background' + Style.RESET_ALL)
print('reset')
print(Fore.WHITE + Back.GREEN + 'white with a green background' + Style.RESET_ALL)
print(Fore.WHITE + Back.BLACK + 'white with a black background' + Style.RESET_ALL)
print(Style.BRIGHT + Fore.WHITE + Back.BLACK + 'bold white with a black background' + Style.RESET_ALL)
print(Style.BRIGHT + Fore.WHITE + Back.GREEN + 'bold white with a green background' + Style.RESET_ALL)
```

The output looks like this:

<img src="{{'/assets/images/term_colors.png' | relative_url }}" alt="Colorama" width="320px" />

## Logging with Colour

TBD.

```python
import logging
from pathlib import Path
from colorama import Fore

colors = {"DEBUG": Fore.BLUE,
          "INFO": Fore.GREEN,
          "WARNING": Fore.YELLOW,
          "ERROR": Fore.RED,
          "CRITICAL": Fore.MAGENTA} 

class ColouredFormatter(logging.Formatter):
    """ Custom Formater which adds colour to output, based on logging level """
    def format(self, record): 
        msg = logging.Formatter.format(self, record) 
        if record.levelname in colors: 
            msg = colors[record.levelname] + msg + Fore.RESET 
        return msg

SCRIPT_DIR = Path(__file__).parent
LOG_FILE = Path(SCRIPT_DIR, "my_file.log")

# setup
logger = logging.getLogger("FooBar-App")
logger.setLevel(logging.DEBUG)

# Write to console with threshold of INFO
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_fmt = ColouredFormatter(fmt='%(asctime)s.%(msecs)03d:%(name)s - %(levelname)s: %(message)s', 
                               datefmt='%H:%M:%S')
stream_handler.setFormatter(stream_fmt)
logger.addHandler(stream_handler)

file_handler = logging.FileHandler(LOG_FILE, mode='a')
file_handler.setLevel(logging.DEBUG)
file_fmt = logging.Formatter(fmt="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                             datefmt='%H:%M:%S')
file_handler.setFormatter(file_fmt)
logger.addHandler(file_handler)

my_key = "foo"
my_val = "bar"
logger.debug("Testing a debug line")
logger.info("My key is named %s, and its value is %s", my_key, my_val)
logger.warning("Warning!")
logger.error("Testing an error line")
logger.critical("Ooops!")
```
