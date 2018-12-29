# Import the libraries we need
import pandas as pd
import re
import random
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
from Scraping import scrapeUnderstat
from ScrapingFPL import scrapeFPL
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pulp import *


def getPlayers():
    final_players = []

    all_players = scrapeUnderstat()
    fpl_players = scrapeFPL()

    all_players_copy = all_players[:]
    fpl_players_copy = fpl_players[:]

    print (len(all_players))
    print (len(fpl_players))

    count = 0

    # first pass through the players which closely match 
    for xgPlayer in all_players_copy:
        for fplPlayer in fpl_players_copy:

            ratio = fuzz.ratio( xgPlayer["player_name"], fplPlayer["first_name"]+ " " + fplPlayer["second_name"] )

            if ( ratio > 90 ):
                print(xgPlayer["player_name"] + " close matches with : " + fplPlayer["first_name"] + " " + fplPlayer["second_name"] )
                final_players.append( [ xgPlayer["player_name"], xgPlayer["xG"], xgPlayer["xA"], fplPlayer["now_cost"], fplPlayer["total_points"], xgPlayer["time"], fplPlayer["element_type"] ] )
                all_players.remove(xgPlayer)
                print("removed " + xgPlayer["player_name"] )
                fpl_players.remove(fplPlayer)
                print("removed " + fplPlayer["first_name"] + " " + fplPlayer["second_name"] )
                count+=1
                break

    print("close matches: ", count)
    # print(len(all_players))
    # print(len(fpl_players))

    count2 = 0 
    matchCount = 0

    reduced_all_players_copy = all_players[:]
    reduced_fpl_players_copy = fpl_players[:]

    for xgPlayer in reduced_all_players_copy:
        matchCount = 0
        matchedPlayers = []
        for fplPlayer in reduced_fpl_players_copy:

            ratio = fuzz.ratio( xgPlayer["player_name"], fplPlayer["first_name"]+ " " + fplPlayer["second_name"] )

            if ( 55 < ratio < 90 ):
                print(xgPlayer["player_name"] + " weak matches with : " + fplPlayer["first_name"] + " " + fplPlayer["second_name"] )
                matchedPlayers.append(fplPlayer)
                matchCount+=1

        if ( matchCount > 1):
            copy_matchedPlayers = matchedPlayers[:]

            maxRatio = 0
            maxRatioPlayer = None
            for matchedPlayer in copy_matchedPlayers:
                ratio = fuzz.ratio( xgPlayer["player_name"], matchedPlayer["first_name"]+ " " + matchedPlayer["second_name"] )
                if ( ratio > maxRatio ):
                    maxRatio = ratio
                    maxRatioPlayer = matchedPlayer

            print(xgPlayer["player_name"] + " has has the closest match with  : " + maxRatioPlayer["first_name"] + " " + maxRatioPlayer["second_name"])
            final_players.append( [ xgPlayer["player_name"], xgPlayer["xG"], xgPlayer["xA"], maxRatioPlayer["now_cost"], maxRatioPlayer["total_points"], xgPlayer["time"], maxRatioPlayer["element_type"] ] )
            all_players.remove(xgPlayer)
            print("removed " + xgPlayer["player_name"] )
            fpl_players.remove(maxRatioPlayer)
            print("removed " + maxRatioPlayer["first_name"] + " " + maxRatioPlayer["second_name"] )
        elif ( matchCount == 1 ):
            print(xgPlayer["player_name"] + " has has 1 closest match with  : " + matchedPlayers[0]["first_name"] + " " + matchedPlayers[0]["second_name"])
            final_players.append( [ xgPlayer["player_name"], xgPlayer["xG"], xgPlayer["xA"], matchedPlayers[0]["now_cost"], matchedPlayers[0]["total_points"], xgPlayer["time"], matchedPlayers[0]["element_type"] ] )
            all_players.remove(xgPlayer)
            print("removed " + xgPlayer["player_name"] )
            fpl_players.remove(matchedPlayers[0])
            print("removed " + matchedPlayers[0]["first_name"] + " " + matchedPlayers[0]["second_name"] )

    return final_players        


