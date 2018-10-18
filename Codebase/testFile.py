import sqlite3
import variables
from databaseOperations import insert_competition, check_duplicate_competition
from sqlite3 import Error
from createDatabase import create_connection, close_connection
from competition import create_competition
from jsonOperations import readCompetitions, readMatches

def main():
    connection = create_connection(variables.database_location)
    bool = check_duplicate_competition(connection, 50)
    print( bool )
     
if __name__ == '__main__':
    main()