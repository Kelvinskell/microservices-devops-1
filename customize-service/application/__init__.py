from flask import Flask
from flask import render_template

app = Flask(__name__)
from application import routes
