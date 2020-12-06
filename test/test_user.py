import pytest
from src.user import User


def test_adding_new_users_correctly(init_sqlite3_db, init_users_db_table,
                                    return_new_users_correctly):
    # Retrieve the connection and the cursor to the "users.db" table
    dao_handler = init_sqlite3_db

    # Add users to "users" table in the SQLite database
    for index, user in enumerate(return_new_users_correctly):
        dao_handler.add_row_into_table(object=user, table_name='users')

        # Count how many users are there in the "users.db" table
        count_rows_sql_statement = 'SELECT COUNT(*) FROM users;'
        dao_handler._cursor.execute(count_rows_sql_statement)
        n_rows = dao_handler._cursor.fetchone()[0]
        assert (n_rows == index + 1)


@pytest.mark.parametrize('user', [('Edoardo', 'Casiraghi', '25/04/1993',
                                   'Merate', 'University')])
def test_init_user_correctly(user):
    name, surname, birth_date, birth_place, instruction_level = user
    u = User(name=name, surname=surname, birth_date=birth_date,
             birth_place=birth_place, instruction_level=instruction_level)
    assert(u.name == name)
    assert(u.surname == surname)
    assert(u.birth_place == birth_place)
    assert(u.birth_date == birth_date)
    assert(u.instruction_level == instruction_level)


@pytest.mark.parametrize('user_description', [(None, 'Casiraghi', '25/04/1993',
                                               'Merate', 'University'),
                                              ('Edoardo', None, '25/04/1993',
                                               'Merate', 'University'),
                                              ('Edoardo', 'Casiraghi', None,
                                               'Merate', 'University'),
                                              ('Edoardo', 'Casiraghi', '25/04/1993',
                                               None, 'University')])
def test_init_user_empty_attributes_error(user_description):
    name, surname, birth_date, birth_place, instruction_level = user_description
    with pytest.raises(expected_exception=ValueError):
        User(name=name, surname=surname, birth_date=birth_date, birth_place=birth_place,
             instruction_level=instruction_level)


@pytest.mark.parametrize('user,age', [(User(name='Edoardo', surname='Casiraghi',
                                            birth_date='01/01/2020', birth_place='Merate',
                                            instruction_level='University'), 0),
                                      (User(name='Edoardo', surname='Casiraghi',
                                            birth_date='29/07/2021', birth_place='Merate',
                                            instruction_level='University'), ValueError),
                                      (User(name='Edoardo', surname='Casiraghi',
                                            birth_date='25/04/1993', birth_place='Merate',
                                            instruction_level='University'), 27),
                                      (User(name='Edoardo', surname='Casiraghi',
                                            birth_date='25/04/2002', birth_place='Merate',
                                            instruction_level='University'), 18)])
def test_compute_age_from_birth_date(user, age):
    if isinstance(age, int):
        # Compute the age given the birth date of a user
        computed_age = user.compute_age_from_birth_date()
        assert( computed_age == age )
    elif isinstance(age, Exception):
        with pytest.raises(ValueError):
            # Compute the age given the birth date of a user
            user.compute_age_from_birth_date()


@pytest.mark.parametrize('user,age', [(User(name='Edoardo', surname='Casiraghi',
                                            birth_date='01/01/2020', birth_place='Merate',
                                            instruction_level='University'), 0),
                                      (User(name='Edoardo', surname='Casiraghi',
                                            birth_date='29/07/2021', birth_place='Merate',
                                            instruction_level='University'), ValueError),
                                      (User(name='Edoardo', surname='Casiraghi',
                                            birth_date='25/04/1993', birth_place='Merate',
                                            instruction_level='University'), 27),
                                      (User(name='Edoardo', surname='Casiraghi',
                                            birth_date='25/04/2002', birth_place='Merate',
                                            instruction_level='University'), 18)])
def test_compute_age_from_birth_date(user, age):
    if isinstance(age, int):
        # Compute the age given the birth date of a user
        computed_age = user.compute_age_from_birth_date()
        assert(computed_age == age)
    else:
        with pytest.raises(ValueError):
            # Compute the age given the birth date of a user
            user.compute_age_from_birth_date()


@pytest.mark.parametrize('user,birth_date', [
    (User(name='Edoardo', surname='Casiraghi', birth_date='01/01/2020',
          birth_place='Merate', instruction_level='University'),
     '01/01/2020'),
    (User(name='Edoardo', surname='Casiraghi', birth_date='2020-11-01',
          birth_place='Merate', instruction_level='University'),
     '01/11/2020'),
    (User(name='Edoardo', surname='Casiraghi', birth_date='2020/11-01',
          birth_place='Merate', instruction_level='University'),
     ValueError),
    (User(name='Edoardo', surname='Casiraghi', birth_date='2020-11/01',
          birth_place='Merate', instruction_level='University'),
     ValueError),
    (User(name='Edoardo', surname='Casiraghi', birth_date='1999/11/01',
          birth_place='Merate', instruction_level='University'),
      '01/11/1999'),
    (User(name='Edoardo', surname='Casiraghi', birth_date='1999-11-01',
           birth_place='Merate', instruction_level='University'),
      '01/11/1999'),
    (User(name='Edoardo', surname='Casiraghi', birth_date='11-1999-01',
           birth_place='Merate', instruction_level='University'),
      ValueError)
     ])
def test_convert_date_to_standard_format(user, birth_date):
    if isinstance(birth_date, str):
        # Compute the age given the birth date of a user
        computed_birth_date = user.convert_date_to_standard_format()
        assert(computed_birth_date == birth_date)
    else:
        with pytest.raises(ValueError):
            # Compute the age given the birth date of a user
            computed_birth_date = user.convert_date_to_standard_format()
