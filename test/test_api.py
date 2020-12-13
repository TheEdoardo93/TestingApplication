import json
import pytest


def _get_formatted_response(response):
    result_dict={}
    result_dict['data'] = json.loads(response.data.decode('utf-8'))
    result_dict['status_code'] = response.status_code

    return result_dict


def test_flask_up_and_running(init_flask_app):
    response = _get_formatted_response(init_flask_app.get('/up_and_running'))
    assert(response['data']['text'] == 'OK')
    assert(response['status_code'] == 200)


def test_create_user_correctly(init_users_db_table, init_flask_app):
    data = {'name': 'Edoardo', 'surname': 'Casiraghi', 'birth_place': 'Merate',
            'birth_date': '25/04/1993', 'instruction_level': 'University'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = _get_formatted_response(init_flask_app.post('/add_user', data=json.dumps(data), headers=headers))
    assert(response['data']['text'] == 'The user has been added to SQLite database with ID auto-generated equal to "1".')
    assert(response['status_code'] == 201)


def test_create_user_with_one_field_none(init_users_db_table, init_flask_app):
    data = {'name': 'Edoardo', 'surname': None, 'birth_place': 'Merate',
            'birth_date': '25/04/1993', 'instruction_level': 'University'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    with pytest.raises(ValueError):
        _ = init_flask_app.post('/add_user', data=json.dumps(data), headers=headers)


def test_create_user_without_data(init_users_db_table, init_flask_app):
    data = {}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    with pytest.raises(ValueError):
        _ = init_flask_app.post('/add_user', data=json.dumps(data), headers=headers)


def test_create_user_with_many_fields_none(init_users_db_table, init_flask_app):
    data = {'name': 'Edoardo', 'surname': None, 'birth_place': 'Merate',
            'birth_date': None, 'instruction_level': None}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    with pytest.raises(ValueError):
        _ = init_flask_app.post('/add_user', data=json.dumps(data), headers=headers)


def test_delete_user_without_passing_id(examples_users_db_table, init_flask_app):
    with pytest.raises(json.decoder.JSONDecodeError):
        response = _get_formatted_response(init_flask_app.delete('/delete_user/'))
        assert(response['status_code'] == 404)


def test_delete_user_by_not_existing_id(examples_users_db_table, init_flask_app):
    with pytest.raises(ValueError):
        response = _get_formatted_response(init_flask_app.delete('/delete_user/10'))
        assert(response['data']['text'] == 'There is no user with ID equal to "10" into the SQLite database.')
        assert(response['status_code'] == 200)


def test_delete_user_by_existing_id(examples_users_db_table, init_flask_app):
    response = _get_formatted_response(init_flask_app.delete('/delete_user/1'))
    assert(response['data']['text'] == 'The user with ID equal to "1" has been removed from the SQLite database correctly.')
    assert(response['status_code'] == 200)


def test_get_user_by_existing_id(examples_users_db_table, init_flask_app):
    response = _get_formatted_response(init_flask_app.get('/get_user/1'))
    assert(response['data']['text'] == 'The user with ID equal to 1 is Edoardo Casiraghi,' +
           ' born in 25/04/1993 at Merate and him/her instruction level is University.')
    assert(response['status_code'] == 200)

def test_get_user_without_passing_id(examples_users_db_table, init_flask_app):
    with pytest.raises(json.decoder.JSONDecodeError):
        response = _get_formatted_response(init_flask_app.get('/get_user/'))
        assert(response['status_code'] == 404)


def test_get_user_by_not_existing_id(examples_users_db_table, init_flask_app):
    with pytest.raises(ValueError):
        response = _get_formatted_response(init_flask_app.get('/get_user/10'))
        assert(response['data']['text'] == 'There is no user with ID equal to "10" into the SQLite database.')
        assert(response['status_code'] == 200)


def test_update_one_field_user_by_existing_id(examples_users_db_table, init_flask_app):
    data = {'name': 'Edward'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = _get_formatted_response(init_flask_app.put('/update_user/1', headers=headers, data=json.dumps(data)))
    assert(response['data']['text'] == 'The user with ID equal to "1" has been updated in the SQLite database correctly.')
    assert(response['status_code'] == 200)


def test_update_many_fields_user_by_existing_id(examples_users_db_table, init_flask_app):
    data = {'name': 'Edward', 'birth_place': 'Milan', 'instruction_level': 'High School'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = _get_formatted_response(init_flask_app.put('/update_user/1', headers=headers, data=json.dumps(data)))
    assert (response['data']['text'] == 'The user with ID equal to "1" has been updated in the SQLite database correctly.')
    assert (response['status_code'] == 200)

def test_update_zero_fields_user_by_existing_id(examples_users_db_table, init_flask_app):
    with pytest.raises(ValueError):
        data = {}
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        response = _get_formatted_response(init_flask_app.put('/update_user/1', headers=headers, data=json.dumps(data)))
        assert(response['data']['text'] == 'No fields to update for user with ID equal to "1" has been received by the server.')
        assert(response['status_code'] == 200)


###########

@pytest.mark.courses
def test_create_course_correctly(init_courses_db_table, init_flask_app):
    data = {'name': 'Programming Languages 1', 'professor': 'Sam Jones', 'tutor': 'John Mc Donald\'s',
            'academic_year': '2020/2021', 'academic_semester': 1, 'credits_number': 8,
            'description': 'Python, Java and OOP.'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = _get_formatted_response(init_flask_app.post('/create_course', data=json.dumps(data), headers=headers))
    assert(response['data']['text'] == 'The course has been created to SQLite database with ID auto-generated equal to "1".')
    assert(response['status_code'] == 201)


@pytest.mark.courses
def test_create_course_with_one_field_none_error(init_courses_db_table, init_flask_app):
    data = {'name': None, 'professor': 'Sam Jones', 'tutor': 'John Mc Donald\'s',
            'academic_year': '2020/2021', 'academic_semester': 1, 'credits_number': 8,
            'description': 'Python, Java and OOP.'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    with pytest.raises(ValueError):
        _ = init_flask_app.post('/create_course', data=json.dumps(data), headers=headers)


@pytest.mark.courses
def test_create_course_with_one_field_none_correctly(init_courses_db_table, init_flask_app):
    data = {'name': 'Programming Languages 1', 'professor': 'Sam Jones', 'tutor': None,
            'academic_year': '2020/2021', 'academic_semester': 1, 'credits_number': 8,
            'description': 'Python, Java and OOP.'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = _get_formatted_response(init_flask_app.post('/create_course', data=json.dumps(data), headers=headers))
    assert (response['data']['text'] == 'The course has been created to SQLite database with ID auto-generated equal to "1".')
    assert (response['status_code'] == 201)


@pytest.mark.courses
def test_create_course_without_data(init_courses_db_table, init_flask_app):
    data = {}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    with pytest.raises(ValueError):
        _ = init_flask_app.post('/create_course', data=json.dumps(data), headers=headers)


@pytest.mark.courses
def test_create_course_with_many_fields_none_correctly(init_courses_db_table, init_flask_app):
    data = {'name': 'Programming Languages 1', 'professor': 'Sam Jones', 'tutor': None,
            'academic_year': '2020/2021', 'academic_semester': 1, 'credits_number': 8,
            'description': None}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    response = _get_formatted_response(init_flask_app.post('/create_course', data=json.dumps(data), headers=headers))
    assert (response['data']['text'] == 'The course has been created to SQLite database with ID auto-generated equal to "1".')
    assert (response['status_code'] == 201)


@pytest.mark.courses
def test_create_course_with_many_fields_none_error(init_courses_db_table, init_flask_app):
    data = {'name': None, 'professor': None, 'tutor': 'John Mc Donald\'s',
            'academic_year': '2020/2021', 'academic_semester': 1, 'credits_number': 8,
            'description': 'Python, Java and OOP.'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    with pytest.raises(ValueError):
        _ = init_flask_app.post('/create_course', data=json.dumps(data), headers=headers)

def test_delete_course_without_passing_id(examples_courses_db_table, init_flask_app):
    with pytest.raises(json.decoder.JSONDecodeError):
        response = _get_formatted_response(init_flask_app.delete('/delete_course/'))
        assert(response['status_code'] == 404)


def test_delete_course_by_not_existing_id(examples_courses_db_table, init_flask_app):
    with pytest.raises(ValueError):
        response = _get_formatted_response(init_flask_app.delete('/delete_course/10'))
        assert(response['data']['text'] == 'There is no course with ID equal to "10" into the SQLite database.')
        assert(response['status_code'] == 200)


def test_delete_course_by_existing_id(examples_courses_db_table, init_flask_app):
    response = _get_formatted_response(init_flask_app.delete('/delete_course/1'))
    assert(response['data']['text'] == 'The course with ID equal to "1" has been removed from the SQLite database correctly.')
    assert(response['status_code'] == 200)


def test_get_course_by_existing_id(examples_courses_db_table, init_flask_app):
    response = _get_formatted_response(init_flask_app.get('/get_course/1'))
    assert(response['data']['text'] == 'The course with ID equal to "1" is Programming Languages 1, held by' +
           ' John Sky during the academic year 2018/2019 in the 2° semester and it is 10 credits.')
    assert(response['status_code'] == 200)


def test_get_course_without_passing_id(examples_courses_db_table, init_flask_app):
    with pytest.raises(json.decoder.JSONDecodeError):
        response = _get_formatted_response(init_flask_app.get('/get_course/'))
        assert(response['status_code'] == 404)


def test_get_course_by_not_existing_id(examples_courses_db_table, init_flask_app):
    with pytest.raises(ValueError):
        response = _get_formatted_response(init_flask_app.get('/get_course/10'))
        assert(response['data']['text'] == 'There is no course with ID equal to "10" into the SQLite database.')
        assert(response['status_code'] == 200)

'''
def test_update_one_field_user_by_existing_id(examples_users_db_table, init_flask_app):
    data = {'name': 'Edward'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = _get_formatted_response(init_flask_app.put('/update_user/1', headers=headers, data=json.dumps(data)))
    assert(response['data']['text'] == 'The user with ID equal to "1" has been updated in the SQLite database correctly.')
    assert(response['status_code'] == 200)


def test_update_many_fields_user_by_existing_id(examples_users_db_table, init_flask_app):
    data = {'name': 'Edward', 'birth_place': 'Milan', 'instruction_level': 'High School'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = _get_formatted_response(init_flask_app.put('/update_user/1', headers=headers, data=json.dumps(data)))
    assert (response['data']['text'] == 'The user with ID equal to "1" has been updated in the SQLite database correctly.')
    assert (response['status_code'] == 200)

def test_update_zero_fields_user_by_existing_id(examples_users_db_table, init_flask_app):
    with pytest.raises(ValueError):
        data = {}
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        response = _get_formatted_response(init_flask_app.put('/update_user/1', headers=headers, data=json.dumps(data)))
        assert(response['data']['text'] == 'No fields to update for user with ID equal to "1" has been received by the server.')
        assert(response['status_code'] == 200)
'''
