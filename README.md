# Make Me A Recipe
###### This is a Python/Flask application which uses spoonacular external api. The goal behind this application is user can find recipes on the basis of ingredients they have at their home in refrigerator or pantry.

### Features
1. Find recipe by entering Ingredients.
2. Find recipe by cuisine, recipe-key word, meal type.
3. Signup/Signin 
4. Signed In users can save recipe to favorites, email and print recipe.
5. Users can add any allergies or ingredients they want to avoid in recipe.
6. Users can add reviews to recipe.

### How To Use This
1. Navigate over to https://spoonacular.com/food-api, get free api key.
2. Clone git repository: https://github.com/RAPatel24/make-me-a-recipe.git
3. Fill in the api key in secrets.sh file in the root folder. Add your api key as an environment variable API_KEY
4. Run secrets.sh file
5. Run pip install -r requirements.txt to install dependencies
6. Run python3 server.py
7. Navigate to http://localhost:5001 in your browser
