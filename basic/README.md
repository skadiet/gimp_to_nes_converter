# Basic Converter
The basic converter assumes that you have drawn your picture using only red (ff0000), green (00ff00), and blue (0000ff) colors.  You will need to create your own palettes and attribute tables separately.  These must be included in your main NESASM .asm file.

The code input is the raw image .data file.  
The code output is two separate files.  
- The first is a binary file called output.chr which contains all the unique tiles from your picture. 
- The second is an ASCII text file called output.i which contains an uncompressed representation of the data for your background image.

Both the .chr file and the .i file should be included in your main NESASM .asm file (example not included).

Use NESASM to compile your program with the output files, and your code should run!
