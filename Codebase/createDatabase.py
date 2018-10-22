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
                                        index integer,
                                        matchId integer,
                                        lastUpdatedDt text,
                                        timeStamp text,
                                        duration text,
                                        period integer,
                                        minute integer,
                                        second integer,
                                        sequence text,
                                        teamSequence text,
                                        period text,
                                        teamId integer,
                                        opponentId integer,
                                        playerId integer,
                                        player2Id integer,
                                        positionX text,
                                        positionY text,
                                        position2X text,
                                        position2Y text,
                                        goalPositionY text,
                                        goalPositionZ text,
                                        possessionId integer,
                                        possessionTeamId integer,
                                        possessionOppId integer
                                    ); """


    sql_create_ballRecovery_table = """ CREATE TABLE IF NOT EXISTS ballRecovery (
                                        id integer PRIMARY KEY,
                                        eventFk integer NOT NULL,
                                        offensiveFl integer,
                                        recoveryFailureFl integer
                                    ); """   


    sql_create_block_table = """ CREATE TABLE IF NOT EXISTS block (
                                        id integer PRIMARY KEY,
                                        eventId integer NOT NULL,
                                        deflectionFl integer,
                                        offensiveFl integer,
                                        saveBlockFl integer,
                                        outFl integer,
                                        outcome integer,
                                        outcomeName text
                                    ); """      
                                    

    sql_create_dribble_table = """ CREATE TABLE IF NOT EXISTS dribble (
                                        id integer PRIMARY KEY,
                                        eventFk integer NOT NULL,
                                        overrunFl integer,
                                        nutmegFl integer,
                                        outcome integer,
                                        outcomeName text
                                    ); """      


     sql_create_foulCommitted_table = """ CREATE TABLE IF NOT EXISTS foulCommitted (
                                        id integer PRIMARY KEY,
                                        eventFk integer NOT NULL,
                                        offensiveFl integer,
                                        type integer,
                                        outcome integer,
                                        outcomeName text,
                                        advantageFl integer,
                                        penaltyFl integer,
                                        card integer,
                                        cardName text
                                    ); """      
                                    

    sql_create_foulWon_table = """ CREATE TABLE IF NOT EXISTS foulWon (
                                        id integer PRIMARY KEY,
                                        eventFk integer NOT NULL,
                                        defensiveFl integer,
                                        advantageFl integer,
                                        penaltyFl integer,
                                    ); """      


    sql_create_goalkeeperEvent_table = """ CREATE TABLE IF NOT EXISTS goalkeeperEvent (
                                        id integer PRIMARY KEY,
                                        eventFk integer NOT NULL,
                                        position integer,
                                        positionName text,
                                        technique integer,
                                        techniqueName text,
                                        bodyPart integer,
                                        bodyPartName text,
                                        type integer,
                                        typeName text,
                                        outcome integer,
                                        outcome text
                                    ); """      

    sql_create_injuryStoppage_table = """ CREATE TABLE IF NOT EXISTS injuryStoppage (
                                        id integer PRIMARY KEY,
                                        eventFk integer NOT NULL,
                                        inChain integer
                                    ); """  

    sql_create_pass_table = """ CREATE TABLE IF NOT EXISTS pass (
                                        id integer PRIMARY KEY,
                                        eventFk integer NOT NULL,
                                        recipientId integer,
                                        length real,
                                        angle real,
                                        height integer,
                                        heightName text,
                                        endLocationX integer,
                                        endLocationY integer,
                                        assistedShotId integer,
                                        backheelFl integer,
                                        angle real,
                                        deflectedFl integer,
                                        miscommunicationFl integer,
                                        throughBallFl integer,
                                        crossFl integer,
                                        cutbackFl integer,
                                        switchFl integer,
                                        shotAssistFl integer,
                                        goalAssistFl integer,
                                        bodyPart integer,
                                        bodyPartName text,
                                        type integer,
                                        typeName text,
                                        outcome integer,
                                        outcomeName text
                                    ); """  

    sql_create_shot_table = """ CREATE TABLE IF NOT EXISTS shot (
                                        id integer PRIMARY KEY,
                                        eventFk integer NOT NULL,
                                        keyPassId integer,
                                        endLocationX integer,
                                        endLocationY integer,
                                        endLocationZ integer,
                                        followDribbleFl integer,
                                        deadball integer,
                                        deadballName text,
                                        firstTimeFl integer,
                                        redirectFl integer,
                                        oneOnOneFl integer,
                                        openGoalFl integer,
                                        statsBombxG real,
                                        technique integer,
                                        techniqueName text,
                                        deflectedFl integer,
                                        bodyPart integer,
                                        bodyPartName text,
                                        outcome integer,
                                        outcome text,
                                        bodyPartName text
                                    ); """  

    sql_create_substitution_table = """ CREATE TABLE IF NOT EXISTS substitution (
                                        id integer PRIMARY KEY,
                                        eventFk integer NOT NULL,
                                        replacementId integer,
                                        replacementName text,
                                        outcome integer,
                                        outcome text
                                    ); """  

    sql_create_clearance_table = """ CREATE TABLE IF NOT EXISTS clearance (
                                        id integer PRIMARY KEY,
                                        eventFk integer NOT NULL,
                                        aerialWonFl integer
                                    ); """  

    sql_create_miscontrol_table = """ CREATE TABLE IF NOT EXISTS miscontrol (
                                        id integer PRIMARY KEY,
                                        eventFk integer NOT NULL,
                                        aerialWonFl integer
                                    ); """ 

    sql_create_duel_table = """ CREATE TABLE IF NOT EXISTS duel (
                                        id integer PRIMARY KEY,
                                        eventFk integer NOT NULL,
                                        type integer,
                                        typeName text,
                                        outcome integer,
                                        outcomeName text
                                    ); """                                     

    sql_create_inteception_table = """ CREATE TABLE IF NOT EXISTS interception (
                                        id integer PRIMARY KEY,
                                        eventFk integer NOT NULL,
                                        outcome integer,
                                        outcome text
                                    ); """ 

    sql_create_badBehaviour_table = """ CREATE TABLE IF NOT EXISTS badBehaviour (
                                        id integer PRIMARY KEY,
                                        eventFk integer NOT NULL,
                                        card integer,
                                        cardName text
                                    ); """ 


    # lineup table - matchId, teamId,  PlayerId, 
    
    # player table - playerId, name, number, countryId, teamId

    # country table - id, name                                                                                                                  


    if ( conn is not None ):
    	create_table(conn, sql_create_competition_table)
    	create_table(conn, sql_create_match_table)
    	create_table(conn, sql_create_team_table)
    	create_table(conn, sql_create_season_table)
    	create_table(conn, sql_create_lineup_table)
    	create_table(conn, sql_create_player_table)
    	create_table(conn, sql_create_country_table)
        create_table(conn, sql_create_event_table)
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