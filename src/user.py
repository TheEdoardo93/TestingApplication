from datetime import datetime
import math


class User(object):

    def __init__(self, name, surname, birth_date, birth_place, instruction_level):
        self.name = name
        self.surname = surname
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.instruction_level = instruction_level

    ### GETTER methods ###
    @property
    def name(self):
        return self._name

    @property
    def surname(self):
        return self._surname

    @property
    def birth_date(self):
        return self._birth_date

    @property
    def birth_place(self):
        return self._birth_place

    @property
    def instruction_level(self):
        return self._instruction_level

    ### SETTER methods ###
    @name.setter
    def name(self, name):
        if name is None:
            raise ValueError('ERROR: the name of a user can not be empty.')
        self._name = name

    @surname.setter
    def surname(self, surname):
        if surname is None:
            raise ValueError('ERROR: the surname of a user can not be empty.')
        self._surname = surname

    @birth_date.setter
    def birth_date(self, birth_date):
        if birth_date is None:
            raise ValueError('ERROR: the birth date of a user can not be empty.')
        self._birth_date = birth_date

    @birth_place.setter
    def birth_place(self, birth_place):
        if birth_place is None:
            raise ValueError('ERROR: the birth place of a user can not be empty.')
        self._birth_place = birth_place

    @instruction_level.setter
    def instruction_level(self, instruction_level):
        if instruction_level not in ['Middle School', 'High School', 'University']:
            raise ValueError('ERROR: the instruction level of a user can be only "Middle School",'
                                 '"High School or "University".')
        self._instruction_level = instruction_level

    def compute_age_from_birth_date(self):
        # Retrieve the current date
        current_date = datetime.now()
        # Convert the birth date from string type to datetime type
        birth_date = datetime.strptime(self.birth_date, '%d/%m/%Y')
        # Derive the age of a user as the difference between the current date and the birth date of the user
        age = math.floor( float( (current_date - birth_date).days / 365 ) )
        # If the difference between them is negative, then it is a error to capture
        if age < 0:
            raise ValueError('ERROR: The birth date can not be after the current date.')

        return age

    def convert_date_to_standard_format(self):
        birth_date = self.birth_date

        # If there are both "-" and "/" characters that split day, month and year, it is a not understandable format
        if '-' in birth_date and '/' in birth_date:
            raise ValueError('ERROR: in a date can not be both "-" and "/" characters.')

        # Convert "-" to "/" if necessary
        if '-' in birth_date:
            birth_date = birth_date.replace('-', '/')

        # Split the date to its component i.e. day, month, year
        day, month, year = birth_date.split('/')

        # If the year is between day and month, it is a not understandable format
        if len(month) == 4:
            raise ValueError('ERROR: date format not understandable.')

        # If the day is at the end of the date and the year is at the beginning of the date, switch them
        if len(day) == 4 and len(year) == 2:
            day, year = year, day

        return '{}/{}/{}'.format(day, month, year)