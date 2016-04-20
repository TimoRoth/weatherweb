#!/bin/bash
cd "$(dirname "$0")"
shopt -s globstar
dos2unix **/*.{py,html}
chmod 644 **/*.py
chmod +x *.py
chmod -x setup.py
