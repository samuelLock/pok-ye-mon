import requests
import json
from flask import Flask
app = Flask(__name__)

baseUrl = "https://pokeapi.co/api/v2/pokemon-species/"
shakespeareUrl = "https://api.funtranslations.com/translate/shakespeare"

def extractDescription(pokemonData, name):
    allDescriptions = pokemonData["flavor_text_entries"]
    description = extractEnglishDescription(allDescriptions, name)
    return description

def extractEnglishDescription(pokemonDescriptions, name):
    engDescription = []
    for description in pokemonDescriptions:
        if description["language"]["name"] == "en" and description["version"]["name"] == "yellow":
            engDescription.append(description["flavor_text"])
    if engDescription.count > 1:
        raise IndexError("Expected 1 count of english descriptions for " + name + " in Pokemon Yellow. Instead " + str(engDescription.count) +" were found.")
    return engDescription[0]

def replaceUnwantedCharacters(string :str, replacements :tuple) -> str:
    for pair in replacements:
        string = string.replace(pair[0], pair[1])
    return string

def translateDescription(phrase: str) -> str:
    try:
        r = requests.post(url = shakespeareUrl, data = {'text':phrase}) # Should never really throw an exception in theory, hence throwing 500.
        data = r.json()
    except:
        return("Internal server error", 500)
    
    if r.status_code != 200:
        return ("Bad Gateway (Shakespeare API)",502)

    try:
        translation = data["contents"]["translated"]
    except:
        return ("Bad Gateway (Shakespeare API)",502)
        
    return translation

@app.route('/pokemon/<name>')
def name(name):
    url = baseUrl+name
    try:
        r = requests.get(url = url) # Should never really throw an exception in theory, hence throwing 500.
        data = r.json()
    except:
        return("Internal server error", 500)

    if: r.status_code != 200: # Likely if the pokemon doesn't exist.
        return("Not Found", 404)

    try:
        description = extractDescription(data, name)
    except:
        return ("Bad Gateway (Pokemon API)",502)
    
    if description == []:
        return ("Not Found (Are you sure your Pokemon is from the first generation?)", 404)

    description = replaceUnwantedCharacters(json.dumps(description), (("\\n"," "), ("\\u00e9","e")))
    translatedDescription = translateDescription(description)
    return translatedDescription