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

<img src="{{'/assets/images/term_colors.png' | relative_url }}" alt="Colorama" width="400px" />

## Logging with Colour

TBD.