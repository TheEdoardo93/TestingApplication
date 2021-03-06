import os
import sqlite3

class DAO(object):
    def __init__(self, path_to_db):
        # Define the path where to save the SQLite3 database data
        self._path_to_db = path_to_db

        # Retrieve the connection to the (already created) database
        self._connection = sqlite3.connect(database=self._path_to_db)
        self._connection.row_factory = sqlite3.Row
        self._cursor = self._connection.cursor()

    def destroy(self):
        self._cursor.close()
        self._connection.close()

    def _create_table(self, table_name):
        sql_statement=None
        if table_name == 'users':
            sql_statement = """ CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name varchar NOT NULL,
                surname varchar NOT NULL,
                birth_place varchar NOT NULL,
                birth_date varchar NOT NULL,
                instruction_level varchar NOT NULL,
                age INTEGER NOT NULL
            ); """
        elif table_name == 'courses':
            sql_statement = """ CREATE TABLE courses (
                id INTEGER PRIMARY KEY,
                name varchar NOT NULL,
                professor varchar NOT NULL,
                tutor varchar NULL,
                academic_year varchar NOT NULL,
                academic_semester varchar NOT NULL,
                credits_number INT NOT NULL,
                description varchar NULL
            ); """
        try:
            self._cursor.execute(sql_statement)
            self._connection.commit()
        except Exception as e:
            print(e)

    def _truncate_table(self, table_name):
        sql_statement = """ DELETE FROM {}; """.format(table_name)

        try:
            self._cursor.execute(sql_statement)
            self._connection.commit()
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
        elif table_name == 'courses':
            return self._add_course_into_courses_table(course=object)

    def _add_course_into_courses_table(self, course):
        # Define the SQL statement to use for adding a new course in the "courses" database table
        sql_statement = 'INSERT INTO courses(name, professor, tutor, academic_year, academic_semester, credits_number, description)' + \
                        'VALUES (?, ?, ?, ?, ?, ?, ?);'
        self._cursor.execute(sql_statement, (course.name, course.professor, course.tutor, course.academic_year,
                                             course.academic_semester, course.credits_number, course.description))
        self._connection.commit()

        # Retrieve the ID automatically assigned by SQLite database
        course_id = self._cursor.lastrowid

        return course_id

    def _add_user_into_users_table(self, user):
        # Define the SQL statement to use for adding a new user in the "users" database table
        sql_statement = 'INSERT INTO users(name, surname, birth_date, age, birth_place, instruction_level)' + \
                        'VALUES (?, ?, ?, ?, ?, ?);'
        self._cursor.execute(sql_statement, (user.name, user.surname, user.birth_date, user.age,
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
        if object_id not in [element['id'] for element in result]:
            # The particular row from a table name has not been removed correctly
            raise ValueError('There is no {} with ID equal to "{}" into the SQLite database.'.format(
                table_name[:-1], object_id))

        sql_statement = """DELETE FROM {} WHERE id = {};""".format(table_name, object_id)
        self._cursor.execute(sql_statement)
        self._connection.commit()

        sql_statement = """SELECT * FROM {};""".format(table_name)
        result = self._cursor.execute(sql_statement).fetchall()

        if object_id in [element['id'] for element in result]:
            raise ValueError('The {} with ID equal to "{}"'.format(table_name[:-1], object_id) +\
                             ' has not been removed correctly from the SQLite database.')

    def get_row_from_table(self, object, table_name):
        # Get the ID of the object to remove from a specific table in the SQLite database
        if 'id' in object:
            object_id = object['id']

        # Define the SQL statement to use for removing a specific user with ID equal to the one received
        try:
            sql_statement = """SELECT * FROM {} WHERE id = {};""".format(table_name, object_id)
            result = self._cursor.execute(sql_statement).fetchone()

            # If a specific user with ID does not exist in the SQLite database, raise a KeyError Exception
            if object_id == result['id']:
                # The particular row from a table name has been removed correctly
                # Return the description of a specific user by ID
                return {field: result[field] for field in list(result.keys()) if field != 'id'}
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

        if object_id not in [element['id'] for element in result]:
            # The particular row from a table name has not been removed correctly
            raise ValueError('There is no {} with ID equal to "{}" into the SQLite database.'.format(table_name[:-1], object_id))

        # Remove the 'id' of the user
        new_data_dict = {k: v for k, v in object.items() if k != 'id'}
        if len(new_data_dict) == 0:
            raise ValueError('No fields to update for {} with ID equal to "{}"'.format(table_name[:-1], object_id) +\
                             ' has been received by the server.')

        # Define the portion of the SQL DML statement for updating the user field(s)
        update_values_stmt = _prepare_sql_update_statement(new_data_dict=new_data_dict)

        # Update the found user with new data values
        sql_statement = """UPDATE {} SET {} WHERE id = {};""".format(table_name, update_values_stmt, object_id)
        self._cursor.execute(sql_statement)
        self._connection.commit()

        # Check the update operation has been done successfully
        sql_statement = """SELECT * FROM {} WHERE id = {};""".format(table_name, object_id)
        result = self._cursor.execute(sql_statement).fetchone()

        for field, new_value in new_data_dict.items():
            if result[field] != new_value:
                raise AttributeError
