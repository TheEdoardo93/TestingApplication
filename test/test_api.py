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
    assert(response['data']['text'] == 'OK')
    assert(response['status_code'] == 200)
