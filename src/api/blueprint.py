from flask import Blueprint, request, jsonify
import json

from src.model.user import User
from src.dao.dao import DAO

app_blueprint = Blueprint('main', __name__)

@app_blueprint.route('/', methods=['GET'])
def index():
    return jsonify({'text': 'OK'}) , 200

@app_blueprint.route('/add_user', methods=['POST'])
def add_user():
    d = "C:\\Users\\edoardo.casiraghi\\AppData\\Local\\Temp\\pytest-of-edoardo.casiraghi\\pytest-298/test_DB"
    #d='./test_DB'
    dao_handler = DAO(db_name=d)
    dao_handler._cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print('\nTABLES 2: {}'.format(dao_handler._cursor.fetchall()))

    dao_handler._cursor.execute("SELECT * FROM users;")
    print('\nROWS 2: {}'.format(dao_handler._cursor.fetchall()))

    dao_handler._cursor.execute("SELECT sql FROM sqlite_master WHERE name = 'users';")
    print('\nSCHEMA 2: {}'.format(dao_handler._cursor.fetchall()))

    # Get the data received by HTTP POST request
    request_data = json.loads(request.data)
    print('\nrequest_data: {}'.format(request_data))

    # Create a User object with the information about him/her passed by HTTP request
    u = User(name=request_data['name'], surname=request_data['surname'], birth_date=request_data['birth_date'],
             birth_place=request_data['birth_place'], instruction_level=request_data['instruction_level'])
    print('\nUser: {}'.format(u))

    # Add the user to the SQLite database
    dao_handler.add_row_into_table(object=u, table_name='users')

    return jsonify({'text': 'OK'}) , 200
