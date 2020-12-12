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

    def delete_row_from_table(self, object, table_name):
        # Get the ID of the object to remove from a specific table in the SQLite database
        if 'id' in object:
            object_id = object['id']

        # Define the SQL statement to use for removing a specific user with ID equal to the one received
        sql_statement = """SELECT * FROM {};""".format(table_name)
        result = self._cursor.execute(sql_statement).fetchall()
        if object_id not in [element[0] for element in result]:
            # The particular row from a table name has not been removed correctly
            raise ValueError('There is no user with ID equal to "{}" into the SQLite database.'.format(object_id))

        sql_statement = """DELETE FROM {} WHERE id = {};""".format(table_name, object_id)
        self._cursor.execute(sql_statement)
        self._connection.commit()

        sql_statement = """SELECT * FROM {};""".format(table_name)
        result = self._cursor.execute(sql_statement).fetchall()

        if object_id in [element[0] for element in result]:
            raise ValueError('The user with ID equal to "{}" has not been removed correctly from the SQLite database.')

    def get_row_from_table(self, object, table_name):
        # Get the ID of the object to remove from a specific table in the SQLite database
        if 'id' in object:
            object_id = object['id']

        # Define the SQL statement to use for removing a specific user with ID equal to the one received
        try:
            sql_statement = """SELECT * FROM {} WHERE id = {};""".format(table_name, object_id)
            result = self._cursor.execute(sql_statement).fetchone()

            # If a specific user with ID does not exist in the SQLite database, raise a KeyError Exception
            if object_id == result[0]:
                # The particular row from a table name has been removed correctly
                # Return the description of a specific user by ID
                return {'name': result[1], 'surname': result[2], 'birth_place': result[3],
                        'birth_date': result[4], 'instruction_level': result[5]}
            else:
                # The particular row from a table name has not been removed correctly
                raise KeyError('ERROR: there is no {} with ID equal to "{}"'.format(table_name[:-1], object_id) + \
                               ' in the "{}" table of the SQLite database.'.format(table_name))

        except Exception as e:
            raise ValueError

    def update_row_in_table(self, table_name, object):
        def _prepare_sql_update_statement(new_data_dict):
            update_values_stmt = ''
            for k, v in new_data_dict.items():
                update_values_stmt += '{} = "{}", '.format(k, v)
            update_values_stmt = update_values_stmt.rstrip(', ')

            return update_values_stmt

        # Get the ID of the object to remove from a specific table in the SQLite database
        if 'id' in object:
            object_id = object['id']

        # Define the SQL statement to use for removing a specific user with ID equal to the one received
        sql_statement = """SELECT * FROM {};""".format(table_name)
        result = self._cursor.execute(sql_statement).fetchall()
        if object_id not in [element[0] for element in result]:
            # The particular row from a table name has not been removed correctly
            raise ValueError('There is no user with ID equal to "{}" into the SQLite database.'.format(object_id))

        # Remove the 'id' of the user
        new_data_dict = {k: v for k, v in object.items() if k != 'id'}
        if len(new_data_dict) == 0:
            raise ValueError('No fields to update for user with ID equal to "{}"'.format(object_id) +\
                             ' has been received by the server.')

        # Define the portion of the SQL DML statement for updating the user field(s)
        update_values_stmt = _prepare_sql_update_statement(new_data_dict=new_data_dict)

        # Update the found user with new data values
        sql_statement = """UPDATE {} SET {} WHERE id = {};""".format(table_name, update_values_stmt, object_id)
        self._cursor.execute(sql_statement)
        self._connection.commit()

        sql_statement = """SELECT * FROM {} WHERE id = {};""".format(table_name, object_id)
        result = self._cursor.execute(sql_statement).fetchone()

        support_dict = {'id': 0, 'name': 1, 'surname': 2, 'birth_place': 3, 'birth_date': 4, 'instruction_level': 5}
        for field, new_value in new_data_dict.items():
            if result[support_dict[field]] != new_value:
                raise AttributeError
