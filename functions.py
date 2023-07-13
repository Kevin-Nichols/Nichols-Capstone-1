import requests

def get_monster_data(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception("An error occurred while fetching data")
    

def get_stat_block_data(data):
    
    proficiencies = []
    for proficiency in data["proficiencies"]:
        proficiency_data = {
            "Value": proficiency["value"],
            "Name": proficiency["proficiency"]["name"],
        }
        proficiencies.append(proficiency_data)
        
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
        
    actions = []
    for action in data["actions"]:
        if "actions" in action:
            del action["actions"]
            
        actions.append(action)
        
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
        # "image": data["image"],
    }
    return stat_block