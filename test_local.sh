#!/bin/sh

##pip3 install geocoder geopandas==0.9

# sudo docker container run  --rm --volume ./:/cre/python/CreGeoReference  --workdir /cre/python/CreGeoReference/ credocker/crepython:2020.0 /cre/python/CreGeoReference/test_local.sh


pip3 install ../CreGeoReference/

# if [ ! -f mysecrets.py ]; then
#   cp mysecrets.orig.py mysecrets.py
# fi

#python3 -m unittest
resultsFound=$(python3 -m unittest 2>&1)

pip3 uninstall -y CreGeoReference
##pip3 install CreGeoReference

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
