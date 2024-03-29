from functools import wraps

from flask import render_template, redirect, session

def error(message):
    print(message)
    return render_template('error.html', message = message)

def msg(message):
    print(message)
    return render_template('msg.html', message = message)

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function