import requests
import json
from flask import Flask
app = Flask(__name__)

baseUrl = "https://pokeapi.co/api/v2/pokemon-species/"
shakespeareUrl = "https://api.funtranslations.com/translate/shakespeare"
apiKey = "fVdKcXiN1t6_rc_FnSXROgeF"

def extractDescription(pokemonData, name):
    allDescriptions = pokemonData["flavor_text_entries"]
    description = extractEnglishDescription(allDescriptions, name)
    return description

def extractEnglishDescription(pokemonDescriptions, name):
    engDescription = []
    for description in pokemonDescriptions:
        if description["language"]["name"] == "en" and description["version"]["name"] == "yellow": # Extracts the english version of Pokemon Yellow's description for the pokemon.
            engDescription.append(description["flavor_text"])
    if len(engDescription) > 1: # Raise IndexError if there are more than one description. This should never happen.
        raise IndexError("Expected 1 count of english descriptions for " + name + " in Pokemon Yellow. Instead " + str(engDescription.count) +" were found.")
    if len(engDescription) == 0: # Raise ValueError if there is no description. This occurs when the pokemon does exist but not in Pokemon Yellow (or in English). A different exception type is needed so the exception is handled differently in the calling code.
        raise ValueError("Expected 1 count of english descriptions for " + name + " in Pokemon Yellow. Instead none were found.")
    return engDescription[0]

def replaceUnwantedCharacters(string :str, replacements :tuple) -> str: # replacements should be a tuple of pairs of strings e.g ((foo,bar),(wiz,bang)
    for pair in replacements:
        string = string.replace(pair[0], pair[1])
    return string

def translateDescription(phrase: str) -> str:
    try:
        r = requests.post(url = shakespeareUrl, data = {'text':phrase, 'api_key':apiKey}) # Should never really throw an exception in theory, hence throwing 500.
    except Exception as e:
        print(e)
        return("Internal server error", 500)
    
    if r.status_code != 200:
        print("Shakespeare API responded with " + str(r.status_code))
        return("Bad Gateway (Shakespeare API)",502)

    try:
        data = r.json()
        translation = data["contents"]["translated"]
    except Exception as e:
        print(e)
        return("Bad Gateway (Shakespeare API)",502)

    return translation

@app.route('/pokemon/<name>')
def name(name):
    url = baseUrl+name
    try:
        r = requests.get(url = url) # Should never really throw an exception in theory, hence throwing 500.
    except Exception as e:
        print(e)
        return("Internal server error", 500)

    if r.status_code == 404: # Likely if the pokemon doesn't exist.
        return("Not Found (Are you sure your pokemon exists?)", 404)
    elif r.status_code != 200:
        return("Bad Gateway (Pokemon API responded with " + str(r.status_code)+")",502)

    try:
        data = r.json()
        description = extractDescription(data, name)
    except ValueError as e:
            return ("Not Found (Are you sure your Pokemon is from the first generation?)", 404)
    except Exception as e:
            print(e)
            return ("Bad Gateway (Pokemon API)",502)

    description = replaceUnwantedCharacters(json.dumps(description), (("\\n"," "), ("\\f"," "), ("\\u00e9","e")))
    translatedDescription = translateDescription(description)
    return translatedDescription