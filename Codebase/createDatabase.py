import sqlite3
from sqlite3 import Error
import variables

def main():

    sql_create_competition_table = """ CREATE TABLE IF NOT EXISTS competition (
                                        id integer PRIMARY KEY,
                                        competitionId integer NOT NULL,
                                        seasonId integer NOT NULL,
                                        countryName text,
                                        competitionName text,
                                    	seasonName text,
                                    	matchUpdatedDttm text,
                                    	matchAvailableDttm text
                                    ); """

    sql_create_match_table = """ CREATE TABLE IF NOT EXISTS match (
                                        id integer PRIMARY KEY,
                                        matchId integer,
                                        matchDate text,
                                        kickOff text,
                                        competitionId integer,
                                        seasonId integer,
                                    	homeTeamId integer,
                                    	awayTeamId text,
                                    	homeScore integer,
                                    	awayScore integer,
                                    	stadiumName text,
                                    	refereeName text,
                                    	matchStatus text,
                                    	lastUpdated text,
                                    	dataVersion text
                                    ); """

    sql_create_team_table = """ CREATE TABLE IF NOT EXISTS team (
                                        id integer PRIMARY KEY,
                                        teamId integer NOT NULL,
                                    	teamName text
                                    ); """         

    sql_create_season_table = """ CREATE TABLE IF NOT EXISTS season (
                                        id integer PRIMARY KEY,
                                        seasonId integer NOT NULL,
                                    	seasonName text
                                    ); """    

    sql_create_lineup_table = """ CREATE TABLE IF NOT EXISTS lineup (
                                        id integer PRIMARY KEY,
                                        matchId integer,
                                        teamId integer,
                                        playerId integer
                                    ); """

    sql_create_player_table = """ CREATE TABLE IF NOT EXISTS player (
                                        id integer PRIMARY KEY,
                                        playerId integer NOT NULL,
                                        name integer,
                                        number integer,
                                        countryId integer,
                                        teamId integer
                                    ); """

    sql_create_country_table = """ CREATE TABLE IF NOT EXISTS country (
                                        id integer PRIMARY KEY,
                                        countryId integer,
                                        name integer
                                    ); """


    #event table then a table for each event typ elike pass/tackle etc with the extra info
    sql_create_event_table = """ CREATE TABLE IF NOT EXISTS eventType (
                                        id integer PRIMARY KEY,
                                        identifier text NOT NULL,
                                        matchId integer,
                                        description integer,
                                        attributeGroup integer,
                                        attribute integer,
                                        attributeDescription integer
                                    ); """                                    
    # lineup table - matchId, teamId,  PlayerId, 
    
    # player table - playerId, name, number, countryId, teamId

    # country table - id, name                                                                                                                  


    conn = create_connection(variables.database_location)
    if ( conn is not None ):
    	create_table(conn, sql_create_competition_table)
    	create_table(conn, sql_create_match_table)
    	create_table(conn, sql_create_team_table)
    	create_table(conn, sql_create_season_table)
    	create_table(conn, sql_create_lineup_table)
    	create_table(conn, sql_create_player_table)
    	create_table(conn, sql_create_country_table)
    	close_connection(conn)

    else:
    	print("ERROR - Could not create database connection")
  
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    global conn

    try:
        conn = sqlite3.connect(db_file)
        print("Opened database connection")
        return conn
    except Error as e:
        print(e)
    return None

def close_connection(connection):
	connection.close()
	print("Closed database connection")

def create_table(connection, table_name):
    """ add the competition table to the database """
    try:
    	c = conn.cursor()
    	c.execute( table_name )
    	print("Created table " + table_name)
    except Error as e:
        print(e)
 
if __name__ == '__main__':
    main()