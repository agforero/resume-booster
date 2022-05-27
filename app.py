from flask import Flask
from bin import optimize_text as ot

app = Flask(__name__)

@app.route("/")
def main():
    o = ot.Optimizer_Demo()
    return f"<p>yes</p>"