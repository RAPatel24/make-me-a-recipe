const api_key = document.getElementById('api-key').innerHTML
function showRecipes(results) {
    document.querySelector('#search-recipe-form').reset()
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
        let exclude_ingredients = getExcludedIngredients()
        console.log(exclude_ingredients)
        function findCommonElement(a1, a2) {
            for(let i = 0; i < a1.length; i++) {
                for(let j = 0; j < a2.length; j++) {
                    if(a1[i].includes(a2[j])) {
                        return true
                    }
                }
            }
            return false;
        }
        if(!findCommonElement(missedIngredients,exclude_ingredients)) {
            recipes.push(recipe)
        }
    }
    const ele = document.querySelector('#recipe_list')
    document.querySelector('#results-title').classList.add('d-block')
    document.querySelector('#results-title').classList.remove('d-none')
    //ele.insertAdjacentHTML('beforebegin', `<h4 id="results-title">Results</h4>`)
    for (key of recipes) {
        ele.insertAdjacentHTML('afterbegin', 
                `<div class="col-4 text-center">
                    <a href="recipe/${key.id}/${key.title}" onclick="gotoRecipe(${key.id})"><div id="recipe_div" style="border: 1px grey solid; padding: 25px;">
                    <h5>${key.title}</h5>
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
    document.querySelector('#recipe_list').innerHTML = ""
    document.querySelector('#results-title').classList.add('d-none')
    document.querySelector('#results-title').classList.remove('d-block')
    const ingredients = document.querySelector('#search-box').value
    const url = `https://api.spoonacular.com/recipes/findByIngredients?ingredients=${ingredients}&number=30&apiKey=${api_key}`
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
document.querySelector('#exclude-ingredient').addEventListener("keyup", excludeIngredient)
function excludeIngredient(e) {
    if (e.keyCode === 13) {
        // Cancel the default action, if needed
        e.preventDefault();
        let text = document.querySelector('#exclude-ingredient').value;
        let ele = document.querySelector('#exclude-ingredient-section');
        ele.insertAdjacentHTML('afterbegin',
                        `<div class="exclude-toast" id=${text}>
                            <p id="exclude-value">${text}</p>
                            <button type="button" class="btn-close" aria-label="Close" onClick=closeButton(${text})></button>
                        </div>`);
        document.querySelector('#exclude-ingredient').value = ''
    }
}
function getExcludedIngredients() {
    let values = document.querySelectorAll('p#exclude-value')
    let excludeIngredientList = []
    for(let i=0; i<values.length; i++)
    {
        excludeIngredientList.push(values[i].innerHTML)
    }
    return excludeIngredientList
}

function closeButton(ele) {
    ele.remove()
}
/*document.querySelector('#search-by-recipe').addEventListener('submit', getRecipesByKeyword);
function getRecipesByKeyword(evt) {
    evt.preventDefault();
    let recipeKeyword = document.querySelector('#search-recipe').value;
    let diet =  document.querySelector('#search-by-recipe-diet').value;
    let url;
    if(diet !== 'Diet' && recipeKeyword !== null) {
        url = `https://api.spoonacular.com/recipes/complexSearch?query=${recipeKeyword}&diet=${diet}&number=20&apiKey=${api_key}`
    } else {
        url = `https://api.spoonacular.com/recipes/complexSearch?query=${recipeKeyword}&number=20&apiKey=${api_key}`
    }
    
    fetch(url, {
    headers: {
        'Content-Type': 'application/json',
    },
    })
    .then(response => response.json())
    .then(showRecipesByKeyword);
}

document.querySelector('#search-by-cuisine-and-type').addEventListener('submit', getRecipesByCuisineAndType);
function getRecipesByCuisineAndType(evt) {
    evt.preventDefault();
    let cuisine = document.querySelector('#cuisine').value;
    let diet =  document.querySelector('#diet').value;
    let type =  document.querySelector('#type').value;
    let url;
    if(diet !== 'Diet' && cuisine !== 'Cuisine' && type !== 'Type') {
        url = `https://api.spoonacular.com/recipes/complexSearch?cuisine=${cuisine}&diet=${diet}&type=${type}&number=20&apiKey=${api_key}`
    } 
    else if(diet == 'Diet' && cuisine !== 'Cuisine' && type !== 'Type') {
        url = `https://api.spoonacular.com/recipes/complexSearch?cuisine=${cuisine}&type=${type}&number=20&apiKey=${api_key}`
    }
    else if(diet !== 'Diet' && cuisine !== 'Cuisine' && type == 'Type') {
        url = `https://api.spoonacular.com/recipes/complexSearch?cuisine=${cuisine}&diet=${diet}&number=20&apiKey=${api_key}`
    }
    else if(diet !== 'Diet' && cuisine == 'Cuisine' && type == 'Type') {
        url = `https://api.spoonacular.com/recipes/complexSearch?diet=${diet}&type=${type}&number=20&apiKey=${api_key}`
    }
    else if(diet == 'Diet' && cuisine == 'Cuisine' && type !== 'Type') {
        url = `https://api.spoonacular.com/recipes/complexSearch?type=${type}&number=20&apiKey=${api_key}`
    } 
    else if(diet !== 'Diet' && cuisine == 'Cuisine' && type == 'Type') {
        url = `https://api.spoonacular.com/recipes/complexSearch?type=${type}&number=20&apiKey=${api_key}`
    } else {
        url = `https://api.spoonacular.com/recipes/complexSearch?cuisine=${cuisine}&number=20&apiKey=${api_key}`
    }
    
    fetch(url, {
    headers: {
        'Content-Type': 'application/json',
    },
    })
    .then(response => response.json())
    .then(showRecipesByKeyword);
}

function showRecipesByKeyword(results) {
    let recipes = []
    console.log(results.results)
    for(let item of results.results) {
        let recipe = {}
        recipe["id"] = item.id
        recipe["title"] = item.title;
        recipe["image"] = item.image;
        recipes.push(recipe)
    }
    fetch(`/getmethod/${recipes}`,{
        headers: {
            'Content-Type': 'application/json',
        },
        })
        .then(response => response.json())
        .then(response => console.log(response));
}*/