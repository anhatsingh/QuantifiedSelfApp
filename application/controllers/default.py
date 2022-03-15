from flask import Flask, request
from flask import render_template
from flask import current_app as app
from flask_security import login_required
from application.models import *

@app.route('/')
@login_required
def home_page():
    return render_template('home.html')