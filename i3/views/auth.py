from flask import render_template, request, redirect, url_for, \
        flash, jsonify, session
import i3
import i3.auth
import i3.database
import i3.decorators
import i3.models

# User interface
def auth_login():
    if request.method == "POST":
        r = i3.auth.is_valid_login(
                request.form["username"],
                request.form["password"]
                )
        if r:
            session["username"] = r[0]
            session["uid"] = r[1]
            flash("Login successful.", "success")
            return redirect(url_for("news_read"))
        flash("Login failed!", "error")
    return render_template("auth/login.html")

def auth_logout():
    if "username" in session:
        session.pop("username")
        try: session.pop("uid")
        except: pass
        flash("Logged out.", "success")
        return redirect(url_for("news_read"))
    else:
        flash("You are already logged out!", "success")
        return redirect(url_for("auth_login"))

# API interface
def api_auth_login():
    success = False
    if i3.auth.is_valid_login(
            request.form["username"],
            request.form["password"]
            ):
        session["username"] = request.form["username"]
        success = True
    return jsonify(success=success, username=request.form["username"])

def api_auth_whoami():
    if "username" in session:
        return jsonify(loggedin=True, username=session["username"])
    return jsonify(loggedin=False, username="no-user")

def api_auth_logout():
    if "username" in session:
        session.pop("username")
    return jsonify(success=True)

