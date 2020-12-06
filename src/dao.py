import os
import sqlite3

class DAO(object):
    def __init__(self, db_name):
        # Define the path where to save the SQLite3 database data
        path_to_db = '{}.db'.format(db_name)  # os.path.join('database', '{}.db'.format(db_name))

        # Define a connection to SQLite3 database (costly operation)
        self._connection = sqlite3.connect(database=path_to_db, timeout=30)
        # Define a cursor to use the SQLite3 database (not costly operation)
        self._cursor = self._connection.cursor()

    '''def drop_database(self, db_name):
        os.remove('{}.db'.format(db_name))

    def drop_table(self, table_name):
        try:
            drop_table_sql_statement=None
            if table_name == 'user':
                drop_table_sql_statement = """ DROP TABLE users;"""

            self._cursor.execute(drop_table_sql_statement)
        except Exception as e:
            print(e)'''

    def create_table(self, table_name):
        if table_name == 'users':
            create_table_sql_statement = """ CREATE TABLE users (
                                                name varchar NOT NULL,
                                                surname varchar NOT NULL,
                                                birth_place varchar NOT NULL,
                                                birth_date varchar NOT NULL,
                                                instruction_level varchar NOT NULL
                                            ); """
            try:
                self._cursor.execute(create_table_sql_statement)
            except Exception as e:
                print(e)

    def _retrieve_last_id_of_table(self, table_name):
        # Retrieve the last ID assigned to "users" table
        last_id_sql_statement = 'SELECT MAX(id) from {};'.format(table_name)
        self._cursor.execute(last_id_sql_statement)
        last_id = self._cursor.fetchone()
        print('WARN: the "{}" table in the database is empty.'.format(table_name))
        if last_id[0] is None:
            last_id = 0
        print('last_id: {}'.format(last_id))

        return last_id

    def add_row_into_table(self, object, table_name):
        if table_name == 'users':
            self._add_user_into_users_table(user=object)

    def _add_user_into_users_table(self, user):
        # Define the SQL statement to use for adding a new user in the "users" database table
        sql_statement = 'INSERT INTO users(name, surname, birth_date, birth_place, instruction_level)' + \
                        'VALUES (?, ?, ?, ?, ?);'
        self._cursor.execute(sql_statement, (user.name, user.surname, user.birth_date, user.birth_place, user.instruction_level))
        self._connection.commit()