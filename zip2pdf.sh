#!/bin/bash

CALL_DIR=$(PWD)

cd $(dirname $(readlink $0))

pipenv run python main.py $@

cd $CALL_DIR