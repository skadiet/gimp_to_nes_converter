# gimp_to_nes_converter
This repository contains the Python code to convert images drawn in GIMP (GNU Image Manipulation Program) to the NES (Nintendo Entertainment System) native format.

There are two different versions of the code.  One is the basic converter and the other is the advanced converter.  This code has only been tested using Python 3.8.5 on Linux.

To use either converter, make sure you follow the below steps while drawing your picture:
- Use GIMP to draw your picture.
- Set the image size to a width of 256 pixels and a height of 240 pixels.
- Export the picture in the "Raw image data (*.data)" format.

## Basic Converter
The basic converter assumes that you have drawn your picture using only red (ff0000), green (00ff00), and blue (0000ff) colors.  You will need to create your own palettes and attribute tables separately.

## Advanced Converter
The advanced converter assumes that you have imported the provided nes_palette.gpl file and are only using those colors.  It also assumes that you are manually keeping track of using only three distinct colors per 8x8 tile.
