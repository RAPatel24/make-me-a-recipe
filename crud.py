"""CRUD operations."""

from model import db, User, UserPreference, Preference, Recipe, connect_to_db

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
    result = db.session.query(Recipe.recipe_id.distinct()).filter(User.id == user_id).all()
    recipe_id_list = []
    for id in result:
        recipe_id_list.append(id[0])
    
    return recipe_id_list
    
def remove_recipe(user_id, recipe_id):
    """delete recipe """
    Recipe.query.filter(Recipe.recipe_id == recipe_id, Recipe.user_id == user_id).delete()
    db.session.commit()
    return True

if __name__ == "__main__":
    from server import app

    connect_to_db(app)