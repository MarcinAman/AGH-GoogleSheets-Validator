import re
from datetime import datetime, timedelta


class TimeValidator:
    def __init__(self, file):
        self.file = file

    def validate_time_format(self):
        list(self.file.filter(
            lambda x: not re.match('\d\d:\d\d', x.godz)
        ))

    def get_classrooms_occupancy(self):
        classrooms = {}

        for class_element in self.file:
            index = (class_element.miejsce, class_element.dzien)

            dictionary_element = classrooms.get(index)

            if dictionary_element is None:
                classrooms[index] = \
                    [zip_begin_with_end(class_element.godz, class_element.koniec, class_element)]
            else:
                classrooms[index] = dictionary_element.append(
                    zip_begin_with_end(class_element.godz, class_element.koniec, class_element))

        return classrooms

    def check_if_classes_overlap(self):
        classes = self.get_classrooms_occupancy()

        overlapping = []

        for key in classes.keys():
            hours_list = classes[key].sorted()

            for index in range(1, len(hours_list)):
                if hours_list[index - 1][1] < hours_list[index][0]:
                    overlapping.append(
                        (hours_list[index - 1][2], hours_list[index - 1][2])
                    )

        return overlapping


def convert_to_time(expr):
    return datetime.strptime(expr, '%H:%M')


def zip_begin_with_end(begin_hour, end_hour, class_element):
    if end_hour:
        return convert_to_time(begin_hour), convert_to_time(end_hour), class_element

    parsed_begin_hour = convert_to_time(begin_hour)

    parsed_end_hour = parsed_begin_hour + timedelta(hours=1, minutes=30)

    return parsed_begin_hour, parsed_end_hour, class_element
