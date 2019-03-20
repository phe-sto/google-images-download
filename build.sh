#!/usr/bin/env bash
echo "########## BUILD DOCUMENTATION ##########"
make clean
make html
echo "########## BUILD DISTANT WHEEL ##########"
python3 setup.py bdist_wheel