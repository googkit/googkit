#!/bin/bash

DEPSWRITER=closure/library/closure/bin/build/depswriter.py

cd $(dirname $0)/..
python $DEPSWRITER --root_with_prefix="debug/js_dev ../../../../debug/js_dev" --output_file="debug/js_dev/deps.js"
