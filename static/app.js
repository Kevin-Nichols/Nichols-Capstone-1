//-----------------------------------------------------------------------------------------------
//functions for the monster search field on the /encounter/<int:encounter_id> page.

let url = "https://www.dnd5eapi.co/api/monsters/"
let allNames = [];
const input = document.querySelector('#monster');
const suggestions = document.querySelector('.suggestions ul');
const lowerNames = allNames;

//Retrieves all monster names that exist in the API.
function getMonsterNames () {
    axios.get(url)
    .then(function(res){
        let arr = res.data.results
        arr.forEach(e => allNames.push(e.index))
    })
};
getMonsterNames();

//Creates a variable that grabs input text and makes it lower case. Then creates a variable that compares the input and lowerNames, then creates a new array.
function search(str) {
	let userInput = input.value.toLowerCase();
	let results = lowerNames.filter(word => word.match(userInput));
	return results;
}

//Sets the suggestions div to empty. Calls showSuggestions using the results by calling the search function using the input value.
function searchHandler(e) {
	suggestions.innerHTML='';
	showSuggestions(search(input.value));
}

//Loop through if the results are not undefined and not empty, create an li and append.
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



//-----------------------------------------------------------------------------------------------
//functions for creating and removing monsters from an encounter page.

//Creates a link on the encounter page that takes a user to the monster's stats page.
function createLink() {
	let inputField = document.getElementById("monster");

	let monsterName = inputField.value;

  if(allNames.some(e => e == monsterName)){
	fetch("/monster/add", {
        method: "POST",
        body: JSON.stringify({ monsterName }),
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token() }}"
        }
    })

	setTimeout(function() {
		location.reload();
	  }, 50);
  }
}

//Function for removing a monster from an encounter.
$(document).ready(function() {
	// Submit the form when the Remove button is clicked
	$('.remove-monster-form').submit(function(event) {
		event.preventDefault();
		var form = $(this);
		$.ajax({
			url: form.attr('action'),
			type: form.attr('method'),
			data: form.serialize(),
			success: function(response) {
				// Remove the <li> from the list
				form.closest('li').remove();
			},
			error: function(error) {
				console.log(error);
			}
		});
	});
});



//-----------------------------------------------------------------------------------------------
//functions for initiative cards on an encounter page.

