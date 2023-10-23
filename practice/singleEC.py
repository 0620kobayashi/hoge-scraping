from bs4 import BeautifulSoup
import requests

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

print(data_ec)