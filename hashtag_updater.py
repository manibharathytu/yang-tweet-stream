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
 
    result = sheet1.get_all_records()
    ht=[]
    for item in result :
        ht.append(item['YG_Hashtags'])
    return ht


    