let selectedCard = null;

  //Creates an initiative card on an encounter page.
  function createCard() {

    // Create the card element.
    let card = document.createElement("div");
    card.classList.add("card");

    // Create the card body element.
    let cardBody = document.createElement("div");
    cardBody.classList.add("card-body");

    let br = document.createElement("br");

    let nameLabel = document.createElement("label");
    nameLabel.innerText = "Player Name";
    nameLabel.classList.add("card-label");
    let hitPointLabel = document.createElement("label");
    hitPointLabel.innerText = "Hit Points";
    hitPointLabel.classList.add("card-label");
    let acLabel = document.createElement("label");
    acLabel.innerText = "Armor Class";
    acLabel.classList.add("card-label");
    let spellSaveDCLabel = document.createElement("label");
    spellSaveDCLabel.innerText = "Spell Save DC";
    spellSaveDCLabel.classList.add("card-label");

    // Create the editable text fields.
    let nameField = document.createElement("input");
    nameField.type = "text";
    nameField.id = "player-name"
    nameField.name = "player-name";
    nameField.value = "";
    nameField.classList.add("card-input");
    let hitPointField = document.createElement("input");
    hitPointField.type = "text";
    hitPointField.id = "hit-points"
    hitPointField.name = "hit-points";
    hitPointField.value = "";
    hitPointField.classList.add("card-input");
    let acField = document.createElement("input");
    acField.type = "text";
    acField.id = "armor-class"
    acField.name = "armor-class";
    acField.value = "";
    acField.classList.add("card-input");
    let spellSaveDCField = document.createElement("input");
    spellSaveDCField.type = "text";
    spellSaveDCField.id = "spell-save"
    spellSaveDCField.name = "spell-save";
    spellSaveDCField.value = "";
    spellSaveDCField.classList.add("card-input");

    // Append the text field to the card body.
    cardBody.appendChild(nameLabel);
    cardBody.appendChild(nameField);
    cardBody.appendChild(br.cloneNode());
    cardBody.appendChild(hitPointLabel);
    cardBody.appendChild(hitPointField);
    cardBody.appendChild(br.cloneNode());
    cardBody.appendChild(acLabel);
    cardBody.appendChild(acField);
    cardBody.appendChild(br.cloneNode());
    cardBody.appendChild(spellSaveDCLabel);
    cardBody.appendChild(spellSaveDCField);
    cardBody.appendChild(br.cloneNode());


    let removeButton = document.createElement("button");
    removeButton.textContent = "Remove";
    removeButton.classList.add("btn", "btn-outline-danger");
    removeButton.addEventListener("click", function () {
      cardContainer.removeChild(card);
      saveCardContainer();
      saveCardData();
    });

    // Append the remove button to the card body.
    cardBody.appendChild(removeButton);

    // Append the card body to the card.
    card.appendChild(cardBody);

    // Append the card to the card container.
    let cardContainer = document.getElementById("cardContainer");
    cardContainer.appendChild(card);

    saveCardContainer();

    // Add click event listener to the card.
    card.addEventListener("click", function () {
      if (selectedCard) {
        selectedCard.classList.remove("selected");
      }
      card.classList.add("selected");
      selectedCard = card;
    });
  }

  // Saves the cardContainer and it's contents.
  function saveCardContainer() {
    let cardContainer = document.getElementById("cardContainer");
    localStorage.setItem("cardContainer", cardContainer.innerHTML);
  }

  window.addEventListener("DOMContentLoaded", function () {
    let cardContainer = document.getElementById("cardContainer");
    let savedCardContainerHTML = localStorage.getItem("cardContainer");
    if (savedCardContainerHTML) {
      cardContainer.innerHTML = savedCardContainerHTML;

      // Attach event listeners to the remove buttons of existing cards.
      let removeButtons = cardContainer.getElementsByClassName("btn", "btn-outline-danger");
      Array.from(removeButtons).forEach(function (button) {
        button.addEventListener("click", function () {
          let card = button.closest(".card");
          cardContainer.removeChild(card);
          saveCardContainer();
        });
      });

      loadCardData();
    }
  });

  //Saves data within each card after being edited.
  function saveCardData() {
    let cardContainer = document.getElementById("cardContainer");
    let cards = cardContainer.getElementsByClassName("card");
    let cardData = [];
    Array.from(cards).forEach(function (card) {
      let nameField = card.querySelector("#player-name");
      let hitPointField = card.querySelector("#hit-points");
      let acField = card.querySelector("#armor-class");
      let spellSaveDCField = card.querySelector("#spell-save");

      let data = {
        name: nameField.value,
        hitPoints: hitPointField.value,
        armorClass: acField.value,
        spellSaveDC: spellSaveDCField.value
      };

      cardData.push(data);
    });

    localStorage.setItem("cardData", JSON.stringify(cardData));
  }

  //Loads card data back in page is reloaded.
  function loadCardData() {
    let cardContainer = document.getElementById("cardContainer");
    let savedCardData = localStorage.getItem("cardData");
    if (savedCardData) {
      let cardData = JSON.parse(savedCardData);

      let cards = cardContainer.getElementsByClassName("card");
      Array.from(cards).forEach(function (card, index) {
        let nameField = card.querySelector("#player-name");
        let hitPointField = card.querySelector("#hit-points");
        let acField = card.querySelector("#armor-class");
        let spellSaveDCField = card.querySelector("#spell-save");

        if (cardData[index]) {
          nameField.value = cardData[index].name || "";
          hitPointField.value = cardData[index].hitPoints || "";
          acField.value = cardData[index].armorClass || "";
          spellSaveDCField.value = cardData[index].spellSaveDC || "";
        }
      });
    }
    updateCardEventListeners();
  }

  //Updates event listeners if page is reloaded.
  function updateCardEventListeners() {
    let cardContainer = document.getElementById("cardContainer");
    let cards = cardContainer.getElementsByClassName("card");

    Array.from(cards).forEach(function (card) {
      card.removeEventListener("click", cardClickHandler);

      card.addEventListener("click", cardClickHandler);
    });
  }

  //Handles the highlighting of initiative cards.
  function cardClickHandler() {
    let clickedCard = this;

    // If the clicked card is already selected, remove the selection.
    if (clickedCard === selectedCard) {
      clickedCard.classList.remove("selected");
      selectedCard = null;
    } else {
      // If there is a previously selected card, remove its selection.
      if (selectedCard) {
        selectedCard.classList.remove("selected");
      }
      // Add the selection to the clicked card.
      clickedCard.classList.add("selected");
      selectedCard = clickedCard;
    }
  }