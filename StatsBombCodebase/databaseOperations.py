import sqlite3
import variables
from sqlite3 import Error
from createDatabase import create_connection, close_connection
from competition import create_competition

def insert_competition(connection, competition):
    """
    Create a new competition into the competition table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO competition(competitionId, seasonId, countryName, competitionName, seasonName, matchUpdatedDttm, matchAvailableDttm)
              VALUES(?,?,?,?,?,?,?) '''
    cur = connection.cursor()
    cur.execute(sql, competition)
    return cur.lastrowid

def insert_match(connection, match):    
    sql = ''' INSERT INTO match(matchId, matchDate, kickOff, competitionId, seasonId, homeTeamId, awayTeamId, homeScore, awayScore, stadiumName, refereeName, matchStatus, lastUpdated, dataVersion)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = connection.cursor()
    cur.execute(sql, match)
    return cur.lastrowid

def insert_team(connection, team):      
    sql = ''' INSERT INTO team( teamId, teamName)
              VALUES(?,?) '''
    cur = connection.cursor()
    cur.execute(sql, team)
    return cur.lastrowid

def insert_season(connection, season):
    sql = ''' INSERT INTO season(seasonId, seasonName)
              VALUES(?,?) '''
    cur = connection.cursor()
    cur.execute(sql, season)
    return cur.lastrowid

def insert_lineup(connection, lineup):
    sql = ''' INSERT INTO lineup(matchId, teamId, playerId)
              VALUES(?,?,?) '''
    cur = connection.cursor()
    cur.execute(sql, lineup)
    return cur.lastrowid

def insert_player(connection, player):
    sql = ''' INSERT INTO player( playerId, name, number, countryId, teamId)
              VALUES(?,?,?,?,?) '''
    cur = connection.cursor()
    cur.execute(sql, player)
    return cur.lastrowid    

def insert_event(connection, event):
    sql = ''' INSERT INTO event( playerId, name, number, countryId, teamId)
              VALUES(?,?,?,?,?) '''
    cur = connection.cursor()
    cur.execute(sql, event)
    return cur.lastrowid   


def check_duplicate_competition(connection, competitionId):
    cursor = connection.cursor()
    cursor.execute("SELECT competitionId FROM competition WHERE competitionId = ?", ( competitionId,))
    data=cursor.fetchone()
    if data is None:
        return False
    else:
        return True   

def check_duplicate_match(connection, matchId):
    cursor = connection.cursor()
    cursor.execute("SELECT matchId FROM match WHERE matchId = ?", ( matchId,))
    data=cursor.fetchone()
    if data is None:
        return False
    else:
        return True        

def check_duplicate_team(connection, teamId):
    cursor = connection.cursor()
    cursor.execute("SELECT teamId FROM team WHERE teamId = ?", ( teamId,))
    data=cursor.fetchone()
    if data is None:
        return False
    else:
        return True

def check_duplicate_season(connection, seasonId):
    cursor = connection.cursor()
    cursor.execute("SELECT seasonId FROM season WHERE seasonId = ?", ( seasonId,))
    data=cursor.fetchone()
    if data is None:
        return False
    else:
        return True   

def check_duplicate_lineup(connection, matchId, teamId, playerId):
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM lineup WHERE matchId = ? AND teamId = ? AND playerId = ?", ( matchId, teamId, playerId))
    data=cursor.fetchone()
    if data is None:
        return False
    else:
        return True      

def check_duplicate_player(connection, playerId):
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM player WHERE playerId = ?", ( playerId,))
    data=cursor.fetchone()
    if data is None:
        return False
    else:
        return True                                  