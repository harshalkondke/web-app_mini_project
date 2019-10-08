from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# configure application
app = Flask(__name__)

# ensure template are auto-reload
app.config["TEMPLATES_AUTO_RELOAD"] = True

adminid = "admin"
adminpass = "adminpass"


# responses aren't from cached
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

# I used cs50 library to use sqlite database. because its easy
db = SQL("sqlite:///sdms.db")


@app.route('/')
@login_required
def index():
    return render_template("home.html")


@app.route('/std_display')
@login_required
def std_display():
    if request.method == "GET":
        seestudent = db.execute(
            "SELECT username, stdFname, stdLame, stdDiv, stdAge, D_name, D_location, P_name, P_guide, CGPA FROM student WHERE username = :user_id",
            user_id=session["user_id"])

        return render_template("display.html", seestudent=seestudent)


@app.route("/std_add", methods=["GET", "POST"])
@login_required
def std_add():
    # if form is already filled and need to be submitted
    if request.method == "POST":

        # Ensure First_name was submitted
        if not request.form.get("First_name"):
            return apology("must provide First Name", 403)

        # Ensure Last_name was submitted
        if not request.form.get("Last_name"):
            return apology("must provide Last Name", 403)

        # Ensure division was submitted
        if not request.form.get("std_div"):
            return apology("must provide Division", 403)

        # Ensure age was submitted
        if not request.form.get("std_age"):
            return apology("must provide your Age", 403)

        # Ensure Department name  was submitted
        if not request.form.get("dname"):
            return apology("must provide Department Name", 403)

        # Ensure Department Location was submitted
        if not request.form.get("dlocation"):
            return apology("must provide Department Location", 403)

        # Ensure project name was submitted
        if not request.form.get("pname"):
            return apology("must provide Project Name", 403)

        # Ensure Project Guide was submitted
        if not request.form.get("pguide"):
            return apology("must provide Project Guide", 403)

        # Ensure sem1 result was submitted
        if not request.form.get("r1st"):
            return apology("must provide Sem 1 result", 403)

        # Ensure sem2 result was submitted
        if not request.form.get("r2nd"):
            return apology("must provide sem 2 result", 403)

        # Ensure sem3 result was submitted
        if not request.form.get("r3rd"):
            return apology("must provide sem 3 result", 403)

        # inserted values into student table
        db.execute(
            "UPDATE student SET stdFname = :First_name, stdLame=:Last_name, stdDiv=:std_div, stdAge=:std_age, D_name=:dname, D_location=:dlocation, P_name=:pname, P_guide=:pguide, R_1st=:r1st, R_2nd=:r2nd, R_3rd=:r3rd, CGPA=:cgpa WHERE username = :user_id",
            First_name=request.form.get("First_name"),
            Last_name=request.form.get("Last_name"),
            std_div=request.form.get("std_div"),
            std_age=request.form.get("std_age"),
            dname=request.form.get("dname"),
            dlocation=request.form.get("dlocation"),
            pname=request.form.get("pname"),
            pguide=request.form.get("pguide"),
            r1st=request.form.get("r1st"),
            r2nd=request.form.get("r2nd"),
            r3rd=request.form.get("r3rd"),
            cgpa=request.form.get("cgpa"),
            user_id=session["user_id"])

        # Display a flash message
        flash("You are successfully added!")

        # Redirect user to home page
        return redirect(url_for("index"))

    # user reached via get to filled the form
    else:
        return render_template("add_std.html")


@app.route("/admin_delete", methods=["GET", "POST"])
@login_required_admin
def admin_delete():
    if request.method == "POST":
        db.execute("DELETE FROM student WHERE username = :deletestd",
                   deletestd=request.form.get("delete_username"))
        flash("You deleted student")
        return redirect(url_for("admin_delete"))
    else:
        return render_template("admin_delete.html")


@app.route("/std_delete", methods=["GET", "POST"])
@login_required
def std_delete():
    if request.method == "POST":
        db.execute("DELETE FROM student WHERE username = :username",
                   username=session["user_id"])
        flash("Your record deleted ")
        return redirect(url_for("std_display"))
    else:
        return render_template("delete.html")


@app.route("/admin_panel", methods=["GET", "POST"])
@login_required_admin
def admin_panel():
    return render_template("admin_home.html")


@app.route("/admin_display", methods=["GET", "POST"])
@login_required_admin
def admin_display():
    if request.method == "GET":
        seestudent = db.execute("SELECT * FROM student")

        return render_template("admin_display.html", seestudent=seestudent)


