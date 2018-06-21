import re
from datetime import datetime, timedelta


def is_matched(element):
    return bool(re.match('\d\d:\d\d', element)) or bool(re.match('\d:\d\d', element))


def check_if_format_matches(element):
    return is_matched(element['godz']) or is_matched(element['godz']) and len(
        element['godz']) <= 5


class TimeValidator:
    def __init__(self, file):
        self.file = file

    def validate_time_format(self):
        return [x for x in self.file if
                not check_if_format_matches(x) and x['godz'] != '']

    def get_classrooms_occupancy(self):
        classrooms = {}

        for class_element in self.file:
            if not is_empty_record(class_element):
                index = (class_element['miejsce'], class_element['dzien'])

                if index[0] and index[1] and is_matched(class_element['godz']):
                    dictionary_element = classrooms.get(index)

                    if dictionary_element is None:
                        classrooms[index] = \
                            [zip_begin_with_end(class_element['godz'], class_element['koniec'], class_element)]
                    else:
                        dictionary_element.append(
                            zip_begin_with_end(class_element['godz'], class_element['koniec'], class_element))

                        classrooms[index] = dictionary_element

        return classrooms

    def check_if_classes_overlap(self):
        classes = self.get_classrooms_occupancy()

        overlapping = []

        for place, day in classes.keys():
            hours_list_with_none = classes[(place, day)]

            hours_list = sorted(
                [a for a in hours_list_with_none if a[0] is not None],
                key=lambda x: x[0])

            for index in range(1, len(hours_list)):
                if is_end_later_than_finish(hours_list[index - 1], hours_list[index]) \
                        and can_overlap(hours_list[index], hours_list[index - 1]):
                    overlapping.append(
                        (hours_list[index - 1][2], hours_list[index][2])
                    )

        return overlapping


def are_the_same(val_a, val_b):
    shared_items = set(val_a[2].items()) & set(val_b[2].items())

    return len(shared_items) == len(val_a[2].items())


def can_overlap(class_a, class_b):
    return class_b[2]['tyg'] == class_a[2]['tyg'] \
           and class_a[2]['sem'] == class_b[2]['sem'] \
           and class_a[2]['studia'] == class_b[2]['studia'] \
           and class_a[2]['pora'] == class_b[2]['pora'] \
           and class_a[2]['wym']+class_b[2]['wym'] > 28


def is_end_later_than_finish(a, b):
    if a is None:
        return True
    if b is None:
        return False

    return a[1] > b[0]


def convert_to_time(expr):
    return datetime.strptime(expr, '%H:%M')


def zip_begin_with_end(begin_hour, end_hour, class_element):
    if end_hour != '' and is_matched(begin_hour) and is_matched(end_hour):
        return convert_to_time(begin_hour), convert_to_time(end_hour), class_element

    parsed_begin_hour = None
    parsed_end_hour = None

    if is_matched(begin_hour):
        parsed_begin_hour = convert_to_time(begin_hour)
        parsed_end_hour = parsed_begin_hour + timedelta(hours=1, minutes=30)

    return parsed_begin_hour, parsed_end_hour, class_element


def is_empty_record(record):
    return record['godz'] == '' and record['koniec'] == ''


def get_classrooms_schedule(file):
    classes = TimeValidator(file)

    occupancy = classes.get_classrooms_occupancy()

    return sorted([
        (str(k) + ' ' + str(v), sorted([x for x in occupancy[k, v] if x[0] is not None], key=lambda x: x[0]))
        for k, v in occupancy
    ],key=lambda x: x[0])


def validate_time_format(file):
    validator = TimeValidator(file)
    return validator.validate_time_format()


def validate(file):
    validator = TimeValidator(file)

    return validator.check_if_classes_overlap()
