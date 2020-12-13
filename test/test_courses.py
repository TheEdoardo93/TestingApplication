import pytest

from src.model.course import Course

@pytest.mark.courses
@pytest.mark.parametrize('course', [('Programming Languages 1', 'Sam Jones', 'John Mc Donald\'s',
                                     '2020/2021', 1, 8, 'Learning Python, Java and OOP.')])
def test_init_course_correctly(course):
    name, professor, tutor, academic_year, academic_semester, credits_number, description = course
    c = Course(name=name, professor=professor, tutor=tutor, academic_year=academic_year,
               academic_semester=academic_semester, credits_number=credits_number, description=description)
    assert(c.name == name)
    assert(c.professor == professor)
    assert(c.tutor == tutor)
    assert(c.academic_year == academic_year)
    assert(c.academic_semester == academic_semester)
    assert(c.credits_number == credits_number)
    assert(c.description == description)

@pytest.mark.courses
@pytest.mark.parametrize('course_description,expected_output', [
    ( (None, 'Sam Jones', 'John Mc Donald\'s', '2020/2021', 1, 8, 'Learning Python, Java and OOP.'), ValueError),
    ( ('Programming Languages 1', None, 'John Mc Donald\'s', '2020/2021', 1, 8, 'Learning Python, Java and OOP.'), ValueError),
    ( ('Programming Languages 1', 'Sam Jones', None, '2020/2021', 1, 8, 'Learning Python, Java and OOP.'), 'OK'),
    ( ('Programming Languages 1', 'Sam Jones', 'John Mc Donald\'s', None, 1, 8, 'Learning Python, Java and OOP.'), ValueError),
    ( ('Programming Languages 1', 'Sam Jones', 'John Mc Donald\'s', '2020/2021', None, 8, 'Learning Python, Java and OOP.'), ValueError),
    ( ('Programming Languages 1', 'Sam Jones', 'John Mc Donald\'s', '2020/2021', 1, None, 'Learning Python, Java and OOP.'), ValueError),
    ( ('Programming Languages 1', 'Sam Jones', 'John Mc Donald\'s', '2020/2021', 1, 8, None), 'OK')])
def test_init_user_empty_attributes_error(course_description, expected_output):
    name, professor, tutor, academic_year, academic_semester, credits_number, description = course_description

    if expected_output == 'OK':
        c = Course(name=name, professor=professor, tutor=tutor, academic_year=academic_year,
                   academic_semester=academic_semester, credits_number=credits_number, description=description)
        assert (c.name == name)
        assert (c.professor == professor)
        assert (c.tutor == tutor)
        assert (c.academic_year == academic_year)
        assert (c.academic_semester == academic_semester)
        assert (c.credits_number == credits_number)
        assert (c.description == description)

    elif isinstance(expected_output, Exception):
        with pytest.raises(ValueError):
            _ = Course(name=name, professor=professor, tutor=tutor, academic_year=academic_year,
                       academic_semester=academic_semester, credits_number=credits_number, description=description)
