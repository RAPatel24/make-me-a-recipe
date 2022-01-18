from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud

from jinja2 import StrictUndefined
import json
import requests
import os
app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['API_KEY']
@app.route('/')
def homepage():
    """View homepage."""
    with open("data/recipes.json") as f:
        recipe_data = json.loads(f.read())
    
    return render_template('home.html', recipes = recipe_data, API_KEY = API_KEY)

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

@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""
    print("inside login")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")

@app.route("/recipes")
def showRecipes():
    """view recipes list"""
    
    return render_template('recipes.html')

@app.route("/recipe/<int:recipe_id>/<recipe_name>")
def showRecipe(recipe_id,recipe_name):
    """ view recipe """
    with open("data/recipes.json") as f:
        recipe_data = json.loads(f.read())
    
    recipe_id_list = []
    recipe = []
    for data in recipe_data:
        recipe_id_list.append(data['id'])
    
    if recipe_id in recipe_id_list:
        isExternal = False
        print("recipe is present in local db")
        for value in recipe_data:
            if value['id'] == recipe_id:
                recipe.append(value)
        
    else:
        isExternal = True
        url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?includeNutrition=false&apiKey={API_KEY}'
        req = requests.get(url)
        jsonData = req.json()
        recipe = jsonData
    
    return render_template('recipe.html', recipe=recipe, isExternal= isExternal)
   

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)