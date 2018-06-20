import gspread
from oauth2client.service_account import ServiceAccountCredentials
import functools
import platform


def decode_record(record):
    if platform.system() == 'Linux':
        return {k.encode('utf8'): v.encode('utf8') if type(v) == str else v for k, v in record.items()}
    else:
        return record


def contains_only_letters(value):
    return value[1].isalpha()


def is_record_empty(record):
    return functools.reduce(
        lambda acc, element: contains_only_letters(element) or acc, record.items(), False
    )


class Parser:
    def __init__(self, file_name, error_sheet_name):
        self.file_name = file_name
        self.error_sheet_name = error_sheet_name
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.document_len = 0

    def authorize(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', self.scope)

        return gspread.authorize(creds)

    def fetch_file(self):
        client = self.authorize()
        sheet = client.open(self.file_name).sheet1

        records = sheet.get_all_records()

        self.document_len = len(records)

        return [decode_record(x) for x in records]

    def save_to_backup_spreadsheet(self, columns):
        client = self.authorize()

        opened_sheet = client.open(self.file_name)

        delete_worksheet(opened_sheet, self.error_sheet_name)

        opened_sheet.add_worksheet(self.error_sheet_name, self.document_len, 50)

        sheet = opened_sheet.worksheet(self.error_sheet_name)

        for column in columns:
            sheet.update_cell(col=1, row=column + 2, value="E")


def delete_worksheet(opened_sheet, worksheet_name):
    for worksheet in opened_sheet.worksheets():
        if worksheet.title == worksheet_name:
            opened_sheet.del_worksheet(worksheet)
