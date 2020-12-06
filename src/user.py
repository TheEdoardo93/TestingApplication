
class User(object):

    def __init__(self, name, surname, birth_date, birth_place, instruction_level):
        self._name = name
        self._surname = surname
        self._birth_date = birth_date
        self._birth_place = birth_place
        self._instruction_level = instruction_level

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
        self._name = name

    @surname.setter
    def surname(self, surname):
        self._surname = surname

    @birth_date.setter
    def birth_date(self, birth_date):
        self._birth_date = birth_date

    @birth_place.setter
    def birth_place(self, birth_place):
        self._birth_place = birth_place

    @instruction_level.setter
    def instruction_level(self, instruction_level):
        self._instruction_level = instruction_level
