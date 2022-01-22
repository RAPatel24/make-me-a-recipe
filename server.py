from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud
import helper
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
    user_id = helper.get_logged_in_user_id()
    user_email = helper.get_logged_in_user_email()
    loggedIn = helper.is_logged_in()

    recipe_id_list = helper.get_local_recipe_id_list()
    recipe_data = helper.get_local_recipe_data()

    saved_recipes = []
    if loggedIn:
        saved_recipe_id_list = crud.get_saved_recipe_by_id(user_id)
        for savedId in saved_recipe_id_list:
            if savedId in recipe_id_list:
                for recipe in recipe_data:
                    if recipe['id'] == savedId:
                        saved_recipes.append(recipe)
            else:
               url = f'https://api.spoonacular.com/recipes/{savedId}/information?includeNutrition=false&apiKey={API_KEY}'
               req = requests.get(url)
               jsonData = req.json()
               saved_recipes.append(jsonData)
    print(len(saved_recipes))
    return render_template('home.html', recipes=recipe_data, saved_recipes=saved_recipes, API_KEY=API_KEY, loggedIn = loggedIn)

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
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        session["user_id"] = user.id
        flash(f"Welcome back, {user.fname}!")

    return redirect('/')

@app.route("/logout")
def process_logout():
    """Log user out."""
    del session["user_email"]
    del session["user_id"]
    flash("Logged out.")
    return redirect('/')

@app.route("/recipes")
def showRecipes():
    """view recipes list"""
    
    return render_template('recipes.html')

@app.route("/recipe/<int:recipe_id>/<recipe_name>")
def showRecipe(recipe_id,recipe_name):
    """ view recipe """
    recipes = []
    recipe_id_list = helper.get_local_recipe_id_list()
    recipe_data = helper.get_local_recipe_data()
    loggedIn = helper.is_logged_in()
    
    if recipe_id in recipe_id_list:
        isExternal = False
        for value in recipe_data:
            if value['id'] == recipe_id:
                recipes.append(value)
    else:
        isExternal = True
        recipes = helper.get_recipes(recipe_id, API_KEY)
    ''' save recipe '''
    name = session.get('user_email')
    user_id = session.get('user_id')
    save = request.args.get('save')
    remove = request.args.get('remove')
    isRecipeSaved = crud.isRecipeSaved(user_id=user_id,recipe_id=recipe_id)
    if loggedIn and save:
        saveRecipe = crud.save_recipe(user_id,recipe_id)
        if saveRecipe:
            flash(f"Recipe - {recipe_name} is saved!")
    if loggedIn and remove:
        removeRecipe = crud.remove_recipe(user_id=user_id,recipe_id=recipe_id)
        if removeRecipe:
            flash(f"Recipe - {recipe_name} is removed!")
    isRecipeSaved = crud.isRecipeSaved(user_id=user_id,recipe_id=recipe_id)
    return render_template('recipe.html', recipes=recipes, isExternal= isExternal, isRecipeSaved = isRecipeSaved, loggedIn = loggedIn )

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0",port="5001",debug=True)