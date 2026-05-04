#!/bin/sh
python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple CreGeoReference

#python -m unittest
resultsFound=$(python3 -m unittest 2>&1)

pip3 uninstall -y CreGeoReference
pip3 install CreGeoReference

hasError=$(echo $resultsFound | grep -c 'ERROR\|FAIL')
if [ $hasError -eq 0 ]; then
    echo $resultsFound
    echo "[SUCCESS]: unittests succeeded!"
    exit 0
else
    echo $resultsFound
    echo "[FAIL]: Errors in unittests!"
    #echo $resultsFound | grep 'ERROR\|FAIL'
    exit 1
fi
