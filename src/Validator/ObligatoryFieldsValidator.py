import functools
from src.Validator.Parser import is_record_empty


def validate(file, fields):
    validator = ObligatoryValidator(file, fields)

    return validator.validate_obligatory_fields()


def check_if_has_value(record, field):
    return record[field] != ''


class ObligatoryValidator:
    def __init__(self, file, fields):
        self.fields = fields
        self.file = file

    def validate_obligatory_fields(self):
        return list(filter(lambda x: not self.validate_record(x) and is_record_empty(x), self.file))

    def validate_record(self, record):
        return functools.reduce(
            lambda acc, x: acc and check_if_has_value(record, x)
            , self.fields, True)
