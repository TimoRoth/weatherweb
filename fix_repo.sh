#!/bin/bash
cd "$(dirname "$0")"
shopt -s globstar
dos2unix **/*.{py,html,js}
chmod 644 **/*.{py,html,js}
chmod +x external_feeder/*.py
chmod -x external_feeder/pydl15.py
chmod +x *.py
chmod -x setup.py
