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


if __name__ == '__main__':
    all_players = scrapeUnderstat()
    fpl_players = scrapeFPL()

    all_players_copy = all_players[:]
    fpl_players_copy = fpl_players[:]

    print (len(all_players))
    print (len(fpl_players))

    count = 0

    # first pass through the players which closely match 
    for xgPlayer in all_players_copy:
        # matched = False
        for fplPlayer in fpl_players_copy:
     		# print(xgPlayer["player_name"])
     		# print(fplPlayer["first_name"])
     		# print(fplPlayer["second_name"])

            ratio = fuzz.ratio( xgPlayer["player_name"], fplPlayer["first_name"]+ " " + fplPlayer["second_name"] )

            if ( ratio > 90 ):
                print(xgPlayer["player_name"] + " close matches with : " + fplPlayer["first_name"] + " " + fplPlayer["second_name"] )
                all_players.remove(xgPlayer)
                print("removed " + xgPlayer["player_name"] )
                fpl_players.remove(fplPlayer)
                print("removed " + fplPlayer["first_name"] + " " + fplPlayer["second_name"] )
                count+=1
                break

    print("close matches: ", count)
    print(len(all_players))
    print(len(fpl_players))

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
            all_players.remove(xgPlayer)
            print("removed " + xgPlayer["player_name"] )
            fpl_players.remove(maxRatioPlayer)
            print("removed " + maxRatioPlayer["first_name"] + " " + maxRatioPlayer["second_name"] )
        elif ( matchCount == 1 ):
            print(xgPlayer["player_name"] + " has has 1 closest match with  : " + matchedPlayers[0]["first_name"] + " " + matchedPlayers[0]["second_name"])
            all_players.remove(xgPlayer)
            print("removed " + xgPlayer["player_name"] )
            fpl_players.remove(matchedPlayers[0])
            print("removed " + matchedPlayers[0]["first_name"] + " " + matchedPlayers[0]["second_name"] )



    # print("not close matches: ", count2)				

    print(len(all_players))
    print(len(fpl_players))
    print(all_players)


