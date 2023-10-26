#!/bin/bash
mkdir uploads
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask
python3 web_browser.py