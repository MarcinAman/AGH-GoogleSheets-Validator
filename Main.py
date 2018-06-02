from src import Parser
import json


def get_conf_content(path):
    f = open(path, 'r')
    return json.load(f)


def main():
    file_name = 'plan-lato'

    parser = Parser.Parser(file_name)

    fetched = parser.fetch_file()


if __name__ == '__main__':
    main()
