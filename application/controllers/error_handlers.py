from flask import Flask, request
from flask import render_template
from flask import current_app as app
from application.models import *

@app.errorhandler(404)
def not_found_error(e):
    return 'Page not found', 404