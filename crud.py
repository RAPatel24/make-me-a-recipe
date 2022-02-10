"""CRUD operations."""

from model import db, User, UserPreference, Preference, Recipe, ExcludeIngredient, Review, connect_to_db
import json, requests

recipe_data = []
def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_user_id_by_email(email):
    """Return a user by email."""

    result = db.session.query(User.id).filter(User.email == email).all()
    user_id = ""
    if result:
        for id in result:
            user_id = id[0]
    return user_id

def save_recipe(user_id,recipe_id):
    """ Save recipe """
    recipeSaved = isRecipeSaved(user_id,recipe_id)
    if not recipeSaved:
        recipe = Recipe(user_id = user_id, recipe_id = recipe_id)
        db.session.add(recipe)
        db.session.commit()
        return recipe

    return False
   
def isRecipeSaved(user_id,recipe_id):
    """ check if recipe is already saved for user """
    recipeSaved = db.session.query(User,Recipe).join(Recipe).filter(Recipe.recipe_id == recipe_id,Recipe.user_id == user_id).all()
    if not recipeSaved:
        return False
    
    return True

def get_saved_recipe_by_id(user_id):
    """ return saved recipes """
    result = db.session.query(Recipe.recipe_id).filter(Recipe.user_id == user_id).all()
    db.session.commit()
    recipe_id_list = []
    for id in result:
        recipe_id_list.append(id[0])
    
    return recipe_id_list
    
def remove_recipe(user_id, recipe_id):
    """delete recipe """
    Recipe.query.filter(Recipe.recipe_id == recipe_id, Recipe.user_id == user_id).delete()
    db.session.commit()
    return True

def get_excluded_ingredient(user_id):
    result = db.session.query(ExcludeIngredient.exclude_ingredient).filter(ExcludeIngredient.user_id == user_id).all()
    db.session.commit()
    exclude_ingredient_list = []
    for ingredient in result:
        exclude_ingredient_list.append(ingredient[0])
    return exclude_ingredient_list

def save_ingredient_to_exclude(user_id, ingredient_list):
    for ingredient in ingredient_list:
        exclude_entry = ExcludeIngredient(user_id = user_id, exclude_ingredient = ingredient)
        db.session.add(exclude_entry)
        db.session.commit()
    return db.session.query(ExcludeIngredient).filter(ExcludeIngredient.user_id == user_id).all()

def get_review(recipe_id):
    """Return recipe reviews"""

    result = db.session.query(Review.user_id,Review.recipe_review,Review.recipe_rating).filter(Review.recipe_id == recipe_id).all()
    reviews = []
    for index, tuple in enumerate(result):
        review = { "user_name":"", "review": "", "rating": ""}
        name = get_user_by_id(tuple[0])
        review['user_name'] = name
        review['review'] = tuple[1]
        review['rating'] = tuple[2]
        reviews.append(review)

    return reviews

def get_reviews_total(recipe_id):
    """Return recipe reviews"""

    result = db.session.query(Review.user_id,Review.recipe_review,Review.recipe_rating).filter(Review.recipe_id == recipe_id).all()
    reviews = []
    for index, tuple in enumerate(result):
        review = { "user_name":"", "review": "", "rating": ""}
        name = get_user_by_id(tuple[0])
        review['user_name'] = name
        review['review'] = tuple[1]
        review['rating'] = tuple[2]
        reviews.append(review)
    total_reviews = len(reviews)
    return total_reviews

def get_user_by_id(user_id):
    """Return a user by id."""

    result = db.session.query(User.fname,User.lname).filter(User.id == user_id).all()
    name = ""
    for index, tuple in enumerate(result):
        fname = tuple[0]
        lname = tuple[1]
        name = fname + " " + lname
    return name

def get_recipe(recipe_id, API_KEY):
    recipeJsonData = []
    recipe = []
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?includeNutrition=true&apiKey={API_KEY}'
    req = requests.get(url)
    jsonData = req.json()
    recipeJsonData.append(jsonData)
    for value in recipeJsonData:
        ddict = {
            'recipe_id':"",
            'ingredients': [],
            'title':'',
            'readyInMinutes': '',
            'servings': '',
            'imageUrl': '',
            'instructions': [],
            'sourceUrl': '',
            'isRecipeSaved': '',
            'total_reviews': '',
            'nutrition': {},
            'summary': '',
            'spoonacularSourceUrl': ''
        }
        ddict['title'] = value['title']
        ddict['recipe_id'] = value['id']
        for ingredient in value['extendedIngredients']:
            ddict['ingredients'].append(ingredient['original'])
        ddict['readyInMinutes'] = value['readyInMinutes']
        ddict['servings'] = value['servings']
        ddict['imageUrl'] = value['image']
        ddict['sourceUrl'] = value['sourceUrl']
        ddict['total_reviews'] = get_reviews_total(value['id'])
        ddict['summary'] = value['summary']
        ddict['spoonacularSourceUrl'] = value['spoonacularSourceUrl']
        nutrientdict = {}
        nutrientslist= value['nutrition']
        nutrition_include_list = ['Calories','Fat','Carbohydrates','Sugar','Cholesterol','Protein','Fiber']
        for index,data in enumerate(nutrientslist['nutrients']):
            if nutrientslist['nutrients'][index]['name'] in nutrition_include_list:
                nutrientdict[nutrientslist['nutrients'][index]['name']] = nutrientslist['nutrients'][index]['amount']
        ddict['nutrition'] = nutrientdict
        for steps in value['analyzedInstructions']:
            for value in steps['steps']:
                ddict['instructions'].append(value['step'])
        
    recipe.append(ddict) 
    return recipe

def add_review(user_id, recipe_id, review, rating):
    """add new review."""

    review_added = db.session.query(Review).filter(Review.recipe_id==recipe_id,Review.user_id==user_id).all()

    if not review_added:
        recipe_review = Review(user_id=user_id, recipe_id=recipe_id, recipe_review=review, recipe_rating=rating)
        db.session.add(recipe_review)
        db.session.commit()
        return recipe_review

    return "you have already added a review"

if __name__ == "__main__":
    from server import app

    connect_to_db(app)