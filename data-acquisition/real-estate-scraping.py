import flatdict
import requests
from bs4 import BeautifulSoup
import re
from bs2json import bs2json
import json
import csv


root_url = "https://www.immoweb.be/nl/zoeken/huis-en-appartement/te-koop?countries=BE&page="
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'referer': 'https://www.immoweb.be/en'
}

for page in range(1, 334):
    links = root_url + str(page)

    house_html = requests.get(links, headers=header)
    soup = BeautifulSoup(house_html.text, 'html.parser')
    house_container = soup.find_all('main', class_='main')
    json1 = bs2json().convertAll(house_container, join=True)
    house_json = json1[0]['main'][0]['iw-search']['attributes'][':results']
    house_dict = json.loads(house_json)

    # to get each house page's url
    for i in range(0, 30):
        property_id = house_dict[i]['id']
        property_location = house_dict[i]['property']['location']["district"]
        property_postcode = house_dict[i]['property']['location']['postalCode']
        property_type = house_dict[i]['property']['type']
        property_transaction_type = "te-koop"

        each_house_base_url = "https://www.immoweb.be/nl/zoekertje/"
        link = f"{each_house_base_url}{property_type}/{property_transaction_type}/{property_location}/{property_postcode}/{property_id}"

        # to get each house's information
        property_request = requests.get(link, headers=header)
        property_soup = BeautifulSoup(property_request.text, 'html.parser')

        # convert json to dict, add location in the dict
        script_text = property_soup.find('script', text=re.compile("\s+window.dataLayer")).text.split('= ', 1)[1]
        json_data = json.loads(script_text[script_text.find('{'):script_text.rfind('}') + 1])
        property_info = json_data['classified']
        property_info['location'] = property_location

        # get required info from property_info
        key_lst = ['id', 'type', 'subtype', 'price', 'transactionType', 'kitchen', 'energy',
                   'bedroom', 'land',
                   'outdoor', 'wellnessEquipment', 'condition', 'location']
        required_property_info = {key: value
                                  for key, value in property_info.items()
                                  if key in key_lst}

        # flat the required_property_info
        flat_required_property_info = (flatdict.FlatDict(required_property_info, delimiter='.'))
        print(flat_required_property_info)

        with open('immo.csv', 'w', newline='', encoding='utf-8') as f:
            headers = ['id', 'type', 'subtype', 'price', 'transactionType', 'energy.heatingType', 'bedroom.count',
                       'land.surface', 'outdoor.garden.surface', 'outdoor.terrace.exists',
                       'wellnessEquipment.hasSwimmingPool', 'condition.isNewlyBuilt', 'location']
            writer = csv.DictWriter(f, fieldnames=required_property_info.keys())
            writer.writeheader()
            writer.writerow(required_property_info)


