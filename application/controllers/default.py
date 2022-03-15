from flask import Flask, request
from flask import render_template
from flask import current_app as app
from application.models import *

@app.route('/')
def home_page():
    return 'This is home page'