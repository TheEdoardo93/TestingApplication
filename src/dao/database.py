import sqlite3
import os


class DataBaseHandler(object):
    def __init__(self, db_name):
        # Define the path where to save the SQLite3 database data
        self._path_to_db = db_name

        # Create the SQLite database
        print('INFO: creating the SQLite database...')
        self._connection = sqlite3.connect(database=self._path_to_db)

        print('SQLite Database created correctly to "{}".'.format(self._path_to_db))

    def destroy(self):
        print('INFO: destroying the SQLite database...')
        self._connection.close()
        #os.remove(self._path_to_db)
