---
title: Working with Images
main_img:
  name: RGB Image
  link: /assets/images/rgb_image.gif
tags: 
  - name: NumPy
    link: /python/numpy
  - name: Pillow
    link: https://pillow.readthedocs.io/en/stable/handbook/overview.html
  - name: Matplotlib
    link: https://matplotlib.org/
  - name: ImageIO
    link: https://imageio.readthedocs.io/en/stable/user_guide/index.html    

---
## Overview

Images can be described as a two dimensional grid of pixels, where each pixel has a particular colour.  For grayscale images, the pixels simply require intensity.  Consequently, a grayscale image can be represented as a two dimensional ndarray, with shape (x, y).
Whereas a colour image is typically represented as a two dimensional grid of pixels, plus three channels for each of R, G, B.  Consequently, an RGB image can be represented as an ndarray with shape (x, y, 3).

There are a few ways to work with images in Python. These include:

- **NumPy / Matplotlib**
  - Images are represented as ndarray objects: [x-size, y-size, colour channels]
  - When Matplotlib is working with images, the underlying format is the NumPy ndarray.
- **Pillow**
  - Extensive image format support and general image processing.
  - Capabilities include image processing, thumbnail creation, conversion between formats, point operations, animations, and image transformation.
- **ImageIO**
  - Useful package for reading and writing images.
  - Particularly useful for animations, and for capturing images from various sources and streams.

## Page Contents

