from src.Validator import Parser
import json
import os
from src.Validator.TypoValidator import validate as validate_typo
from src.Validator.TimeValidator import validate as validate_time
from src.Validator.ObligatoryFieldsValidator import validate as validate_obligatory
from src.Validator.TimeValidator import get_classrooms_schedule as get_parsed_schedule
from src.Validator.TimeValidator import validate_time_format
from src.Validator.TeachersParser import get_teachers


def get_conf_content(path):
    f = open(path, 'r')
    return json.load(f)


def check_file(file, conf_file):
    return validate_obligatory(file, conf_file['obligatory']) \
           + validate_time(file) + validate_typo(file, conf_file['days'])


def fetch_file():
    conf_file = get_conf_content(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/conf.json')))
    file_name = conf_file['spreadsheet']

    parser = Parser.Parser(file_name, 'Errors')
    return parser.fetch_file(), conf_file


def get_columns(file):
    return [column for column, _ in file[0].items()]


def get_records_data():
    (fetched, conf_file) = fetch_file()
    return {
        'columns': get_columns(fetched),
        'invalid_typo': validate_typo(fetched, conf_file['days']) + validate_time_format(fetched),
        'invalid_obligatory': validate_obligatory(fetched, conf_file['obligatory']),
        'invalid_overlap': validate_time(fetched),
        'all_records': fetched
    }


def get_teachers_schedule():
    (fetched, conf_file) = fetch_file()

    return get_teachers(fetched)


def get_classroom_schedule():
    (fetched, conf_file) = fetch_file()
    return get_parsed_schedule(fetched)


def main():
    file_name = 'plan-lato'
    error_file_name = 'Errors'
    parser = Parser.Parser(file_name, error_file_name)
    fetched = parser.fetch_file()

    invalid_elements = check_file(fetched, get_conf_content('./resources/conf.json'))

    print(invalid_elements)

    parser.save_to_backup_spreadsheet(
        [fetched.index(x) for x in invalid_elements]
    )


if __name__ == '__main__':
    main()
