days_mapping = {
    'Pn': 0,
    'Wt': 1,
    'Sr': 2,
    'Cz': 3,
    'Pt': 4,
    'Sb': 5,
    'Nd': 6,
    '': 7
}


class TeachersParser:
    def __init__(self, file):
        self.file = file

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

        return sort_teachers(teachers)


def sort_teachers(teachers):
    return sorted(
        [(name, sorted(teachers[name], key=lambda x: (days_mapping[x['dzien']], x['godz'])))
         for name in teachers.keys()]
        , key=lambda x: x[0])


def get_teachers(file):
    teachers_parser = TeachersParser(file)

    return teachers_parser.get_teachers_list()
