#!/bin/sh

export FLASK_APP=debug.py

ls .

flask run --host=0.0.0.0 #--reload
