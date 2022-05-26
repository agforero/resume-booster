from flask import Flask
from src import optimize_text as ot

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"