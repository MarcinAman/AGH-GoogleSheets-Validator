import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json


def decode_record(record):
    return {k.encode('utf8'): v.encode('utf8') if type(v) == unicode else v for k, v in record.items()}


class Parser:
    def __init__(self, file_name):
        self.file_name = file_name
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    def authorize(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', self.scope)

        return gspread.authorize(creds)

    def fetch_file(self):
        client = self.authorize()
        sheet = client.open(self.file_name).sheet1

        records = sheet.get_all_records()

        return [decode_record(x) for x in records]

    def xd(self):
        f = open('./tests/sample.json','w')
        f.write('{ "content": '+json.dumps(self.fetch_file()[:20])+'}')
        f.close()
