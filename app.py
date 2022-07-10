import os
from flask import Flask, redirect, render_template
from svProjectFunctions import getResultForWeb

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Make sure API key is set
if not os.environ.get("Google_API_KEY"):
    raise RuntimeError("Google_API_KEY not set")

# open state data json in static file
with open('./static/states.json', 'r') as stateDataFile:
    stateDataStr = stateDataFile.read()

# print(stateDataStr)

gglapikey = os.environ.get("Google_API_KEY")

@app.route("/")
def index():
    # test panoID in Tibet
    # pano='CAoSLEFGMVFpcE0wR2NoekR0YlhCTVRxTFhZbUlCQXN6Z0NvSjhWcFZRalRLRmlV'
    rst = getResultForWeb()
    print(rst)
    # rst['state'] = 0
    return render_template("index.html", rst= rst, gglapikey=gglapikey)