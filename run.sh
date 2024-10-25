#!/bin/sh

test -d venv || {
	echo "creating venv..."
	(set -x; python3 -m venv venv)
	echo "installing required packages..."
	(set -x; venv/bin/pip install -r requirements.txt)
}

venv/bin/python fetch.py
venv/bin/python visualize.py

open output.html
