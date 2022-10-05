import requests
from bs4 import BeautifulSoup
import json

root_url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=1"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'referer': 'https://www.immoweb.be/en'
}
house_html = requests.get(root_url, headers=header)
soup = BeautifulSoup(house_html.text, 'html.parser')

house_container = soup.find_all('main', class_='main')
house_list = []
for i in house_container:
    house_list.append(i)
print(type(house_list))
