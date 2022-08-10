---
title: Working with Binary and Other Bases
tags: 
  - name: binary and hexadecimal
    link: https://www.mathsisfun.com/binary-decimal-hexadecimal.html
  - name: String format
    link: https://www.programiz.com/python-programming/methods/string/format
---

If you're not familiar with binary, hexadecimal, and bases in general, then I'd suggest you first checkout [this friendly page](https://www.mathsisfun.com/binary-decimal-hexadecimal.html){:target="_blank"}.

## Page Contents

- [Converting Decimal to Other Bases](#converting-decimal-to-other-bases)
- [Converting Any Base to Decimal](#converting-any-base-to-decimal)
- [Converting from Hex to Binary](#converting-from-hex-to-binary)
- [Bit Operations](#bit-operations)

## Converting Decimal to Other Bases

```python
a_num = 20

bin_as_str = bin(20)
print(f"bin_as_str: {bin_as_str}")
print(f"bin component: {bin_as_str[2:]}")

oct_as_str = oct(20)
print(f"bin_as_str: {oct_as_str}")
print(f"bin component: {oct_as_str[2:]}")

hex_as_str = hex(20)
print(f"bin_as_str: {hex_as_str}")
print(f"bin component: {hex_as_str[2:]}")
```

Output:

```text
bin_as_str: 0b10100
bin component: 10100
bin_as_str: 0o24
bin component: 24
bin_as_str: 0x14
bin component: 14
```

## Converting Any Base to Decimal

```python
# bin to dec
print(int("01101001", 2))
print(int("0b01101001", 2))

# hex to dec
print(int("ff", 16))
```

Output:

```text
105
105
255
```

## Converting from Hex to Binary

```python
hex_str = "7bff9"

# To get bin value without leading zeroes, just convert from hex to dec - with int(),
# and then from dec to bin - with bin()
bin_val = bin(int(hex_str, 16))
print(bin_val)

# And now using the 'b' format specifier to go from dec to bin with leading zeroes
bin_len = 4*len(hex_str)
bin_val = "{0:0{width}b}".format(int(hex_str, 16), width=bin_len)
print(bin_val)
```

The first conversion is just using the int() and bin() functions that we've already seen.

The second conversion:

- First converts from hex to decimal, using `int(value, base)`, where `base=16`.
- Then converts the decimal number to binary, by applying a `format spec`, where:
  - The first `{0}` is the first parameter to the `format()` method, i.e. the decimal value;
  - And `:0{width}b` tells `format()` to convert to `binary` type, and then pad with `0` in order to achieve the desired overall length.

In general, when using a _format spec_, the format is:

```
{fill}{align}{width}{type}
```

Output:

```text
0b1111011111111111001
01111011111111111001
```

## Bit Operations

|Operation|Operator|Example|
|---------|--------|-------|
|Bit shift left y places|x << y|E.g. 0b110 < 2 = 0b11000|
|Bit shift right y places|x >> y|E.g. 0b11000 >> 3 = 0b11|
|Bitwise AND|x & y|1 only if both are 1|
|Bitwise OR|x \| y|1 if either is 1|
|Complement / NOT|~x|
|Exclusive OR (XOR)|x ^ y|1 where one or other, but not both