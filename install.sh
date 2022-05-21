#!/usr/bin/env bash

python3 setup.py install --optimize=1
cp nwg-icon-picker.svg /usr/share/pixmaps/
cp nwg-icon-picker.desktop /usr/share/applications/
