#!/bin/bash
cd "$(dirname "$0")"
shopt -s globstar
dos2unix **/*.py
chmod 644 **/*.py
chmod +x *.py
chmod -x setup.py
