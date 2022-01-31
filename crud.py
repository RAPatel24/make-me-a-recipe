"""CRUD operations."""

from model import db, User, UserPreference, Preference, Recipe, ExcludeIngredient, connect_to_db

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
    recipeSaved = db.session.query(User,Recipe).join(Recipe).filter(Recipe.recipe_id == recipe_id).all()
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

if __name__ == "__main__":
    from server import app

    connect_to_db(app)