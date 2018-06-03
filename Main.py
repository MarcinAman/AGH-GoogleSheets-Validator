from src import Parser
import json
from src.TypoValidator import validate as validate_typo
from src.TimeValidator import validate as validate_time
from src.ObligatoryFieldsValidator import validate as validate_obligatory


def get_conf_content(path):
    f = open(path, 'r')
    return json.load(f)


def check_file(file, conf_file):
    return validate_obligatory(file, conf_file['obligatory']) \
           + validate_time(file) + validate_typo(file, conf_file['days'])


def main():
    file_name = 'plan-lato'
    parser = Parser.Parser(file_name)
    fetched = parser.fetch_file()

    print(check_file(fetched, get_conf_content('./resources/conf.json')))


if __name__ == '__main__':
    main()
