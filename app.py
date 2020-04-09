import requests
import json
from flask import Flask
app = Flask(__name__)

baseUrl = "https://pokeapi.co/api/v2/pokemon-species/"

def extractDescription(pokemonData):
    allDescriptions = pokemonData["flavor_text_entries"]
    description = extractEnglishDescription(allDescriptions)
    return description

def extractEnglishDescription(pokemonDescriptions):
    engDescription = []
    for description in pokemonDescriptions:
        if description["language"]["name"] == "en" and description["version"]["name"] == "y":
            engDescription.append(description["flavor_text"])
    return engDescription[0]

@app.route('/pokemon/<name>')
def name(name):
    url = baseUrl+name
    r = requests.get(url = url)
    data = r.json()
    description = extractDescription(data)
    return json.dumps(description)