from flask import Blueprint, request, jsonify
import json

from src.model.user import User
from src.dao.dao import DAO

app_blueprint = Blueprint('main', __name__)

def _get_dao_handler():
    # Read a temporary file called "tmp.txt" which contains the path to the test SQLite database
    with open('tmp.txt', 'r') as input_file:
        path_to_tmp_db_directory = input_file.readline().rstrip('\n')

    # Create a connection to the test SQLite database
    dao_handler = DAO(path_to_db=path_to_tmp_db_directory)

    return dao_handler

@app_blueprint.route('/', methods=['GET'])
def index():
    return jsonify({'text': 'OK'}), 200

@app_blueprint.route('/add_user', methods=['POST'])
def add_user():
    # Get a connection to the test SQLite database
    dao_handler = _get_dao_handler()

    # Get the data received by HTTP POST request
    request_data = json.loads(request.data)

    # Create a User object with the information about him/her passed by HTTP request
    u = User(name=request_data['name'], surname=request_data['surname'], birth_date=request_data['birth_date'],
             birth_place=request_data['birth_place'], instruction_level=request_data['instruction_level'])

    # Add the user to the SQLite database and retrieve the ID automatically assigned to him/her
    user_id = dao_handler.add_row_into_table(object=u, table_name='users')

    return jsonify({'text': 'The user has been added to SQLite database with ID auto-generated equal to "{}".'.format(user_id)}), 200

@app_blueprint.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    print('route corretta con {}'.format(user_id))

    # Get a connection to the test SQLite database
    dao_handler = _get_dao_handler()

    check = dao_handler.delete_row_from_table(table_name='users', object={'id': user_id})
    if check:
        return jsonify({'text': 'The user with ID equal to {} has been removed from SQLite database correctly.'.format(user_id)}), 200
    else:
        return jsonify({'text': 'The user with ID equal to {} has not been removed from SQLite database.'.format(user_id)}), 500
