import flask
from PIL import Image

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import random


# create an instance of Flask
app = Flask(__name__)
bootstrap = Bootstrap(app)


# route decorator binds a function to a URL
@app.route('/')
def hello():
    return render_template('index.html')
