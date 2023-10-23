from bs4 import BeautifulSoup
import requests

url ="https://scraping-for-beginner.herokuapp.com/udemy"
res = requests.get(url)

soup = BeautifulSoup(res.text, 'html.parser')
n_subscriber = soup.find('p', {'class':'subscribers'}).text
n_subscriber = int(n_subscriber.split('：')[1])

n_review = soup.find('p', {'class':'reviews'}).text
n_review = int(n_review.split('：')[1])

print(n_subscriber)
print(n_review)