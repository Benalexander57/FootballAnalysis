# Tutorial from http://www.fantasyfutopia.com/python-for-fantasy-football-getting-and-cleaning-data/

# Import the libraries we need
import pandas as pd
import re
import random
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime

def scrapeUnderstat():

	# Set the url we want
	xg_url = 'https://understat.com/league/EPL'
	 
	# # Use requests to download the webpage
	# xg_data = requests.get(xg_url)
	 
	# # Get the html code for the webpage
	# xg_html = xg_data.content
	 
	# # Parse the html using bs4
	# soup = BeautifulSoup(xg_html, 'lxml')

	# Set up the Selenium driver (in this case I am using the Chrome browser)
	options = webdriver.ChromeOptions()
	 
	# 'headless' means that it will run without opening a browser
	# If you don't set this option, Selenium will open up a new browser window (try it out if you like)
	options.add_argument('headless')
	 
	# Tell the Selenium driver to use the options we just specified
	driver = webdriver.Chrome(chrome_options=options)
	 
	# Tell the driver to navigate to the page url
	driver.get(xg_url)
	 
	# Grab the html code from the webpage
	soup = BeautifulSoup(driver.page_source, 'lxml')
	 
	# It's good practice to try and put any extra code inside a new cell, so you don't have to make a request to the page more than once
	# If you keep running this cell it will make a new request to the site every time
	1
	2
	3
	4
	5
	# Feel free to uncomment the line below and print out the soup if you want to see what it looks like
	# print(soup.prettify())
	# I'm not going to do that here because it will basically just print the html code for the entire webpage!
	# Instead, let's just print the page title
	# print(soup.title)

	# Get the table headers using 3 chained find operations
	# 1. Find the div containing the table (div class = chemp jTable)
	# 2. Find the table within that div
	# 3. Find all 'th' elements where class = sort
	headers = soup.find('div', attrs={'class':'chemp jTable'}).find('table').find_all('th',attrs={'class':'sort'})

	# Iterate over headers, get the text from each item, and add the results to headers_list
	headers_list = []
	for header in headers:
	    headers_list.append(header.get_text(strip=True))

	# You can also simply call elements like tables directly instead of using find('table') if you are only looking for the first instance of that element
	body = soup.find('div', attrs={'class':'chemp jTable'}).table.tbody
	 
	# Create a master list for row data
	all_rows_list = []
	# For each row in the table body
	for tr in body.find_all('tr'):
	    # Get data from each cell in the row
	    row = tr.find_all('td')
	    # Create list to save current row data to
	    current_row = []
	    # For each item in the row variable
	    for item in row:
	        # Add the text data to the current_row list
	        current_row.append(item.get_text(strip=True))
	    # Add the current row data to the master list    
	    all_rows_list.append(current_row)
	 
	# Create a dataframe where the rows = all_rows_list and columns = headers_list
	xg_df = pd.DataFrame(all_rows_list, columns=headers_list)




	playerHeaders = soup.find('div', attrs={'class':'players jTable'}).find('table').find_all('th',attrs={'class':'sort'})

	player_headers_list = []
	for header in playerHeaders:
	    player_headers_list.append(header.get_text(strip=True))

	# You can also simply call elements like tables directly instead of using find('table') if you are only looking for the first instance of that element
	playerBody = soup.find('div', attrs={'class':'players jTable'}).table.tbody

	# Create a master list for row data
	all_player_rows_list = []
	# For each row in the table body
	for tr in playerBody.find_all('tr'):
	    # Get data from each cell in the row
	    row = tr.find_all('td')
	    # Create list to save current row data to
	    current_row = []
	    # For each item in the row variable
	    for item in row:
	        # Add the text data to the current_row list
	        current_row.append(item.get_text(strip=True))
	    # Add the current row data to the master list    
	    all_player_rows_list.append(current_row)
	 
	# Create a dataframe where the rows = all_rows_list and columns = headers_list
	# xg_df = pd.DataFrame(all_player_rows_list, columns=player_headers_list)


	all_scripts = soup.find_all('script')

	all_players = []
	players = []

	for script in all_scripts:
	    if script.find(text=re.compile("var playersData")):
	        m = script.text
	        n = m[m.find("(")+1:m.find(")")]
	        o = n.replace("'","" )	
	        q = o.encode('utf8')
	        players = q.decode('unicode-escape')
	        
	        players = json.loads(players)
	        # for player in players:
	        # 	current_player = [player["id"], player["player_name"], player["games"], player["time"], player["goals"], player["xG"], player["assists"], player["xA"], player["shots"], player["key_passes"], 
	        # 	player["yellow_cards"], player["red_cards"], player["position"], player["team_title"], player["npg"], player["npxG"], player["xGChain"], player["xGBuildup"]]
	        # 	all_players.append(current_player)
	        # break

	all_players_xg_header = ["id", "player_name", "games", "time", "goals", "xG", "assists", "xA", "shots", "key_passes", 
	        	"yellow_cards", "red_cards", "position", "team_title", "npg", "npxG", "xGChain", "xGBuildup"] 

	# all_players_xg = pd.DataFrame(all_players, columns = all_players_xg_header)   

	# return all_players     
	return players     









#loop through all https://understat.com/player/7276 players


