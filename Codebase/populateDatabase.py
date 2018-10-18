import sqlite3
import variables
import os
import sys
import json
from databaseOperations import insert_competition, insert_match, insert_season, insert_team, check_duplicate_competition, check_duplicate_match, check_duplicate_team, check_duplicate_season
from sqlite3 import Error
from createDatabase import create_connection, close_connection
from competition import create_competition
from jsonOperations import readCompetitions, readMatches


def populateDatabase():

    connection = create_connection(variables.database_location)

    competitions = readCompetitions()
    for competition in competitions:
        with connection:
            if not check_duplicate_competition( connection, competition["competition_id"]): 
                id = insert_competition(connection, (competition["competition_id"], competition["season_id"], competition["country_name"], competition["competition_name"], competition["season_name"], competition["match_updated"], competition["match_available"]))
                print("id " + str(id) + " Inserted")

    jsonFiles = readMatches()
    for matches in jsonFiles:
        for match in matches:
            with connection:

                if not check_duplicate_match( connection, match["match_id"]):
                    id = insert_match(connection, (match["match_id"], match["match_date"], match["kick_off"], match["competition"]["competition_id"], match["season"]["season_id"], match["home_team"]["home_team_id"], match["away_team"]["away_team_id"], match["home_score"], match["away_score"], match["stadium_name"], match["referee_name"], match["match_status"], match["last_updated"], match["data_version"]))
                    print("id " + str(id) + " Inserted") 

                if not check_duplicate_team( connection, match["home_team"]["home_team_id"]): 
                    id = insert_team(connection, (match["home_team"]["home_team_id"], match["home_team"]["home_team_name"] ))
                    print("id " + str(id) + " Inserted") 
            
                if not check_duplicate_team( connection, match["away_team"]["away_team_id"]):
                    id = insert_team(connection, (match["away_team"]["away_team_id"], match["away_team"]["away_team_name"] ))
                    print("id " + str(id) + " Inserted")

                if not check_duplicate_season( connection, match["season"]["season_id"]): 
                    id = insert_season(connection, (match["season"]["season_id"], match["season"]["season_name"] ))
                    print("id " + str(id) + " Inserted")  


    directory = os.fsencode(variables.lineups_location)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"): 
            with open(os.path.join(directory, file), encoding='utf-8') as matchFile:
                data = json.load(matchFile)
                print(data)
                                        

    close_connection(connection)

if __name__ == '__main__':
    populateDatabase()