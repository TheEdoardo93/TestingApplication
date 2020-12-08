import pytest
import configparser
import os

from src.model.user import User
from src.dao.dao import DAO
from src.dao.database import DataBaseHandler
from src.api.app import InitFlaskApp
from utils.configuration_utils import ConfigurationsUtils

@pytest.fixture(scope='session', name='init_sqlite3_db')
def init_sqlite3_db(tmpdir_factory):
    ### SET-UP ###
    # Read the init_config_test.cfg file which contains the path to the SQLite database
    cfg_handler = ConfigurationsUtils()

    # Split the path to the SQLite database used for test purposes to its directories and sub-directories
    main_dir, sub_dir = cfg_handler._path_to_sqlite_database.split('/')[1:]

    # Add a sub-directory whose name is read from "init_config_test.cfg" file where to save the SQLite database
    path_to_tmp_db_directory = tmpdir_factory.mktemp(basename=main_dir, numbered=False).mkdir(sub_dir)\
        .join(cfg_handler._database_name)

    # Save in a temporary file called "tmp.txt" the path to the test SQLite database (removed at the end of tests)
    with open('tmp.txt', 'w') as output_file:
        output_file.write(str(path_to_tmp_db_directory)+'\n')

    # Create a SQLite3 database one-shot
    database_handler = DataBaseHandler(db_name=path_to_tmp_db_directory)

    yield database_handler

    ### TEAR-DOWN ###
    database_handler.destroy()
    os.remove('tmp.txt') # file where to save the path to the SQLite database


@pytest.fixture(scope='session', name='init_sqlite3_db_connection')
def init_sqlite3_db_connection(init_sqlite3_db):
    ### SET-UP ###

    dao_handler = DAO(path_to_db=init_sqlite3_db._path_to_db)

    yield dao_handler

    ### TEAR-DOWN ###
    dao_handler.destroy()


@pytest.fixture(scope='function', name='init_users_db_table')
def create_users_table_in_db(init_sqlite3_db, init_sqlite3_db_connection):
    ### SET-UP ###
    dao_handler = init_sqlite3_db_connection
    dao_handler.create_table(table_name='users')

    yield

    ### TEAR-DOWN ###
    print('teardown init_users_db_table')
    #@TODO: drop table in the database

###################################################################

@pytest.fixture(scope='module', name='return_new_users_correctly')
def return_new_users_correctly():
    new_users_correct = [User(name='Edoardo', surname='Casiraghi', birth_date='25/04/1993', birth_place='Merate',
                              instruction_level='University'),
                         User(name='Veronica', surname='Lanzi', birth_date='01/05/1994', birth_place='Lecco',
                              instruction_level='University'),
                         User(name='Danilo', surname='Casiraghi', birth_date='11/10/1961', birth_place='Vimercate',
                              instruction_level='High School'),
                         User(name='Daniela', surname='Bonalume', birth_date='18/02/1963', birth_place='Merate',
                              instruction_level='Middle School')]

    return new_users_correct

@pytest.fixture(scope='module', name='init_flask_app')
def init_flask_app(init_sqlite3_db):
    flask_handler = InitFlaskApp()
    flask_app = flask_handler.create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client # this is where the testing happens!

@pytest.fixture(scope='function', name='examples_users_db_table')
def create_users_table_in_db_with_test_users_already_added(init_sqlite3_db, init_sqlite3_db_connection,
                                                           return_new_users_correctly):
    ### SET-UP ###
    dao_handler = init_sqlite3_db_connection
    ### STEP 1: create an empty "users" table ###
    dao_handler.create_table(table_name='users')

    ### STEP 2: # add some test users in the "users" table ###
    for index, user in enumerate(return_new_users_correctly):
        # Add a user and retrieve him/her ID
        user_id = dao_handler.add_row_into_table(object=user, table_name='users')
        assert (user_id == index + 1)

    yield

    ### TEAR-DOWN ###
    print('teardown init_users_db_table')
    #@TODO: drop table in the database