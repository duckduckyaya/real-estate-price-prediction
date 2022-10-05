import requests
from bs2json import bs2json
from bs4 import BeautifulSoup
import json


def get_first_house_list():
    root_url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page="
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'referer': 'https://www.immoweb.be/en'
    }
    for page in range(1, 334):
        link = root_url + str(page)
        house_html = requests.get(link, headers=header)
        soup = BeautifulSoup(house_html.text, 'html.parser')

        house_container = soup.find_all('main', class_='main')
        converter = bs2json()
        json1 = converter.convertAll(house_container, join=True)
        string_house_info = json1[0]['main'][0]['iw-search']['attributes'][':results']
        new_dict = json.loads(string_house_info)
        for i in range(0, 29):
            new_dict_property = new_dict[i]['property']
            new_dict_property['price'] = new_dict[i]['price']['mainDisplayPrice']
            print(new_dict_property)


print(get_first_house_list())