- [Working with Different Imaging Libraries](#working-with-different-imaging-libraries)
  - [Loading and Showing Image File with Pillow](#loading-and-showing-image-file-with-pillow)
  - [Loading and Showing Image File with Matplotlib (NumPy)](#loading-and-showing-image-file-with-matplotlib-numpy)
  - [Converting from Pillow to NumPy](#converting-from-pillow-to-numpy)
  - [Converting from NumPy to Pillow](#converting-from-numpy-to-pillow)
  - [Converting from Matplotlib to BytesIO](#converting-from-matplotlib-to-bytesio)
  - [Converting from BytesIO to Pillow](#converting-from-bytesio-to-pillow)
  - [From Pillow to various formats, including BytesIO](#from-pillow-to-various-formats-including-bytesio)
  - [From BytesIO to Pillow](#from-bytesio-to-pillow)
  - [From BytesIO to Matplotlib](#from-bytesio-to-matplotlib)
  - [From BytesIO to ImageIO](#from-bytesio-to-imageio)
  - [From ImageIO to File, and File to Pillow](#from-imageio-to-file-and-file-to-pillow)

## Working with Different Imaging Libraries

The code below demonstrates how to read and write images with a few Python libraries, and how to convert between them.

First, some basic imports and prep...

```python
from os import path, mkdir
from io import BytesIO
import imageio as iio
from PIL import Image
from matplotlib import pyplot as plt, image as plt_img
import numpy as np

SCRIPT_DIR = path.abspath(path.curdir)
print(SCRIPT_DIR)
OUTPUT_DIR = path.join(SCRIPT_DIR, "output")
IMG_FILE = path.join(SCRIPT_DIR, "my_pic.jpg")

if not path.exists(OUTPUT_DIR):
    mkdir(OUTPUT_DIR)
```

### Loading and Showing Image File with Pillow

```python
print("Loading image with PIL...")
pil_image = Image.open(IMG_FILE)
print(f"Type: {type(pil_image)}")
print(f"Size: {pil_image.size}")
print(f"Format: {pil_image.format}")
print(f"Mode: {pil_image.mode}")
pil_image.show("Pillow Image")  # show the image
```

```
Loading image with PIL...
Type: <class 'PIL.JpegImagePlugin.JpegImageFile'>
Size: (400, 225)
Format: JPEG
Mode: RGB
```

### Loading and Showing Image File with Matplotlib (NumPy)

```python
print("\nLoading image with matplotlib...")
py_img = plt_img.imread(IMG_FILE)
print(f"Type: {type(py_img)}")
print(f"Dtype: {py_img.dtype}")
print(f"Shape: {py_img.shape}")
plt.axis("off")
plt.imshow(py_img)  # attach the image to the plot
plt.show()  # show the image
```

```text
Loading image with matplotlib...
Type: <class 'numpy.ndarray'>
Dtype: uint8
Shape: (225, 400, 3)
```

### Converting from Pillow to NumPy

```python
print("\nConverting from Pillow to NumPy ndarray...")
from_pillow_to_numpy = np.array(pil_image)
print(f"Type: {type(from_pillow_to_numpy)}")
print(f"Dtype: {from_pillow_to_numpy.dtype}")
print(f"Shape: {from_pillow_to_numpy.shape}")
plt.axis("off")
plt.imshow(from_pillow_to_numpy)
plt.show()
```

```text
Converting from Pillow to NumPy ndarray...
Type: <class 'numpy.ndarray'>
Dtype: uint8
Shape: (225, 400, 3)
```

### Converting from NumPy to Pillow

```python
print("\nConverting from NumPy ndarray to Pillow...")
from_numpy_to_pillow = Image.fromarray(py_img)
print(f"Type: {type(from_numpy_to_pillow)}")
print(f"Size: {from_numpy_to_pillow.size}")
print(f"Format: {from_numpy_to_pillow.format}")
print(f"Mode: {from_numpy_to_pillow.mode}")
from_numpy_to_pillow.show("From NumPy to Pillow")
```

```text
Converting from NumPy ndarray to Pillow...
Type: <class 'PIL.Image.Image'>
Size: (400, 225)
Format: None
Mode: RGB
```

### Converting from Matplotlib to BytesIO

```python
print(f"Source type: {type(py_img)}")
frame = BytesIO()
plt.imshow(py_img)  # load the image into Plt
plt.savefig(frame, format='png')  # save the image to (BytesIO) memory
plt.savefig(Path(OUTPUT_DIR, "pyplot_img_file.png"))  # save to disk
```

### Converting from BytesIO to Pillow

```python
print("\nReading BytesIO in Pillow...")
pil_img = Image.open(frame) # Pillow open seeks for us
pil_img.show()
```

### From Pillow to various formats, including BytesIO

```python
print("\nOpening image in Pillow and then saving in various formats to")
print(path.abspath(OUTPUT_DIR))
pil_img = Image.open(IMG_FILE)
pil_img.save(Path(OUTPUT_DIR, "pil_img_file.jpg"))
pil_img.save(Path(OUTPUT_DIR, "pil_img_file.png"))
print("And saving directly to BytesIO...")
frame = BytesIO()
pil_img.save(frame, format="PNG") # We can save to a file, or to a file-like object, like BytesIO
print("Success.")
```

### From BytesIO to Pillow

```python
print("\nOpening newly saved BytesIO in Pillow...")
pil_img = Image.open(frame) # Pillow open seeks for us
pil_img.show()
```

### From BytesIO to Matplotlib

```python
print("And reading the BytesIO back in using Pillow, and convert to Matplotlib...")
pil_img = Image.open(frame) # Pillow open seeks for us
plt_img = np.asarray(pil_image)
plt.imshow(plt_img)
plt.show()
```

### From BytesIO to ImageIO

```python
# From BytesIO into ImageIO
print("From BytesIO back into ImageIO...")
frame.seek(0)   # We need to seek back to 0
iio_img = iio.imread(frame)
```

### From ImageIO to File, and file to Pillow

```python
# And saving ImageIO to file
print("From ImageIO to file...")
iio.imsave(Path(OUTPUT_DIR, "iio_file.png"), iio_img)

# Let's read it back, to prove...
print("And from file to Pillow to show...")
pil_img = Image.open(Path(OUTPUT_DIR, "iio_file.png")) # Pillow open seeks for us
pil_img.show()
```