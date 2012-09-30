#! /bin/bash

export PYTHONPATH=$PYTHON_PATH:../dictlib:../netelib

$(dirname $0)/.virtualenv/bin/python main.py

