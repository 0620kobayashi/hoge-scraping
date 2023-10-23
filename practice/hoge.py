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
