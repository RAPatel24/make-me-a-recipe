const api_key = document.getElementById('api-key').innerHTML
function showRecipes(results) {
    let recipe_list = []
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
        function findCommonElement(a1, a2) {
            for(let i = 0; i < a1.length; i++) {
                for(let j = 0; j < a2.length; j++) {
                    if(a1[i].includes(a2[j]) || a2[j].includes(a1[i])) {
                        return true
                    }
                }
            }
            return false;
        }
        if(!findCommonElement(missedIngredients,exclude_ingredients)) {
            recipe_list.push(recipe)
        }

    }
    console.log(`recipe_list_length: ${recipe_list.length}`)
    const ele = document.querySelector('#recipe_list')
    document.querySelector('#results-title').classList.add('d-block')
    document.querySelector('#results-title').classList.remove('d-none')
    //ele.insertAdjacentHTML('beforebegin', `<h4 id="results-title">Results</h4>`)
    for (key of recipe_list) {
        ele.insertAdjacentHTML('afterbegin', 
                `<div class="col-4 text-center">
                    <div id="recipe_div" style="border: 1px grey solid; padding: 25px;">
                    <a href="javascript:void(0);" id="save-${key.id}" onclick="saveRecipe('${key.id}','${key.title}')">
                        <i class='far fa-heart' style='font-size:24px' id="save-heart-icon"></i>
                    </a>
                    <a href="javascript:void(0);" id="remove-${key.id}" style="display:none" onclick="removeRecipe('${key.id}','${key.title}')">
                        <i class='fa fa-heart' style='font-size:24px' id="save-heart-icon"></i>
                    </a>
                    <a href="recipe/${key.id}/${key.title}">
                    <h5>${key.title}</h5>
                    <img src='${key.image}'>
                    <p><strong>Used Ingredients:</strong> <i>${key.usedIngredients}</i></p>
                    <p><strong>Missed Ingredients:</strong> <i>${key.missedIngredients}</i></p>
                    </div>
                    </a>
                </div>`)
    }
    document.querySelector('#recipe_list').insertAdjacentHTML('afterend', 
    `<div><button>See All ${recipe_list.length} recipes</button></div>`)
}

function getRecipes(evt) {
    evt.preventDefault();
    document.querySelector('#recipe_list').innerHTML = ""
    document.querySelector('#results-title').classList.add('d-none')
    document.querySelector('#results-title').classList.remove('d-block')
    const ingredients = document.querySelector('#search-box').value
    const url = `https://api.spoonacular.com/recipes/findByIngredients?ingredients=${ingredients}&number=40&apiKey=${api_key}`
    fetch(url, {
    headers: {
        'Content-Type': 'application/json',
    },
    })
    .then(response => response.json())
    .then(showRecipes);
}

document.querySelector('#search-recipe-form').addEventListener('submit', getRecipes);

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

function sendEmail() {
    const email = document.getElementById('send-email-value').value
    const recipe_id = document.querySelector('#recipe-id').innerHTML
    const recipe_title = document.querySelector('#recipe-title').innerHTML
    fetch(`/email?email=${email}&recipe_id=${recipe_id}&recipe_title=${recipe_title}`,{
        headers: {
            'Content-Type': 'application/json',
        },
        })
        .then(response => response.json())
        .then(response => console.log(response));
}
function openPrintPopup() {
     window.print()
 }

function saveRecipe(id,recipe) {
    console.log("inside save")
    fetch(`recipe/${id}/${recipe}?save=True`,{
        headers: {
            'Content-Type': 'application/json',
        },
        })
        .then(response => {
            console.log(response)
            if(response.status== "200" && response.url == "http://localhost:5001/signup") {
                location.href="http://localhost:5001/signup"
            }
            else {
                document.getElementById(`save-${id}`).style.display = "none"
                document.getElementById(`remove-${id}`).style.display = "block"
            }
        })
}

function removeRecipe(id,recipe) {
    console.log("inside remove")
    fetch(`recipe/${id}/${recipe}?remove=True`,{
        headers: {
            'Content-Type': 'application/json',
        },
        })
        .then(response => {
            document.getElementById(`save-${id}`).style.display = "block"
            document.getElementById(`remove-${id}`).style.display = "none"
        })
}