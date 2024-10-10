#!/bin/bash

CALL_DIR=$(PWD)

PYTHON_DIR=$(dirname $(readlink $0))

cd $PYTHON_DIR

source myvenv/bin/activate

cd $CALL_DIR

python $PYTHON_DIR/main.py "$@"
