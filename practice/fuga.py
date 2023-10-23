from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_data_udemy():
    url ="https://scraping-for-beginner.herokuapp.com/udemy"
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')
    n_subscriber = soup.find('p', {'class':'subscribers'}).text
    n_subscriber = int(n_subscriber.split('：')[1])

    n_review = soup.find('p', {'class':'reviews'}).text
    n_review = int(n_review.split('：')[1])
    return{
        'n_subscriber':n_subscriber,
        'n_review':n_review
    }

def get_data_ec():
    url ="https://scraping.official.ec"
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')
    itemList = soup.find('ul',{'id':'itemList'})
    items = itemList.find_all('li')

    data_ec = []
    for item in items:
        datum_ec = {}
        datum_ec['title'] = item.find('p',{'class':'items-grid_itemTitleText_5c97110f'}).text
        price = item.find('p',{'class','items-grid_price_5c97110f'}).text
        datum_ec['price'] = int(price.replace('¥', "").replace(',',""))
        datum_ec['link'] = item.find('a')['href']
        is_stock = item.find('p',{'class':'items-grid_soldOut_5c97110f'}) == None
        datum_ec['is_stock'] = '在庫あり' if is_stock == True else '在庫なし'
        data_ec.append(datum_ec)
    
    df_ec = pd.DataFrame(data_ec)

    return df_ec



import gspread
from google.oauth2.service_account import Credentials
import datetime
from gspread_dataframe import set_with_dataframe

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
data_udemy = get_data_udemy()

today = datetime.date.today().strftime('%Y/%m/%d')
data_udemy['date'] = today

df = pd.concat([df, pd.DataFrame([data_udemy])], ignore_index=True)
df.tail()

set_with_dataframe(worksheet, df, row=1, col=1)


import altair as alt

data = worksheet.get_all_values()
df_udemy = pd.DataFrame(data[1:], columns=data[0])

base = alt.Chart(df_udemy).encode(
    alt.X('date:T').axis(title=None)
)

df_udemy = df_udemy.astype({
    'n_subscriber': int,
    'n_review': int
})
y_min1 = df_udemy['n_subscriber'].min()-10
y_max1 = df_udemy['n_subscriber'].max()+10

y_min2 = df_udemy['n_review'].min()-10
y_max2 = df_udemy['n_review'].max()+10

line1 = base.mark_line(opacity=0.3, color='#57A44C').encode(
    alt.Y('n_subscriber', axis=alt.Axis(title='受講生数', titleColor='#57A44C'), scale=alt.Scale(domain=[y_max1, y_min1]))
)

line2 = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
    alt.Y('n_review', axis=alt.Axis(title='レビュー数', titleColor='#5276A7'), scale=alt.Scale(domain=[y_max2, y_min2]))
)

chart = alt.layer(line1, line2).resolve_scale(
    y='independent'
)
