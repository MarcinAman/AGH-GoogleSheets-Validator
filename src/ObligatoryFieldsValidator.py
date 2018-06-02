import functools


def check_if_has_value(record, field):
    return record[field] != ''


class ObligatoryValidator:
    def __init__(self, file, fields):
        self.fields = fields
        self.file = file

    def validate_obligatory_fields(self):
        return list(filter(lambda x: not self.validate_record(x),self.file))

    def validate_record(self, record):
        return functools.reduce(
            lambda acc, x: acc and check_if_has_value(record, x)
            , self.fields, True)
