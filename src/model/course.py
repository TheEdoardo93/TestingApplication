class Course(object):

    def __init__(self, name, professor, tutor, academic_year, academic_semester, credits_number, description):
        self.name = name
        self.professor = professor
        self.tutor = tutor
        self.academic_year = academic_year
        self.academic_semester = academic_semester
        self.credits_number = credits_number
        self.description = description

    @property
    def name(self):
        return self._name

    @property
    def professor(self):
        return self._professor

    @property
    def tutor(self):
        return self._tutor

    @property
    def academic_year(self):
        return self._academic_year

    @property
    def academic_semester(self):
        return self._academic_semester

    @property
    def credits_number(self):
        return self._credits_number

    @property
    def description(self):
        return self._description

    @name.setter
    def name(self, name):
        if name is None:
            raise ValueError('ERROR: the name of the course is mandatory.')
        self._name = name

    @professor.setter
    def professor(self, professor):
        if professor is None:
            raise ValueError('ERROR: the professor name and surname of the course is mandatory.')
        self._professor = professor

    @tutor.setter
    def tutor(self, tutor):
        self._tutor = tutor

    @academic_year.setter
    def academic_year(self, academic_year):
        if academic_year is None:
            raise ValueError('ERROR: the academic year of the course is mandatory.')
        self._academic_year = academic_year

    @academic_semester.setter
    def academic_semester(self, academic_semester):
        if academic_semester is None:
            raise ValueError('ERROR: the academic semester of the course is mandatory.')
        self._academic_semester = academic_semester

    @credits_number.setter
    def credits_number(self, credits_number):
        if credits_number is None:
            raise ValueError('ERROR: the number of credits of the course is mandatory.')
        self._credits_number = credits_number

    @description.setter
    def description(self, description):
        self._description = description
