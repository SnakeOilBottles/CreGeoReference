#!/bin/sh
pip3 install ../CreGeoReference/
python -m unittest
pip3 uninstall -y CreGeoReference
##pip3 install CreGeoReference
