#!/bin/sh
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple CreGeoReference
python -m unittest
pip3 uninstall -y CreGeoReference
pip3 install CreGeoReference
