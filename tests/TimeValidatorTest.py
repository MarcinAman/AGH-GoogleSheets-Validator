import unittest
import json
from src.Validator.TimeValidator import TimeValidator, check_if_format_matches
from src.Validator.Parser import decode_record


def get_setup_object():
    f = open('sample.json', 'r')
    file_content = json.load(f)['content']
    validator = TimeValidator([decode_record(x) for x in file_content if x['miejsce'] != ''])

    return validator


class CheckingValues(unittest.TestCase):
    def test_check_if_format_matches(self):
        self.assertEqual(True, check_if_format_matches({"godz": '10:00'}))
        self.assertEqual(True, check_if_format_matches({"godz": '7:00'}))
        self.assertEqual(False, check_if_format_matches({"godz": '1a:00'}))
        self.assertEqual(False, check_if_format_matches({"godz": '10:b0'}))

    def test_validate_format_without_error(self):
        validator = get_setup_object()
        self.assertEqual([], validator.validate_time_format())

    def test_validate_format_with_error(self):
        validator = get_setup_object()
        error_causing_object = {"godz": "7:4b", "wym": 28, "miejsce": "D17 1.38", "pora": "Z", "przedmiot": "Algebra",
                                "tyg": "",
                                "obier": "", "dzien": "Wd", "prow": "wms", "osoba": "Przybyło Jakub", "grupa": "",
                                "studia": "s1",
                                "koniec": "9:10", "typ": "W", "sem": 1}
        validator.file.append(error_causing_object)
        self.assertEqual([error_causing_object], validator.validate_time_format())

    def test_validate_without_error(self):
        validator = get_setup_object()
        self.assertEqual([], validator.check_if_classes_overlap())

    def test_validate_with_error(self):
        validator = get_setup_object()
        self.maxDiff = None

        error_causing_object = {"godz": "7:40", "wym": 28, "miejsce": "D17 1.38", "pora": "Z", "przedmiot": "Algebra",
                                "tyg": "",
                                "obier": "", "dzien": "Wt", "prow": "wms", "osoba": 'Przybyło Jakub', "grupa": "",
                                "studia": "s1",
                                "koniec": "9:10", "typ": "W", "sem": 1}
        validator.file.append(error_causing_object)
        self.assertEqual([(error_causing_object, error_causing_object)], validator.check_if_classes_overlap())


if __name__ == '__main__':
    unittest.main()
