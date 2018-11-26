import json
import variables
import os

def readCompetitions():
    with open(variables.competitions_location) as competitonJson:
        data = json.load(competitonJson)

    return data

def readMatches():
    directory = os.fsencode(variables.matches_location)
    matches = []

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"): 
            with open(os.path.join(directory, file)) as matchFile:
                data = json.load(matchFile)
                matches.append(data)
        else:
            continue

    return matches

# def readLineups():
#     directory = os.fsencode(variables.lineups_location)
#     matches = []

#     for file in os.listdir(directory):
#         filename = os.fsdecode(file)
#         if filename.endswith(".json"): 
#             with open(os.path.join(directory, file)) as matchFile:
#                 data = json.load(matchFile)
#                 matches.append(data)
#         else:
#             continue

#     return matches   

# def readEvents():
#     with open(variables.competitions_location) as competitonJson:
#         data = json.load(competitonJson)

#     return data    