import os
import json
from flask import Flask, redirect, render_template, request
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash


from svProjectFunctions import getResultForWeb
from userFunctions import error

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# Make sure API key is set
if not os.environ.get("Google_API_KEY"):
    raise RuntimeError("Google_API_KEY not set")
gglapikey = os.environ.get("Google_API_KEY")

# open state data json in static file
with open('./static/states.json', 'r') as stateDataFile:
    stateDataStr = stateDataFile.read()

# print(stateDataStr)


@app.route("/")
def index():
    statearg = request.args.get("state")
    print(statearg)
    # test panoID in Tibet
    # pano='CAoSLEFGMVFpcE0wR2NoekR0YlhCTVRxTFhZbUlCQXN6Z0NvSjhWcFZRalRLRmlV'


    if statearg == None:
        rst = getResultForWeb()
    else:
        rst = getResultForWeb(state = statearg)

    print(rst)
    # rst['state'] = 0
    return render_template("index.html", rst= rst, gglapikey=gglapikey)

@app.route('/stateslist')
def stateslist():
    # load the states data with street view
    with open('./static/states.json', 'r') as statesDataFile:
        statesDataStr = statesDataFile.read()
    stateslist = json.loads(statesDataStr)
    return render_template("stateslist.html", stateslist = stateslist)

# @app.route('/error')
# def errorPage():
#     return error('test msg')

