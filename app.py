import os
import json
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash


from svProjectFunctions import getResultForWeb
from userFunctions import error, login_required, msg

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

    # to get simple state information of the location istead of options of the index page
    for option in rst['state']:
        if option[1]:
            stateLog = option[0]
    rst['stateLog'] = stateLog
        
    # add log in history in database if user logged
    
    if not session.get("user_id") is None:
        db.execute("INSERT INTO history (user_id, lat, lon, state, pano) VALUES (?,?,?,?,?);",session["user_id"], round(float(rst['lat']),6), round(float(rst['lon']),6), stateLog, rst['panoId'] )
    # else:
        # print('unlogged')
    # rst['state'] = 0

    # test a location in antarctica
    # rst = {'panoId': '9yxJ1_HXapBWpxbb24x5_Q', 'lat': -77.88874642391032, 'lon': 160.5823942629601, 'hemi': 'South', 'continent': 'Antarctica', 'state': [['Antarctica', True]], 'division': 2}
    print(rst)

    return render_template("index.html", rst= rst, gglapikey=gglapikey)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("must provide username")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username does not exist
        if len(rows) != 0:
            return error("the username already exists")

        # Ensure password was submitted
        if not request.form.get("password"):
            return error("must provide password")

        # Ensure confirmation was submitted
        if not request.form.get("confirmation"):
            return error("must confirm password")

        # check the password and the confirmation
        if not request.form.get("password") == request.form.get("confirmation"):
            return error("password don't match")

        password_hash = generate_password_hash(request.form.get("password"))
        username = request.form.get("username")

        # print(f"INSERT INTO users (username, hash) VALUES ('{username}', '{password_hash}');")
        id_inserted = db.execute("INSERT INTO users (username, hash) VALUES (? ,?);", username, password_hash)

        session["user_id"] = id_inserted

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("must provide the username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide the password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@login_required
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@login_required
@app.route("/changepasswords", methods=["GET", "POST"])
def changepasswords():
    """change passwords"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("oldpassword"):
            return error("Please enter the current password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = ?", session['user_id'])

        # Ensure password is correct
        if not check_password_hash(rows[0]["hash"], request.form.get("oldpassword")):
            return error("Wrong Password")

        # Ensure new password was submitted
        if not request.form.get("newpassword"):
            return error("must provide new password")

        # Ensure new password was submitted
        if not request.form.get("confirmation"):
            return error("please re-enter new password")

        # Ensure password check
        if not request.form.get("newpassword") == request.form.get("confirmation"):
            return error("passwords do not match")

        new_password_hash = generate_password_hash(request.form.get("newpassword"))

        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_password_hash, session["user_id"])

        return msg("Change the Passwords Successfully")

    # # User reached route via GET (as by clicking a link or via redirect)
    return render_template("changepasswords.html")

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

@login_required
@app.route('/history')
def history():

    history = db.execute("SELECT timestamp, lat, lon, state, pano FROM history WHERE user_id = ?", session["user_id"])

    print(history)
    # history = "test history msg"

    return render_template("history.html", history = history)

@login_required
@app.route('/favourites')
def favourites():
    userId = session["user_id"]
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    state = request.args.get('state')
    pano = request.args.get('pano')
    #print(args==None)
    # print(userId)
    # print(lat)
    # print(lon)
    # print(state)
    # print(pano)
    if state != None:
        db.execute("INSERT INTO favourite (user_id, lat, lon, state, pano) VALUES (?,?,?,?,?);",userId, round(float(lat),6), round(float(lon),6), state, pano)
    
    favourite = db.execute("SELECT lat, lon, state, pano FROM favourite WHERE user_id = ?", userId)
    
    return render_template('favourites.html', favourites=favourite)