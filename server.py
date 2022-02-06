from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db
import crud,helper,json,os,requests
from jinja2 import StrictUndefined
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
API_KEY = os.environ['API_KEY']
TWILIO_KEY = os.environ['TWILIO_KEY']

@app.route('/')
def homepage():
    """View homepage."""
    user_id = session.get("user_id")
    user_email = session.get("user_email")
    loggedIn = helper.is_logged_in()
    recipe_data = helper.get_local_recipe_data()

    get_exclude_ingredient_list = []
    if loggedIn:
        get_exclude_ingredient_list = crud.get_excluded_ingredient(user_id)

    intolerences = ["egg","peanut","milk","shellfish","walnut","cashew","wheat","soy","sesame"]

    return render_template('home.html', exclude_list = get_exclude_ingredient_list, intolerences=intolerences, recipes=[], search_string=[], recipes_local=recipe_data, API_KEY=API_KEY, loggedIn = loggedIn)

@app.route('/', methods=["POST"])
def home():
    """View homepage."""
    user_id = session.get("user_id")
    user_email = session.get("user_email")
    loggedIn = helper.is_logged_in()
    recipe_data = helper.get_local_recipe_data()
    ingredients = request.form.get('search-box')
    exclude_ingredients_list = []
    intolerences = ["egg","peanut","milk","shellfish","walnut","cashew","wheat","soy","sesame"]
    for item in intolerences:
        if request.form.get(item) is not None:
            exclude_ingredients_list.append(request.form.get(item))
    recipes = []
    url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=40&apiKey={API_KEY}'
    results = requests.get(url)
    json_data = results.json()
    for recipe in json_data:
        missedIngredients = []
        for ingredient in recipe['missedIngredients']:
            missedIngredients.append(ingredient['name'])
        if not excluded_ingredient_present(missedIngredients, exclude_ingredients_list):
            recipes.append(recipe)
        
    get_exclude_ingredient_list = []
    if loggedIn:
        get_exclude_ingredient_list = crud.get_excluded_ingredient(user_id)
    search_string = []
    search_string.append(ingredients)
    search_string.append(exclude_ingredients_list)
    
    return render_template('home.html', exclude_list=get_exclude_ingredient_list, intolerences=intolerences, search_string = search_string, recipes=recipes, recipes_local=recipe_data, API_KEY=API_KEY, loggedIn = loggedIn)

def excluded_ingredient_present(missedIngredients, exclude_ingredients_list):
    for excluded in exclude_ingredients_list:
       for missed in missedIngredients:
           if excluded in missed:
               return True
    return False

@app.route('/favorites')
def show_favorites():
    """ View saved recipe page """
    saved_recipes = []
    user_id = session.get("user_id")
    saved_recipe_id_list = crud.get_saved_recipe_by_id(user_id)
    for savedId in saved_recipe_id_list:
        url = f'https://api.spoonacular.com/recipes/{savedId}/information?includeNutrition=false&apiKey={API_KEY}'
        req = requests.get(url)
        jsonData = req.json()
        saved_recipes.append(jsonData)
    return render_template('favorites.html', saved_recipes=saved_recipes, API_KEY=API_KEY)

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
    confirmpassword = request.form.get("confirm-password")
    #exclude = request.form.get("exclude")
    exclude_ingredients_list = []
    if request.form.get('Milk') is not None:
        exclude_ingredients_list.append(request.form.get('Milk'))
    if request.form.get('Egg') is not None:
        exclude_ingredients_list.append(request.form.get('Egg'))
    if request.form.get('Peanut') is not None:
        exclude_ingredients_list.append(request.form.get('Peanut'))
    if request.form.get('Walnut') is not None:
        exclude_ingredients_list.append(request.form.get('Walnut'))
    if request.form.get('Cashew') is not None:
        exclude_ingredients_list.append(request.form.get('Cashew'))
    if request.form.get('Shellfish') is not None:
        exclude_ingredients_list.append(request.form.get('Shellfish'))
    if request.form.get('Wheat') is not None:
        exclude_ingredients_list.append(request.form.get('Wheat'))
    if request.form.get('Soy') is not None:
        exclude_ingredients_list.append(request.form.get('Soy'))
    if request.form.get('Sesame') is not None:
        exclude_ingredients_list.append(request.form.get('Sesame'))
    print(f'exclude list: {exclude_ingredients_list}')
    user = crud.get_user_by_email(email)
    
    if user:
        flash("Cannot create an account with that email. Try again.")
    
    else:
        if password == confirmpassword:
            crud.create_user(fname, lname, email, password)
            if exclude_ingredients_list:
                user_id = crud.get_user_id_by_email(email)
                if user_id:
                    crud.save_ingredient_to_exclude(user_id, exclude_ingredients_list)
            flash("Account created! Please log in.")
        else:
            flash("Password and confirm password are not same, please try again!")
            return render_template('signup.html')

    return redirect('/')
    

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
        flash(f"Welcome, {user.fname}!")

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
    recipe = []
    loggedIn = helper.is_logged_in()
    user_id = session.get('user_id')
    recipe = crud.get_recipe(recipe_id, API_KEY)

    """ save recipe """
    save = request.args.get('save')
    remove = request.args.get('remove')

    isRecipeSaved = crud.isRecipeSaved(user_id=user_id,recipe_id=recipe_id)
    print(f'before - recipe is saved: {isRecipeSaved}')

    if loggedIn and save:
        saveRecipe = crud.save_recipe(user_id,recipe_id)
        if saveRecipe:
            flash(f"Recipe - {recipe_name} is saved!")

    isRecipeSaved = crud.isRecipeSaved(user_id=user_id,recipe_id=recipe_id)
    print(f'after - if recipe is saved: {isRecipeSaved}')

    if save and user_id == None:
        return redirect('/signup')

    """ remove recipe """
    if loggedIn and remove:
        removeRecipe = crud.remove_recipe(user_id=user_id,recipe_id=recipe_id)
        if removeRecipe:
            flash(f"Recipe - {recipe_name} is removed!")
    isRecipeSaved = crud.isRecipeSaved(user_id=user_id,recipe_id=recipe_id)

    ''' add review '''
    review = request.args.get('review')
    rating = request.args.get('rating')
    if review and rating:
        test_review = crud.add_review(user_id=user_id, recipe_id=recipe_id, review=review, rating=rating)

    return render_template('recipe.html', recipe=recipe, isRecipeSaved = isRecipeSaved, loggedIn = loggedIn)

