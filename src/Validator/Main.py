from src.Validator import Parser
import json
from src.Validator.TypoValidator import validate as validate_typo
from src.Validator.TimeValidator import validate as validate_time
from src.Validator.ObligatoryFieldsValidator import validate as validate_obligatory


def get_conf_content(path):
    f = open(path, 'r')
    return json.load(f)


def check_file(file, conf_file):
    return validate_obligatory(file, conf_file['obligatory']) \
           + validate_time(file) + validate_typo(file, conf_file['days'])


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
