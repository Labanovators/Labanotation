#!/bin/bash
mkdir uploads
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install Flask
pip install opencv-python
pip install numpy