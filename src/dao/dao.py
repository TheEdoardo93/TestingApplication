import os
import sqlite3

class DAO(object):
    def __init__(self, path_to_db):
        # Define the path where to save the SQLite3 database data
        self._path_to_db = path_to_db

        # Retrieve the connection to the (already created) database
        self._connection = sqlite3.connect(database=self._path_to_db)
        self._cursor = self._connection.cursor()

    def destroy(self):
        self._cursor.close()
        self._connection.close()

    def _create_table(self, table_name):
        if table_name == 'users':
            sql_statement = """ CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name varchar NOT NULL,
                surname varchar NOT NULL,
                birth_place varchar NOT NULL,
                birth_date varchar NOT NULL,
                instruction_level varchar NOT NULL
            ); """

        print('CREATING NEW users TABLE...')
        try:
            self._cursor.execute(sql_statement)
        except Exception as e:
            print(e)

    def _truncate_table(self, table_name):
        if table_name == 'users':
            sql_statement = """ DELETE FROM users; """

        print('TRUNCATING EXISTING users TABLE...')
        try:
            self._cursor.execute(sql_statement)
        except Exception as e:
            print(e)

    def create_table(self, table_name):
        # Check whether the table already exists or not
        result = self._cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

        # Get the already existing tables in the SQLite database
        already_existing_table_names = [table_name[0] for table_name in result]
        if len(result) == 0 or table_name not in already_existing_table_names:
            # empty database or the database exists but the table does not exist
            self._create_table(table_name=table_name)
        else:
            # truncate table
            self._truncate_table(table_name=table_name)

    def add_row_into_table(self, object, table_name):
        if table_name == 'users':
            return self._add_user_into_users_table(user=object)

    def _add_user_into_users_table(self, user):
        # Define the SQL statement to use for adding a new user in the "users" database table
        sql_statement = 'INSERT INTO users(name, surname, birth_date, birth_place, instruction_level)' + \
                        'VALUES (?, ?, ?, ?, ?);'
        self._cursor.execute(sql_statement, (user.name, user.surname, user.birth_date,
                                             user.birth_place, user.instruction_level))
        self._connection.commit()

        # Retrieve the ID automatically assigned by SQLite database
        user_id = self._cursor.lastrowid

        return user_id
