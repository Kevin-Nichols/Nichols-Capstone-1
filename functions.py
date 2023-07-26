from jinja2 import nodes
from jinja2.ext import Extension
import requests

#Retrieves all monster data from the API.
def get_monster_data(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception("An error occurred while fetching data")
    
#Handles the removal of unwanted keys on a monster's stats page.
def remove_keys(data, keys_to_remove):
    if isinstance(data, dict):
        for key, value in list(data.items()):
            if key in keys_to_remove:
                del data[key]
            else:
                remove_keys(value, keys_to_remove)
    elif isinstance(data, list):
        for item in data:
            remove_keys(item, keys_to_remove)
    
#Handles generating all wanted data from the API on a monster's stat page.
def get_stat_block_data(data):
    
    #Makes changes to the proficiencies key value data.
    proficiencies = []
    for proficiency in data["proficiencies"]:
        proficiency_data = {
            "Name": proficiency["proficiency"]["name"] + " " + "|" + " " + str(proficiency["value"]),
        }
        proficiencies.append(proficiency_data)
        
    #Makes changes to the abilities key value data.
    abilities = []
    for ability in data["special_abilities"]:
        dc_type_name = ""
        if "dc" in ability and "dc_type" in ability["dc"]:
            dc_type_name = ability["dc"]["dc_type"]["name"]

        ability_data = {
            "name": ability["name"],
            "desc": ability["desc"]
        }
        if dc_type_name:
            ability_data["DC Type"] = dc_type_name

        abilities.append(ability_data)
        
    #Makes changes to the actions key value data.
    actions = []
    for action in data["actions"]:
        if "actions" in action:
            del action["actions"]
            
        remove_keys(action, ["url", "index"])
            
        actions.append(action)
        
    #This is the wanted info to display in a given monster from the API.
    stat_block = {
        "Name": data["name"],
        "Size": data["size"],
        "Type": data["type"],
        "Alignment": data["alignment"],
        "Armor Class": data["armor_class"],
        "Hit Points": data["hit_points"],
        "Hit Points Roll": data["hit_points_roll"],
        "Speed": data["speed"],
        "Strength": data["strength"],
        "Dexterity": data["dexterity"],
        "Constitution": data["constitution"],
        "Intelligence": data["intelligence"],
        "Wisdom": data["wisdom"],
        "Charisma": data["charisma"],
        "Proficiencies": proficiencies,
        "Senses": data["senses"],
        "Languages": data["languages"],
        "Challenge_rating": data["challenge_rating"],
        "Special Abilities": abilities,
        "Actions": actions,
        "Legendary Actions": data["legendary_actions"],
    }
    return stat_block


#TODO: Stretch goals I would like to achieve.
    # Change spacing on all encounters page.
    # Find monster image database and include images for all monsters.
    # Implement a "forgot my password" function and route.
    # Make the monster stat page prettier.
