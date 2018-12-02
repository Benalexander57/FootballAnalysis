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

    # print (all_players)
    # print (fpl_players)


    # print (all_players[0])
    # print (fpl_players[0])
    count = 0
    count2 = 0 



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
                print("removed" + fplPlayer["first_name"] + " " + fplPlayer["second_name"] )
                count+=1
                break
                # matched = True

        #     if ( matched ):
        #         break    

        # if ( matched ):
        #     all_players.remove(xgPlayer)

    print("close matches: ", count)


    # for xgPlayer in all_players:
    #     for fplPlayer in fpl_players:
    #         if ( 70 < ratio < 80 ):
    #             print(xgPlayer["player_name"] + " weak matches with : " + fplPlayer["first_name"] + " " + fplPlayer["second_name"] )
    #             count2+=1	


    # print("not close matches: ", count2)				




