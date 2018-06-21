class TeachersParser:
    def __init__(self, file,days_mapping):
        self.file = file
        self.days_mapping = days_mapping

    def parse_teachers(self):
        teachers = {}

        for record in self.file:
            name = record['osoba']

            if name is not None and name != '':
                fetched = teachers.get(name)

                if fetched is None:
                    teachers[name] = [record]
                else:
                    teachers[name].append(record)

        return teachers

    def get_teachers_list(self):
        teachers = self.parse_teachers()

        return sort_teachers(teachers,self.days_mapping)


def sort_teachers(teachers,days_mapping):
    return sorted(
        [(name, sorted(teachers[name], key=lambda x: (days_mapping[x['dzien']], x['godz'])))
         for name in teachers.keys()]
        , key=lambda x: x[0])


def get_teachers(file,days_mapping):
    teachers_parser = TeachersParser(file,days_mapping)

    return teachers_parser.get_teachers_list()
