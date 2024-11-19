from flask import Flask # type: ignore
from flask_pymongo import PyMongo # type: ignore
from config import Config
from flask_cors import CORS 
import os
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

mongo = PyMongo(app)

@app.route("/")
def index():
    return "Hello, World!"

from controllers.user_controller import *
from controllers.doctor_controller import *

if __name__ == '__main__':
    app.run(debug=True)