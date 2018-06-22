import re
from datetime import datetime, timedelta


def get_classrooms_occupancy(file):
    classrooms = {}

    for class_element in file:
        if not is_empty_record(class_element):
            index = (class_element['miejsce'], class_element['dzien'], class_element['sem'])

            if index[0] and index[1] and index[2] and is_matched(class_element['godz']):
                dictionary_element = classrooms.get(index)

                if dictionary_element is None:
                    classrooms[index] = \
                        [zip_begin_with_end(class_element['godz'], class_element['koniec'], class_element)]
                else:
                    dictionary_element.append(
                        zip_begin_with_end(class_element['godz'], class_element['koniec'], class_element))

                    classrooms[index] = dictionary_element

    return classrooms


def is_matched(element):
    return bool(re.match('\d\d:\d\d', element)) or bool(re.match('\d:\d\d', element))


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


def get_classrooms_schedule(file, days_mapping):
    occupancy = get_classrooms_occupancy(file)

    return sorted([
        (generate_name(k, v, s),
         sorted([x for x in occupancy[k, v, s] if x[0] is not None], key=lambda x: x[0]))
        for k, v, s in occupancy
    ], key=lambda x: string_classrooms_comparator(x, days_mapping))


def generate_name(k, v, s):
    return str(k) + ' ' + str(v) + ' ' + str(s)


def generate_free_schedule(file, conf, days_mapping):
    occupancy = get_classrooms_occupancy(file)

    free_schedule = {}

    for element in occupancy.keys():
        free_schedule[element] = get_free_classes(occupancy[element], conf)

    mapped_free_schedule = map_dict_to_list(free_schedule)
    return sorted(mapped_free_schedule, key=lambda x: string_classrooms_comparator(x, days_mapping))


def string_classrooms_comparator(record, days_mapping):
    splitted = list(record[0].split(' '))

    return splitted[0], splitted[1], days_mapping[splitted[2]], splitted[2]


def generate_empty_periodic_timetable(classes_begining):
    return [
        (convert_to_time(start), convert_to_time(start) + timedelta(hours=1, minutes=30))
        for start in classes_begining
    ]


def get_free_classes(occupancy, conf):
    free_schedule = generate_empty_periodic_timetable(conf['classes_begining'])

    for el in occupancy:  # (start, end,_)
        for value in free_schedule:  # (start,end)
            if el[0] >= value[0] and el[1] <= value[1]:
                free_schedule.remove(value)

    return free_schedule


def map_dict_to_list(free_schedule):
    print(free_schedule.keys())
    return [
        (generate_name(k, d, s),
         [(map_datetime_to_string(start), map_datetime_to_string(end)) for start, end in free_schedule[k, d, s]])
        for k, d, s in free_schedule.keys()]


def map_datetime_to_string(element):
    return element.strftime('%H:%M')
