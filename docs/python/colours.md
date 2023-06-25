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
  - name: Logging
    link: /python/logging
  - name: Extending clases
    link: python/classes#inheritance
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

Ealier, I showed you how to use the Python [logging](/python/logging) module, in order to customise the look of logging messages, to send messages to different outputs, and to set logging thresholds. We used this construct to set the formatting style for each message:

```python
stream_fmt = logging.Formatter(fmt='%(asctime)s.%(msecs)03d:%(name)s - %(levelname)s: %(message)s', 
                               datefmt='%H:%M:%S')
stream_handler.setFormatter(stream_fmt)
```

Here, I've extended the Python `Formatter` class, using a custom class that colours that output, based on the logging level.  It's not rocket science.  First, I override the `__init__()` method, so that we can decide if we want the messages to be coloured, and if we want the level name to be shortened.  They both default to `True`.  Then, I override the `format()` method, such that we wrap the record message with the necessary colour codes.

```python
""" Demonstrate coloured logging with custom Formatter """
import copy
import logging
from pathlib import Path
from colorama import Fore

class ColouredFormatter(logging.Formatter):
    """ Custom Formater which adds colour to output, based on logging level """
    
    def __init__(self, *args, apply_colour=True, shorten_lvl=True, **kwargs) -> None:
        """ Args:
            apply_colour (bool, optional): Apply colouring to messages. Defaults to True.
            shorten_lvl (bool, optional): Shorten level names to 3 chars. Defaults to True.
        """
        super().__init__(*args, **kwargs)
        self._apply_colour = apply_colour
        self._shorten_lvl = shorten_lvl
        
    level_mapping = {"DEBUG": (Fore.BLUE, "DBG"),
                  "INFO": (Fore.GREEN, "INF"),
                  "WARNING": (Fore.YELLOW, "WRN"),
                  "ERROR": (Fore.RED, "ERR"),
                  "CRITICAL": (Fore.MAGENTA, "CRT")
    }

    def format(self, record):
        if record.levelname in ColouredFormatter.level_mapping:
            new_rec = copy.copy(record)
            colour, new_level = ColouredFormatter.level_mapping[record.levelname]
            
            if self._shorten_lvl:
                new_rec.levelname = new_level
            
            if self._apply_colour:
                msg = colour + super().format(new_rec) + Fore.RESET
            else:
                msg = super().format(new_rec)
            
            return msg
        
        # If our logging message is not using one of these levels...
        return super().format(record)

def test():
    SCRIPT_DIR = Path(__file__).parent
    LOG_FILE = Path(SCRIPT_DIR, "my_file.log")

    # setup
    logger = logging.getLogger("FooBar-App")
    logger.setLevel(logging.DEBUG)

    # Write to console with threshold of INFO
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_fmt = ColouredFormatter(fmt='%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s: %(message)s', 
                                datefmt='%H:%M:%S')
    stream_handler.setFormatter(stream_fmt)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(LOG_FILE, mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(fmt="%(asctime)s.%(msecs)03d:%(name)s:%(levelname)8s: %(message)s", 
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

if __name__ == "__main__":
    test()
```

In the console, the output looks like this:

<img src="{{'/assets/images/coloured_console_ouput.png' | relative_url }}" alt="Coloured console output" width="540px" />

And our file output looks like this:

```text
08:32:47.521:FooBar-App:   DEBUG: Testing a debug line
08:32:47.522:FooBar-App:    INFO: My key is named foo, and its value is bar
08:32:47.522:FooBar-App: WARNING: Warning!
08:32:47.522:FooBar-App:   ERROR: Testing an error line
08:32:47.522:FooBar-App:CRITICAL: Ooops!
```

Note that for the `file_handler`, I've used `%(levelname)8s` to pad the level names to 8 characters.