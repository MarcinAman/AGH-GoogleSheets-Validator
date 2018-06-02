import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json


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

        return sheet.get_all_records()

    def xd(self):
        f = open('./tests/sample.json','w')
        f.write('{ "content": '+json.dumps(self.fetch_file()[:20])+'}')
        f.close()
