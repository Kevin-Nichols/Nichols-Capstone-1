import requests

def get_monster_data(monster_name):
    url = f'https://www.dnd5eapi.co/api/monsters/{monster_name}'
    res = requests.get(url)
    data = res.json()
    return data['result']

