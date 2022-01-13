from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""
    
    return render_template('home.html')

@app.route('/login')
def loginpage():
    """View login page """
    return render_template('login.html')

@app.route('/signup')
def signuppage():
    """View login page """
    return render_template('signup.html')

@app.route("/signup", methods=["POST"])
def register_user():
    """Create a new user."""
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        crud.create_user(fname, lname, email, password)
        flash("Account created! Please log in.")

    return redirect("/")

@app.route("/recipes")
def showRecipes():
    """search for recipes"""
    
    return render_template('recipes.html')

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)