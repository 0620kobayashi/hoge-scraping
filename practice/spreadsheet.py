import gspread
from bs4 import BeautifulSoup
import requests
import pandas as pd
from google.oauth2.service_account import Credentials

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'service.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)

SP_SHEET_KEY = '1wAnuYPFuV8zEWquVwr-9QXN4zvk73QtEMAIgO-83Zrg'
sh = gc.open_by_key(SP_SHEET_KEY)
SP_SHEET = 'db'
worksheet = sh.worksheet(SP_SHEET)
data = worksheet.get_all_values()

df = pd.DataFrame(data[1:], columns=data[0])
