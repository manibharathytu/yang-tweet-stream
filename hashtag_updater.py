import gspread
from oauth2client.service_account import ServiceAccountCredentials


from helper import set_interval
import pickle


scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)


def sheet_job():

    sheet = client.open('YangGang_Hashtags')
    sheet1 = sheet.sheet1

    # Column A is the tracked tag list. get_all_records() fails because the
    # header row also has duplicate empty cells.
    rows = sheet1.get_all_values()
    ht = []
    for row in rows[1:]:
        if row and row[0].strip():
            ht.append(row[0].strip())
    return ht


    

