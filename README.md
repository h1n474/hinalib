# hinalib

Tools used at work and more

## Paths

Path extension to make it easier to process files in pathlib.

```python
# Get the image files on the desktop.
p = hinalib.Paths('~/Desktop')
files = p.files('jpg','tif')
files.items #
```

## Exiftool
A wrapper for the command line exiftool

## Framed

Treat image files as if they were framed.

```python
from utils.position import TitlePosition
im = hinalib.Framed('/User/hnt/Desktop/hoge.jpg')
im.add_paper(aspect=1.24).add_tile("my hoge pic", TitlePosition.center)
im.save('hoge.jpg', overwrite=True)
```

## command line tools

1. `cs` -- Fast contact sheet. Automatically determines the height and width.
1. `mz` -- Fast zip file. ignore dotfile.   