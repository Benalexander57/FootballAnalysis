# Import the libraries we need
import pandas as pd
import re
import random
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime

# Set the url we want
url = 'https://fantasy.premierleague.com/drf/bootstrap-static'
response = requests.get(url)
response_data = response.json()
all_players_list = response_data["elements"]

price_list = []
for player in all_players_list:
	current_player = [player["first_name"], player["second_name"], player["now_cost"]]
	price_list.append(current_player)

# print(all_players_list)	

all_players_price = pd.DataFrame(price_list, columns = ["First name", "Last name", "Price £"]) 

all_players_price