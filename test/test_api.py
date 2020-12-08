import json
import pytest
import os


def _get_formatted_response(response):
    result_dict={}
    result_dict['data'] = json.loads(response.data.decode('utf-8'))
    result_dict['status_code'] = response.status_code

    return result_dict

def test_index(init_flask_app):
    response = _get_formatted_response(init_flask_app.get('/'))
    assert(response['data']['text'] == 'OK')
    assert(response['status_code'] == 200)

def test_add_user(init_users_db_table, init_flask_app):
    data = {'name': 'Edoardo', 'surname': 'Casiraghi', 'birth_place': 'Merate',
            'birth_date': '25/04/1993', 'instruction_level': 'University'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = _get_formatted_response(init_flask_app.post('/add_user', data=json.dumps(data), headers=headers))
    assert(response['data']['text'] == 'The user has been added to SQLite database with ID auto-generated equal to "1".')
    assert(response['status_code'] == 200)

def test_delete_user_by_id(examples_users_db_table, init_flask_app):
    response = _get_formatted_response(init_flask_app.delete('/delete_user/1'))
    assert(response['data']['text'] == 'The user with ID equal to 1 has been removed from SQLite database correctly.')
    assert(response['status_code'] == 200)

def test_get_user_by_id(examples_users_db_table, init_flask_app):
    response = _get_formatted_response(init_flask_app.get('/get_user/1'))
    assert(response['data']['text'] == 'The user with ID equal to 1 is Edoardo Casiraghi,' +
           ' born in 25/04/1993 at Merate and him/her instruction level is University.')
    assert(response['status_code'] == 200)
