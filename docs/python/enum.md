---
title: Enum

tags: 
  - name: Enum (GeeksforGeeks)
    link: https://www.geeksforgeeks.org/enum-in-python/
  - name: Enum (Real Python)
    link: https://realpython.com/python-enum/
  - name: Enum (Python Docs)
    link: https://docs.python.org/3/library/enum.html
---
## Page Contents


## Examples

```python
from enum import Enum

class ShapeType(Enum):
    HLINE =       {(0, 0), (1, 0), (2, 0), (3, 0)}
    PLUS =        {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)}
    BACKWARDS_L = {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)}
    I =           {(0, 0), (0, 1), (0, 2), (0, 3)}
    SQUARE =      {(0, 0), (1, 0), (0, 1), (1, 1)}    
```

