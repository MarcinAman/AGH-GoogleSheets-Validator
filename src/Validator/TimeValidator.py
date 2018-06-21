import re
from src.Validator.Classrooms import get_classrooms_occupancy


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

    def check_if_classes_overlap(self):
        classes = get_classrooms_occupancy(self.file)

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
           and class_a[2]['wym'] + class_b[2]['wym'] > 28


def is_end_later_than_finish(a, b):
    if a is None:
        return True
    if b is None:
        return False

    return a[1] > b[0]


def validate_time_format(file):
    validator = TimeValidator(file)
    return validator.validate_time_format()


def validate(file):
    validator = TimeValidator(file)

    return validator.check_if_classes_overlap()
