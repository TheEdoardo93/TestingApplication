import pytest

from src.model.user import User
from src.dao.dao import DAO
from src.api.app import InitFlaskApp

@pytest.fixture(scope='session', name='init_sqlite3_db')
def init_sqlite3_db(tmpdir_factory):
    ### SET-UP ###
    path_to_db = '{}/test_DB'.format(tmpdir_factory.getbasetemp())
    # Create a SQLite3 database one-shot
    dao_handler = DAO(db_name=path_to_db)

    yield dao_handler

    ### TEAR-DOWN ###
    dao_handler._cursor.close()
    dao_handler._connection.close()

@pytest.fixture(scope='function', name='init_users_db_table')
def create_users_table_in_db(init_sqlite3_db):
    ### SET-UP ###
    dao_handler = init_sqlite3_db
    dao_handler.create_table(table_name='users')

    yield

    ### TEAR-DOWN ###
    print('teardown init_users_db_table')

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
def init_flask_app():
    flask_handler = InitFlaskApp()
    flask_app = flask_handler.create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client # this is where the testing happens!
