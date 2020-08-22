# import necessary programs
import os
import json
import numpy as np

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        user_id = session["user_id"]

        userExists = db.execute("SELECT * FROM user_info WHERE id = :id", id=user_id)

        if userExists:
            return redirect("/dashboard")
        else:
            return redirect("/edit")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))

        # unique username
        userExists = db.execute("SELECT username FROM users where username = :username", username=username)

        if userExists:
            return apology("Username already exists")

        # password matching
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match")

        # if all okay, register the new user
        else:
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=username, password=password)
            return redirect("/login")


# home
@app.route("/")
def index():
    return render_template("index.html")


# about page
@app.route("/about")
def about():
    return render_template("about.html")


# Dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    first = db.execute("SELECT first FROM user_info WHERE id = :id", id=user_id)[0]["first"]
    last = db.execute("SELECT last FROM user_info WHERE id = :id", id=user_id)[0]["last"]
    email = db.execute("SELECT email FROM user_info WHERE id = :id", id=user_id)[0]["email"]
    year = db.execute("SELECT year FROM user_info WHERE id = :id", id=user_id)[0]["year"]
    house = db.execute("SELECT house FROM user_info WHERE id = :id", id=user_id)[0]["house"]
    pronouns = db.execute("SELECT pronouns FROM user_info WHERE id = :id", id=user_id)[0]["pronouns"]
    courses = db.execute("SELECT dept, number, addinfo FROM courses WHERE id =:id", id=user_id)

    return render_template("dashboard.html", first=first, last=last, email=email,
                           year=year, house=house, pronouns=pronouns, courses=courses)


# edit profile
@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if request.method == "GET":
        return render_template("edit.html")
    else:
        user_id = session["user_id"]
        first = request.form.get("first").lower()
        last = request.form.get("last").lower()
        email = request.form.get("email").lower()
        year = request.form.get("year")
        house = request.form.get("house").lower()
        pronouns = request.form.get("pronouns").lower()

        # unique email
        emailExists = db.execute("SELECT email FROM user_info WHERE email = :email AND id != :id", email=email, id=user_id)
        if emailExists:
            return apology("Email already exists")

        # if all okay, input the new info
        idExists = db.execute("SELECT id FROM user_info WHERE id = :id", id=user_id)

        if idExists:
            db.execute("UPDATE user_info SET first = :first, last = :last, email = :email, year = :year, house = :house, pronouns = :pronouns WHERE id = :id",
                      first=first, last=last, email=email, year=year, house=house, pronouns=pronouns, id=user_id)
        else:
            db.execute("INSERT INTO user_info (id, first, last, email, year, house, pronouns) VALUES (:id, :first, :last, :email, :year, :house, :pronouns)",
                      id=user_id, first=first, last=last, email=email, year=year, house=house, pronouns=pronouns)

        return redirect("/dashboard")


@app.route("/availability", methods=["GET", "POST"])
@login_required
def availability():
    if request.method == "GET":
        user_id = session["user_id"]
        indices = [i for i in range(32)]
        times = ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00',
                '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
                '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00',
                '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30',
                '22:00', '22:30', '23:00', '23:30']
        ids = [[193 + i for i in range(32)], [1 + i for i in range(32)],
               [33 + i for i in range(32)], [65 + i for i in range(32)],
               [97 + i for i in range(32)], [129 + i for i in range(32)],
               [161 + i for i in range(32)]]

        # calls existing availabilities
        existing = db.execute("SELECT slot_id FROM availability WHERE id = :id", id=user_id)
        existing = [element["slot_id"] for element in existing]

        return render_template("availability.html", indices=indices, times=times, ids=ids, existing=existing)
    elif request.method == "POST":
        user_id = session["user_id"]
        slots = request.get_json()

        exists = db.execute("SELECT * FROM availability WHERE id = :id", id=user_id)
        # if no record yet, insert
        if not exists:
            for i in range(len(slots)):
                db.execute("INSERT INTO availability (id, slot_id) VALUES (:id, :slot_id)",
                           id=user_id, slot_id=slots[i])
        else:
            db.execute("DELETE FROM availability WHERE id = :id", id=user_id)
            for i in range(len(slots)):
                db.execute("INSERT INTO availability (id, slot_id) VALUES (:id, :slot_id)",
                           id=user_id, slot_id=slots[i])
        return redirect("/dashboard")


