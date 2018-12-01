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

    print (len(all_players))
    print (len(fpl_players))

    # print (all_players[0])
    # print (fpl_players[0])
    count = 0
    count2 = 0 

    for xgPlayer in all_players:
     	for fplPlayer in fpl_players:
     		# print(xgPlayer["player_name"])
     		# print(fplPlayer["first_name"])
     		# print(fplPlayer["second_name"])

     		ratio = fuzz.ratio( xgPlayer["player_name"], fplPlayer["first_name"]+ " " + fplPlayer["second_name"] )

     		if ( ratio > 80 ):
     			print("test")
     			print(xgPlayer["player_name"] + " close matches with : " + fplPlayer["first_name"] + " " + fplPlayer["second_name"] )
     			count+=1

     		if ( 70 < ratio < 80 ):
     			print("test")
     			print(xgPlayer["player_name"] + " weak matches with : " + fplPlayer["first_name"] + " " + fplPlayer["second_name"] )
     			count2+=1	

	
    print("close matches: ", count)
    print("iffy matches: ", count2)



