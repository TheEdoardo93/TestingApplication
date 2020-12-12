import pytest
from src.model.user import User


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
    assert(u.age == 27)


@pytest.mark.parametrize('user_description', [(None, 'Casiraghi', '25/04/1993',
                                               'Merate', 'University'),
                                              ('Edoardo', None, '25/04/1993',
                                               'Merate', 'University'),
                                              ('Edoardo', 'Casiraghi', None,
                                               'Merate', 'University'),
                                              ('Edoardo', 'Casiraghi', '25/04/1993',
                                               None, 'University'),
                                              ('Edoardo', 'Casiraghi', '25/04/1993',
                                               'Merate', None)])
def test_init_user_empty_attributes_error(user_description):
    name, surname, birth_date, birth_place, instruction_level = user_description
    with pytest.raises(expected_exception=ValueError):
        _ = User(name=name, surname=surname, birth_date=birth_date, birth_place=birth_place,
                 instruction_level=instruction_level)


@pytest.mark.parametrize('input_birth_date,expected_age',
                         [('01/01/2020', 0),
                          ('25/04/1993', 27),
                          ('25/04/2002', 18)])
def test_compute_age_from_birth_date(input_birth_date, expected_age):
    user = User(name='Edoardo', surname='Casiraghi', birth_date=input_birth_date,
                birth_place='Merate', instruction_level='University')

    if isinstance(expected_age, int):
        # Compute the age given the birth date of a user
        computed_age = user.compute_age_from_birth_date(birth_date=input_birth_date)
        assert( computed_age == expected_age )
    elif isinstance(expected_age, Exception):
        with pytest.raises(ValueError):
            # Compute the age given the birth date of a user
            user.compute_age_from_birth_date(birth_date=input_birth_date)


@pytest.mark.parametrize('input_birth_date, expected_birth_date',
                         [('01/01/2020', '01/01/2020'),
                          ('2020-11-01', '01/11/2020'),
                          ('2020/11-01', ValueError),
                          ('2020-11/01', ValueError),
                          ('1999/11/01', '01/11/1999'),
                          ('1999-11-01', '01/11/1999'),
                          ('11-1999-01', ValueError)])
def test_convert_date_to_standard_format(input_birth_date, expected_birth_date):
    user = User(name='Edoardo', surname='Casiraghi', birth_date='25/04/1993',
                birth_place='Merate', instruction_level='University')

    if isinstance(expected_birth_date, str):
        # Compute the age given the birth date of a user
        computed_birth_date = user.convert_date_to_standard_format(birth_date=input_birth_date)
        assert(computed_birth_date == expected_birth_date)
    else:
        with pytest.raises(ValueError):
            # Compute the age given the birth date of a user
            _ = user.convert_date_to_standard_format(birth_date=input_birth_date)
