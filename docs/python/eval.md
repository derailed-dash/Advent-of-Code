---
title: Eval and Literal Eval

main_img:
  name: Danger, Will Robinson!
  link: /assets/images/dangerwillrobinson.jpg
tags: 
  - name: Eval
    link: https://realpython.com/python-eval-function/
---
## Page Contents

- [Eval](#eval)
- [Literal_Eval](#literal_eval)

## Eval

The Python built-in `eval()` function takes a string, and then executes that string as if it were a Python expression; i.e. as if it were a line of code.

Here are a couple of examples...

```python
print(eval("5 * 10"))
```

Output:

```text
50
```

```python
a = 2
b = 3
print(eval("a + b"))
```

Output:

```text
5
```

The real power here comes from the fact that we can read in external data, and then perform `eval()` on it.

But be careful...

Imagine you read in line from an external file that contained this line:

```text
__import__('os').listdir()
```

```python
print(eval(line))
```

When I run this right now, I get this output:

```text
['.AoC-env', '.env', '.git', '.gitattributes', '.github', '.gitignore', '.pylintrc', '.vscode', 'docs', 'LICENSE', 'README.md', 'requirements.txt', 'resources', 'src']
```

So, you can see that I've managed to execute functions from the `os` package.

What if this was my input data?

![Bad Eval!](/assets/images/bad_eval.png){:style="width: 480px"}

(I shamelessly stole that image from this [Reddit thread](https://www.reddit.com/r/adventofcode/comments/zkoc0o/2022_day_13_got_some_weird_input_today_hope_none/){:target="_blank"}.)
Can you see how bad this would be?

For this reason, `eval()` is considered **unsafe**.  Avoid it if you can, and only use it with input that you're sure of!  

## Literal_Eval

The `ast.literal_eval()` function is much safer!!  It is able to parse a string as if it were a Python type, such as an `int`, `list`, `dict`, etc.

Imagine if you needed to read in some external data that looks like Python data types, and you Python to treat the data as if it truly is a Python data type.  For example, this input:

```text
[1,[2,[3,[4,[5,6,7]]]],8,9]
```

You can read it in like this:

```python
import ast

data = "[1,[2,[3,[4,[5,6,7]]]],8,9]"
thing = ast.literal_eval(data)

print(thing)
print(type(thing))
```

The output:

```text
[1, [2, [3, [4, [5, 6, 7]]]], 8, 9]
<class 'list'>
```

Neat, right?

Take a look at [this program](/2022/13){:target="_blank"} for an example of how to make use of this.