class TypoValidator:
    def __init__(self, file, days):
        self.file = file
        self.days = days

    def check_days(self):
        incorrect_objects = []
        for element in self.file:
            if element['dzien'] not in self.days and element['dzien'] != '':
                incorrect_objects.append(element)

        return incorrect_objects


def validate(file,days):
    validator = TypoValidator(file, days)

    return validator.check_days()
