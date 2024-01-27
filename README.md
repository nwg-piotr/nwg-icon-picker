<img src="https://github.com/nwg-piotr/nwg-icon-picker/assets/20579136/c6d045d4-f671-4aaf-a1ff-4cadab79b62c" width="90" style="margin-right:10px" align=left alt="logo">
<H1>nwg-icon-picker</H1><br>

This application is a part of the [nwg-shell](https://nwg-piotr.github.io/nwg-shell) project.

I was looking for a GTK icon browser with a good textual search feature. It turned out to be easier to write one in 
200 [SLOC](https://en.wikipedia.org/wiki/Source_lines_of_code).

This program is intended to work as the icon picker for [nwg-panel](https://github.com/nwg-piotr/nwg-panel), 
but it may be used standalone. It displays a window to choose an icon with a textual search entry, and returns the icon 
name. You can also open a file from the search result in GIMP or Inkscape - if installed.

<img src="https://github.com/nwg-piotr/nwg-icon-picker/assets/20579136/0fae642c-0c78-4a67-b42f-949a30de5710" width=640 alt="Screenshot"><br>

## Installation

Find a package in your Linux distribution repsitories, if possibe.

[![Packaging status](https://repology.org/badge/vertical-allrepos/nwg-icon-picker.svg)](https://repology.org/project/nwg-icon-picker/versions)

Otherwise, you may install manually:

### Dependencies

- gtk3
- python (python3)
- python-gobject
- python-setuptools (make)

Clone this repository, and execute the `install.sh` script.
