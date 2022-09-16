#!/bin/sh

set -e

python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
uvicorn main:app --reload 
