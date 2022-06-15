import os
from flask import Flask, redirect, render_template

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Make sure API key is set
if not os.environ.get("Google_API_KEY"):
    raise RuntimeError("Google_API_KEY not set")

gglapikey = os.environ.get("Google_API_KEY")

@app.route("/")
def index():
    latval = 42.345573
    lngval = -71.098326
    return render_template("index.html", latval=latval, lngval=lngval, gglapikey=gglapikey)