@app.route("/admin_add", methods=["GET", "POST"])
@login_required_admin
def admin_add():
    # if form is already filled and need to be submitted
    if request.method == "POST":

        # Ensure First_name was submitted
        if not request.form.get("First_name"):
            return apology("must provide First Name", 403)

        # Ensure Last_name was submitted
        if not request.form.get("Last_name"):
            return apology("must provide Last Name", 403)

        # Ensure division was submitted
        if not request.form.get("std_div"):
            return apology("must provide Division", 403)

        # Ensure age was submitted
        if not request.form.get("std_age"):
            return apology("must provide your Age", 403)

        # Ensure Department name  was submitted
        if not request.form.get("dname"):
            return apology("must provide Department Name", 403)

        # Ensure Department Location was submitted
        if not request.form.get("dlocation"):
            return apology("must provide Department Location", 403)

        # Ensure project name was submitted
        if not request.form.get("pname"):
            return apology("must provide Project Name", 403)

        # Ensure Project Guide was submitted
        if not request.form.get("pguide"):
            return apology("must provide Project Guide", 403)

        # Ensure sem1 result was submitted
        if not request.form.get("r1st"):
            return apology("must provide Sem 1 result", 403)

        # Ensure sem2 result was submitted
        if not request.form.get("r2nd"):
            return apology("must provide sem 2 result", 403)

        # Ensure sem3 result was submitted
        if not request.form.get("r3rd"):
            return apology("must provide sem 3 result", 403)

        # inserted values into student table
        db.execute(
            "INSERT INTO student (username, hash, stdFname, stdLame, stdDiv, stdAge, D_name, D_location, P_name, P_guide, R_1st, R_2nd, R_3rd, CGPA)"
            "VALUES (:username, :hash, :First_name, :Last_name, :std_div, :std_age, :dname, :dlocation, :pname, :pguide, :r1st, :r2nd, :r3rd, :cgpa)",
            First_name=request.form.get("First_name"),
            Last_name=request.form.get("Last_name"),
            std_div=request.form.get("std_div"),
            std_age=request.form.get("std_age"),
            dname=request.form.get("dname"),
            dlocation=request.form.get("dlocation"),
            pname=request.form.get("pname"),
            pguide=request.form.get("pguide"),
            r1st=request.form.get("r1st"),
            r2nd=request.form.get("r2nd"),
            r3rd=request.form.get("r3rd"),
            cgpa=request.form.get("cgpa"),
            username=request.form.get("username"),
            hash=generate_password_hash(request.form.get("password")))

        # Display a flash message
        flash("Student added successfully!")

        # Redirect user to home page
        return redirect(url_for("admin_panel"))

    # user reached via get to filled the form
    else:
        return render_template("admin_add.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget all current user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # check is user is admin
        if adminid == request.form.get("username"):
            if adminpass == request.form.get("password"):
                session["user_id"] = "admin"
                return redirect(url_for("admin_panel"))
            else:
                return apology("You are not admin", 401)

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM student WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["username"]

        # Redirect user to home page
        return redirect(url_for("index"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        
        elif (request.form.get("username") == "admin"):
            return apology("you are not admin", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password and confirmation match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # hash the password and insert a new user in the database
        hash = generate_password_hash(request.form.get("password"))
        new_user_id = db.execute("INSERT INTO student (username, hash) VALUES(:username, :hash)",
                                 username=request.form.get("username"),
                                 hash=hash)

        # unique username constraint violated?
        if not new_user_id:
            return apology("username taken", 400)

        # Remember which user has logged in
        session["user_id"] = new_user_id

        # Display a flash message
        flash("Registered!")

        # Redirect user to home page
        return redirect(url_for("logout"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow students to change her password"""

    if request.method == "POST":

        # Ensure current password is not empty
        if not request.form.get("current_password"):
            return apology("must provide current password", 400)

        rows = db.execute("SELECT hash FROM student WHERE username = :user_id", user_id=session["user_id"])

        # current password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("current_password")):
            return apology("invalid password", 400)

        # new password is not empty
        if not request.form.get("new_password"):
            return apology("must provide new password", 400)

        # new password confirmation is not empty
        elif not request.form.get("new_password_confirmation"):
            return apology("must provide new password confirmation", 400)

        # new password and confirmation match
        elif request.form.get("new_password") != request.form.get("new_password_confirmation"):
            return apology("new password and confirmation must match", 400)

        # Update database
        hash = generate_password_hash(request.form.get("new_password"))
        rows = db.execute("UPDATE student SET hash = :hash WHERE username = :user_id", user_id=session["user_id"],
                          hash=hash)

        # Show flash
        flash("Changed!")

    return render_template("change_password.html")


if __name__ == '__main__':
    app.run()
