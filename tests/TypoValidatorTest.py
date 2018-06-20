import unittest
import json
from src import TypoValidator
from src.Validator.Main import get_conf_content


def get_setup_object():
    f = open('sample.json', 'r')
    file_content = json.load(f)['content']
    conf_content = get_conf_content('../resources/conf.json')['days']
    validator = TypoValidator(file_content, conf_content)

    return validator


class CheckingValues(unittest.TestCase):

    def test_validate_without_error(self):
        validator = get_setup_object()
        self.assertEqual([], validator.check_days())
        validator.file.append({"dzien": ""})
        self.assertEqual([],validator.check_days())

    def test_validate_with_error(self):
        validator = get_setup_object()
        error_causing_object = {"godz": "7:40", "wym": 28, "miejsce": "D17 1.38", "pora": "Z", "przedmiot": "Algebra", "tyg": "",
             "obier": "", "dzien": "Wd", "prow": "wms", "osoba": "Przyby\u0142o Jakub", "grupa": "", "studia": "s1",
             "koniec": "9:10", "typ": "W", "sem": 1}
        validator.file.append(error_causing_object)
        self.assertEqual([error_causing_object], validator.check_days())


if __name__ == '__main__':
    unittest.main()
