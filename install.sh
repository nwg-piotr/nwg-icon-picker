#!/usr/bin/env bash

python3 setup.py install --optimize=1
cp nwg-icon-picker.svg /usr/share/pixmaps/
cp nwg-icon-picker.desktop /usr/share/applications/

install -Dm 644 -t "/usr/share/licenses/nwg-icon-picker" LICENSE
install -Dm 644 -t "/usr/share/doc/nwg-icon-picker" README.md