# add courses
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        user_id = session["user_id"]
        dept = request.form.get("dept").lower()
        number = request.form.get("number").lower()
        addinfo = request.form.get("addinfo").lower()

        # previously unlogged dept + number, assuming all inputs are correct
        alreadyEntered = db.execute("SELECT * FROM courses WHERE id = :id AND dept = :dept AND number = :number",
                                    id=user_id, dept=dept, number=number)
        if alreadyEntered:
            return redirect("/dashboard")
        else:
            db.execute("INSERT INTO courses (id, dept, addinfo, number) VALUES (:id, :dept, :addinfo, :number)",
                       id=user_id, dept=dept, addinfo=addinfo, number=number)
        return redirect("/dashboard")


# delete courses
@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    user_id = session["user_id"]

    if request.method == "GET":
        # establish courses logged by user
        userCourses = db.execute("SELECT * FROM courses WHERE id = :id", id=user_id)

        return render_template("delete.html", userCourses=userCourses)

    else:
        course = request.form.get("course").lower()

        if not course:
            return apology("must select course.")

        split = course.split()
        dept = split[0]
        number = split[1]

        db.execute("DELETE FROM courses WHERE id = :id AND dept = :dept AND number = :number",
                   id=user_id, dept=dept, number=number)

        return redirect("/dashboard")


# find partners
@app.route("/partners", methods=["GET", "POST"])
@login_required
def partners():
    user_id = session["user_id"]
    if request.method == "GET":
        # establish courses logged by user
        userCourses = db.execute("SELECT * FROM courses WHERE id = :id", id=user_id)
        return render_template("partners.html", userCourses=userCourses)
    else:
        course = request.form.get("course")

        if not course:
            return apology("must select course.")

        split = course.split()
        dept = split[0]
        number = split[1]

        # does not check for availability
        pairedUsers = db.execute("SELECT * FROM user_info JOIN courses ON user_info.id = courses.id JOIN availability on availability.id = user_info.id JOIN times ON times.slot_id = availability.slot_id WHERE dept = :dept AND number = :number AND courses.id != :id AND time IN(SELECT time FROM times JOIN availability ON times.slot_id = availability.slot_id WHERE id = :id)",
                                 dept=dept, number=number, id=user_id)
        if not pairedUsers:
            return apology("no mutual availabilities at this time")
        return render_template("pairs.html", split=split, pairedUsers=pairedUsers)


# delete account
@app.route("/deactivate", methods=["GET", "POST"])
@login_required
def deactivate():
    if request.method == "GET":
        return render_template("deactivate.html")

    else:
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        user_id = session["user_id"]
        db.execute("DELETE FROM user_info WHERE id = :id", id=user_id)
        db.execute("DELETE FROM courses WHERE id = :id", id=user_id)
        db.execute("DELETE FROM users WHERE id = :id", id=user_id)
        return redirect("/logout")


# change password
@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    if request.method == "GET":
        return render_template("password.html")
    else:
        user_id = session["user_id"]
        old = request.form.get("old")
        new = request.form.get("new")
        confirmation = request.form.get("confirmation")

        rows = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id=session["user_id"])

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], old):
            return apology("incorrect old password.")
        if new != confirmation:
            return apology("the passwords don't match.")

        # update new password
        hash = generate_password_hash(new)
        db.execute("UPDATE users SET hash = :hash WHERE id = :user_id", user_id=user_id, hash=hash)

        flash("password changed.")
        return redirect("/dashboard")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)