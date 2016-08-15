#!/usr/bin/env python

import os, pymongo, json, bson, re
from bottle import Bottle, request

application = Bottle()
app = application

@app.route('/')
def index():
    return 'Welcome!'


