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
//functions for creating and removing monsters from the encounter.


function createLink() {
	// let linkContainer = document.getElementById("linkContainer");
	let inputField = document.getElementById("monster");

	let monsterName = inputField.value;

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


//function for removing a monster from an encounter.
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

//---------------------------------------------------------
//functions for creating and removing initiative cards.

let selectedCard = null;

  function createCard() {

    // Create the card element
    let card = document.createElement("div");
    card.classList.add("card"); // Add 'card' class to the card element

    // Create the card body element
    let cardBody = document.createElement("div");
    cardBody.classList.add("card-body"); // Add 'card-body' class to the card body element

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

    // Create the editable text fields
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

    // Append the text field to the card body
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

    // Append the remove button to the card body
    cardBody.appendChild(removeButton);

    // Append the card body to the card
    card.appendChild(cardBody);

    // Append the card to the card container
    let cardContainer = document.getElementById("cardContainer");
    cardContainer.appendChild(card);

    // localStorage.setItem("cardContainer", cardContainer.innerHTML);
    saveCardContainer();

    // Add click event listener to the card
    card.addEventListener("click", function () {
      if (selectedCard) {
        selectedCard.classList.remove("selected");
      }
      card.classList.add("selected");
      selectedCard = card;
    });
  }

  // Save the cardContainer HTML to Local Storage
  function saveCardContainer() {
    let cardContainer = document.getElementById("cardContainer");
    localStorage.setItem("cardContainer", cardContainer.innerHTML);
  }

  window.addEventListener("DOMContentLoaded", function () {
    let cardContainer = document.getElementById("cardContainer");
    let savedCardContainerHTML = localStorage.getItem("cardContainer");
    if (savedCardContainerHTML) {
      cardContainer.innerHTML = savedCardContainerHTML;

      // Attach event listeners to the remove buttons of existing cards
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

  function updateCardEventListeners() {
    let cardContainer = document.getElementById("cardContainer");
    let cards = cardContainer.getElementsByClassName("card");

    Array.from(cards).forEach(function (card) {
      // Remove click event listeners from all cards
      card.removeEventListener("click", cardClickHandler);

      // Add click event listener to each card
      card.addEventListener("click", cardClickHandler);
    });
  }

  function cardClickHandler() {
    let clickedCard = this;

    // If the clicked card is already selected, remove the selection
    if (clickedCard === selectedCard) {
      clickedCard.classList.remove("selected");
      selectedCard = null;
    } else {
      // If there is a previously selected card, remove its selection
      if (selectedCard) {
        selectedCard.classList.remove("selected");
      }
      // Add the selection to the clicked card
      clickedCard.classList.add("selected");
      selectedCard = clickedCard;
    }
  }