def calculatePoints(player):
    basePoints = round(float(player[5])) / 90 * 2
    pointsPerXg = 0
    pointsPerXA = 3

    if ( player[6] == 1 ) or ( player[6] == 2 ):
        pointsPerXg = 6
    elif ( player[6] == 3 ):
        pointsPerXg = 5
    elif ( player[6] == 4 ):
        pointsPerXg = 4    

    goalPoints = round(float(player[1])) * pointsPerXg
    assistPoints = round(float(player[1])) * pointsPerXA
    points = goalPoints + assistPoints + basePoints
    return points



def summary(prob):
    div = '---------------------------------------\n'
    print("Variables:\n")
    score = str(prob.objective)
    constraints = [str(const) for const in prob.constraints.values()]
    for v in prob.variables():
        score = score.replace(v.name, str(v.varValue))
        constraints = [const.replace(v.name, str(v.varValue)) for const in constraints]
        if v.varValue != 0:
            print(v.name, "=", v.varValue)
    print(div)
    print("Constraints:")
    for constraint in constraints:
        constraint_pretty = " + ".join(re.findall("[0-9\.]*\*1.0", constraint))
        if constraint_pretty != "":
            print("{} = {}".format(constraint_pretty, eval(constraint_pretty)))
    print(div)
    print("Score:")
    score_pretty = " + ".join(re.findall("[0-9\.]+\*1.0", score))
    print("{} = {}".format(score_pretty, eval(score_pretty)))    


if __name__ == '__main__':
    players = []
    availablePlayers = []
    players = getPlayers()

    for player in players:
        # print(round(float(player[1]), 2))
        # print(round(float(player[1])), 2))
        # print( player )
        points = calculatePoints(player)
        playerInfo = { "Name": player[0], "Position": str(player[6]), "Price": float(player[3]), "Points": float(points) }
        availablePlayers.append(playerInfo)

    frame = pd.DataFrame.from_dict(availablePlayers)   
    print(frame) 

    # this next bit is taken from https://medium.com/ml-everything/using-python-and-linear-programming-to-optimize-fantasy-football-picks-dc9d1229db81
    # makes little sense to me right now

    availables = frame[["Name", "Points", "Position","Price"]].groupby(["Name", "Points", "Position","Price"]).agg("count")
    availables = availables.reset_index()
    print(availables[availables.Position=="1"].head(15))

    prices = {}
    points2 = {}
    for pos in availables.Position.unique():
        available_pos = availables[availables.Position == pos]
        salary = list(available_pos[["Name","Price"]].set_index("Name").to_dict().values())[0]
        point = list(available_pos[["Name","Points"]].set_index("Name").to_dict().values())[0]
        prices[pos] = salary
        points2[pos] = point

    pos_num_available = {
    "4": 3,
    "3": 5,
    "2": 5,
    "1": 1
    }

    # print(prices)
    # print(points2.items())
    # print(points.keys())
    # print(points.items())
    # print(prices.keys())
    # print(prices.items())


    TOTAL_BUDGET = 1000

    for k, v in points2.items():
        print(k)
        print(v)
    
    _vars = {k: LpVariable.dict(k, v, cat="Binary") for k, v in points2.items()}
    print(_vars)

    prob = LpProblem("Fantasy", LpMaximize)
    rewards = []
    costs = []
    position_constraints = []
    # Setting up the reward
    for k, v in _vars.items():
        costs += lpSum([prices[k][i] * _vars[k][i] for i in v])
        rewards += lpSum([points2[k][i] * _vars[k][i] for i in v])
        prob += lpSum([_vars[k][i] for i in v]) <= pos_num_available[k]
        
    prob += lpSum(rewards)
    prob += lpSum(costs) <= TOTAL_BUDGET

    prob.solve()

    summary(prob)
