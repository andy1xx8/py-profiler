#!/bin/sh

rm -rf ./build && rm -rf dist && rm -rf src/py_profiler.egg-info
python3 -m build && python3 -m twine upload dist/*

rm -rf src/py_profiler.egg-info
rm -rf ./build

