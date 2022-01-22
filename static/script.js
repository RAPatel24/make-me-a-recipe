function showRecipes(results) {
    let recipes = []
    for(let item of results) {
        let recipe = {}
        recipe["id"] = item.id
        recipe["title"] = item.title;
        recipe["image"] = item.image;
        let missedIngredients = []
        for (let i of item.missedIngredients) {
            missedIngredients.push(i.name)
        }
        recipe["missedIngredients"] = missedIngredients
        let usedIngredients = []
        for(let i of item.usedIngredients) {
            usedIngredients.push(i.name)
        }
        recipe["usedIngredients"] = usedIngredients
        recipes.push(recipe)
    }
    const ele = document.querySelector('#recipe_list')
    ele.insertAdjacentHTML('beforebegin', "<h4>Results</h4>")
    for (key of recipes) {
        console.log(key);
        ele.insertAdjacentHTML('afterbegin', 
                `<div class="col-4 text-center">
                    <a href="recipe/${key.id}/${key.title}" onclick="gotoRecipe(${key.id})"><div id="recipe_div" style="border: 1px grey solid; padding: 25px;">
                    <h4>${key.title}</h4>
                    <img src='${key.image}'>
                    <p><strong>Used Ingredients:</strong> <i>${key.usedIngredients}</i></p>
                    <p><strong>Missed Ingredients:</strong> <i>${key.missedIngredients}</i></p>
                    </div>
                    </a>
                </div>`)
    }
}

function getRecipes(evt) {
    evt.preventDefault();
    console.log("inside recipes")
    const api_key = document.getElementById('api-key').innerHTML
    const formInputs = document.querySelector('#search-box').value
    const url = `https://api.spoonacular.com/recipes/findByIngredients?ingredients=${formInputs}&number=20&apiKey=${api_key}`
    fetch(url, {
    headers: {
        'Content-Type': 'application/json',
    },
    })
    .then(response => response.json())
    .then(showRecipes);
}

document.querySelector('#search-recipe-form').addEventListener('submit', getRecipes);

function gotoRecipe(id) {
    console.log(id)
}