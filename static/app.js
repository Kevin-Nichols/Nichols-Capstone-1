//---------------------------------------------------------
//functions for monster search field.
let url = "https://www.dnd5eapi.co/api/monsters/"
let allNames = [];

function getMonsterNames () {
    axios.get(url)
    .then(function(res){
        let arr = res.data.results
        arr.forEach(e => allNames.push(e.index))
    })
};
getMonsterNames();

const input = document.querySelector('#monster');
const suggestions = document.querySelector('.suggestions ul');
const lowerNames = allNames;

//Creates a variable that grabs input text and makes it lower case. Then creates a variable that compares the input and lowerNames, then creates a new array. Returns the new filtered array and changes the first letter back to upper case.
function search(str) {
	let userInput = input.value.toLowerCase();
	let results = lowerNames.filter(word => word.match(userInput));
	// let results = filterNames.map(x => x.charAt(0).toUpperCase() + x.substring(1));
	return results;
}

//Set the suggestions div to empty. Call showSuggestions using the results by calling the search function using the input value.
function searchHandler(e) {
	suggestions.innerHTML='';
	showSuggestions(search(input.value));
}

//Loop through if the results are not undefined and not empty, create an li and appened.
function showSuggestions(results) {
	for(let i = 0; i<=lowerNames.length; i++){
		if(results[i] != undefined && input.value != ''){
			let suggList = document.createElement('li');
			suggList.innerText = results[i];
			suggestions.appendChild(suggList);
		}
	}
}

//If the target clicked on is an li, make the input text = to the target text and set the suggestions div to empty.
function useSuggestion(e) {
	if(e.target.tagName === 'LI'){
		input.value = e.target.innerText;
		suggestions.innerHTML = '';
	}
}

input.addEventListener('keyup', searchHandler);
suggestions.addEventListener('click', useSuggestion);


//---------------------------------------------------------
//functions for other things.


function createLink() {
	let linkContainer = document.getElementById("linkContainer");
	let inputField = document.getElementById("monster");

	let monsterName = inputField.value;

	// Create the <a> element
	let link = document.createElement("a");
	link.href = "/stats/" + monsterName;
	link.textContent = `View Info for ${monsterName}`;

	// Append the <a> element to the link container
	linkContainer.appendChild(link);
	linkContainer.appendChild(document.createElement("br"));
}