import sqlite3
import os


class DataBaseHandler(object):
    def __init__(self, db_name):
        # Define the path where to save the SQLite3 database data
        self._path_to_db = db_name
        print('\n\npath_to_db: {}'.format(self._path_to_db))

        self._db_name = self._path_to_db.split('/')[-1]
        print('\ndb_name: {}'.format(self._db_name))

        # Create the SQLite database
        print('INFO: creating the SQLite database...')
        connection = sqlite3.connect(database=self._path_to_db, timeout=10)
        connection.close()
        print('SQLite Database created correctly to "{}".'.format(self._path_to_db))

    def destroy(self):
        print('self._path_to_db: {}'.format(self._path_to_db))
        print('INFO: destroying the SQLite database...')
        os.remove(self._path_to_db)
