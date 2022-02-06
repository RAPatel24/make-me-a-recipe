import json, requests
from flask import session

def get_local_recipe_data():
    with open("data/home-recipes.json") as f:
        recipe_data = json.loads(f.read())

    return recipe_data

def get_local_recipe_id_list():
    
    recipe_data = get_local_recipe_data()
    recipe_id_list = []
    for data in recipe_data:
        recipe_id_list.append(data['id'])
    
    return recipe_id_list

def get_logged_in_user_id():
    user_id = session.get('user_id')
    return user_id

def get_logged_in_user_email():
    user_email = session.get('user_email')
    return user_email

def is_logged_in():
    if session.get('user_id') and session.get('user_email'):
        return True
    return False

def get_recipes(recipe_id, API_KEY):
    recipe = []
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?includeNutrition=false&apiKey={API_KEY}'
    req = requests.get(url)
    jsonData = req.json()
    recipe.append(jsonData)
    return recipe