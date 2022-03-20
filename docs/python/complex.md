---
title: Complex Numbers
tags: 
  - name: Complex Numbers
    link: https://www.mathsisfun.com/numbers/complex-numbers.html
  - name: Complex Numbers in Python
    link: https://realpython.com/python-complex-numbers/
---
<script id="MathJax-script" async
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>

## Introduction

Complex numbers are a mathematic concept. They are the combination of a _real_ number (the kinds of numbers you're used to working with every day), and a so-called **_imaginary_** number. Imaginary numbers, when squared, return a negative result. And this is why they're _imaginary_!  With _real_ numbers, the result of any negative number multiplied by itself is always a positive number. And thus, it is impossible to have the square root of a negative number. And yet, this is the very definition of an _imaginary_ number. 

By convention, we say:

\\(\sqrt{-1} = j\\)

(Sometimes we use `i` instead of `j`.) 

Whereas, with real numbers \\( \sqrt{4} = 2 \\), with imaginary numbers:

$$
\begin{align}
\sqrt{-4} = 2j \\
\sqrt{-25} = 5j
\end{align}
$$

And so on.

And to conclude: **a complex number is the combination of a _real number_ and an _imaginary number_.** For example:

\\( 5 + 3j \\)

In fact, the _regular_ number 5 can be represented as a complex number! I.e. a regular number is a complex number that simply doesn't have an imaginary component. E.g.

\\( 5 + 0j \\)


## So What?

Well, this mathematical definition is all well and good. But why should you care? Well actually, for many practical applications of complex numbers in Python, you don't need to know about any of the stuff above. You just need to know that:

- Complex numbers are treated as _first class citizens_ in Python.  You don't **complex numbers are