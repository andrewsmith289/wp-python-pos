#!/bin/bash
# Removes the existing copy of the wp-api-python test package, and then
# installs the latest version from Github.

sudo rm -Rf src/
sudo pip install -e git+https://github.com/xxxxxxxxx/wp-api-python.git#egg=wordpress
