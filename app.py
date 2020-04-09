import requests
import json
from flask import Flask
app = Flask(__name__)

baseUrl = "https://pokeapi.co/api/v2/pokemon-species/"
shakespeareUrl = "https://api.funtranslations.com/translate/shakespeare"

def extractDescription(pokemonData):
    allDescriptions = pokemonData["flavor_text_entries"] # Try catch
    description = extractEnglishDescription(allDescriptions)
    return description

def extractEnglishDescription(pokemonDescriptions):
    engDescription = []
    for description in pokemonDescriptions:
        if description["language"]["name"] == "en" and description["version"]["name"] == "y":
            engDescription.append(description["flavor_text"])
    # Check count is 1, if not throw error
    return engDescription[0]

def replaceUnwantedCharacters(string :str, replacements :tuple) -> str:
    for pair in replacements:
        string = string.replace(pair[0], pair[1])
    return string

def translateDescription(phrase: str) -> str:
    r = requests.post(url = shakespeareUrl, data = {'text':phrase}) # Try catch
    data = r.json()
    translation = data["contents"]["translated"]
    return translation

@app.route('/pokemon/<name>')
def name(name):
    url = baseUrl+name
    r = requests.get(url = url) # Try catch
    data = r.json()
    description = extractDescription(data)
    description = replaceUnwantedCharacters(json.dumps(description), (("\\n"," "), ("\\u00e9","e")))
    translatedDescription = translateDescription(description)
    return translatedDescription