@app.route("/recipes",methods=["POST"])
def getRecipesByKeyword():
    keyword = request.args.get('keyword')
    url = ""
    if keyword:
        recipe = request.form.get("recipe")
        diet = request.form.get("Diet")
        if diet != "Diet":
            url = f'https://api.spoonacular.com/recipes/complexSearch?query={recipe}&diet={diet}&number=40&apiKey={API_KEY}'
        else:
            url = f'https://api.spoonacular.com/recipes/complexSearch?query={recipe}&number=40&apiKey={API_KEY}'
    else:
        cuisine = request.form.get("cuisine")
        mealtype = request.form.get("type")
        diet = request.form.get("Diet")
        url = f'https://api.spoonacular.com/recipes/complexSearch?cuisine={cuisine}&diet={diet}&type={mealtype}&number=40&apiKey={API_KEY}'

    result = requests.get(url)
    jsonData = result.json()
    return render_template('recipes.html', recipes=jsonData, API_KEY=API_KEY)

@app.route('/review')
def show_reviews():
    """Show reviews."""

    return render_template('review.html')

@app.route("/reviews/<int:recipe_id>")
def reviews(recipe_id):
    results = crud.get_review(recipe_id)
    return jsonify(results)

@app.route("/reviewcount/<int:recipe_id>")
def review_count(recipe_id):
    results = crud.get_reviews_total(recipe_id)
    return jsonify(results)

@app.route("/email")
def send_email():
    email = request.args.get('email')
    recipe_id = request.args.get('recipe_id')
    recipe_title = request.args.get('recipe_title')
    recipe = crud.get_recipe(recipe_id, API_KEY)
    recipe_url = f'http://localhost:5001/recipe/{recipe_id}/{recipe_title}'
    image_url = ""
    
    for value in recipe:
        image_url = value['imageUrl']

    message = Mail(
        from_email='rapatel765@gmail.com',
        to_emails=email,
        subject=f'Make Me A Recipe - {recipe_title}',
        html_content = f'<strong>{recipe_title}</strong><div><img src="{ image_url }" /></div><strong><a href="{recipe_url}">Click here to find full recipe</a></strong><p>Regards,<strong>Team Make me a recipe</strong></p>')
    sg = SendGridAPIClient(TWILIO_KEY)
    response = sg.send(message)
    results = {'status_code': response.status_code, 'response_body': response.body}
    
    return jsonify(results['status_code'])

@app.route("/<category>")
def getRecipesByCategory(category):
    url = f'https://api.spoonacular.com/recipes/complexSearch?query={category}&number=10&apiKey={API_KEY}'
    result = requests.get(url)
    jsonData = result.json()
    return render_template('recipes.html', recipes=jsonData, API_KEY=API_KEY)

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0",port="5001",debug=True)