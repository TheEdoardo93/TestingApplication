import os
import pytest
import sqlite3

class TestDAO(object):
    @pytest.fixture(scope='module')
    def init_db(self, tmpdir):
        pass


    @pytest.fixture(scope='module')
    def create_connection_cursor_to_db(self):
        ### SET-UP ###
        # Define a connection to SQLite Database to the "users" table
        self.connection = sqlite3.connect('users.db')
        # cursor object
        self.cursor = self.connection.cursor()

        yield

        ### TEAR-DOWN ###
        # Close the cursor and the connection to the SQLite database
        self.cursor.close()
        self.connection.close()