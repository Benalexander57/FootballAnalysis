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

		elif script.find(text=re.compile("var teamsData")):
			m = script.text
			n = m[m.find("(")+1:m.find(")")]
			o = n.replace("'","" )	
			q = o.encode('utf8')
			teams = q.decode('unicode-escape')
	        
			teams = json.loads(teams)



	return players




# for more detailed stats on each player
#loop through all https://understat.com/player/7276 players


