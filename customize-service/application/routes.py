from flask import render_template, redirect, url_for, flash
from application import app
import json


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home_page.html')



