import requests
from bs4 import BeautifulSoup
import re
from bs2json import bs2json
import json
import csv
import collections
from joblib import Parallel, delayed

root_url = "https://www.immoweb.be/nl/zoeken/huis-en-appartement/te-koop?countries=BE&page="
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Referer': 'https://www.immoweb.be/'
}

for page in range(1, 334):
    links = root_url + str(page)

    house_html = requests.get(links, headers=header)
    soup = BeautifulSoup(house_html.text, 'html.parser')
    house_container = soup.find_all('main', class_='main')
    json1 = bs2json().convertAll(house_container, join=True)
    house_json = json1[0]['main'][0]['iw-search']['attributes'][':results']
    house_dict = json.loads(house_json)

    with open('immowebepc.csv', 'a', newline="", encoding='utf-8') as f:
        headers = ['id', 'type', 'subtype', 'price', 'transactionType', 'kitchen_type', 'energy_heatingType',
                   'bedroom_count', 'land_surface',
                   'outdoor_terrace_exists', 'outdoor_garden_surface', 'wellnessEquipment_hasSwimmingPool',
                   'condition_isNewlyBuilt', 'location', 'region', 'province', 'EPC']
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()


        # to get each house page's url
        def flatten(d, parent_key='', sep='_'):
            items = []
            for k, v in d.items():
                new_key = parent_key + sep + k if parent_key else k
                if isinstance(v, collections.abc.MutableMapping):
                    items.extend(flatten(v, new_key, sep=sep).items())
                else:
                    items.append((new_key, v))
            return dict(items)


        link_list = []
        for i in range(30):
            property_id = house_dict[i]['id']
            property_location = house_dict[i]['property']['location']["district"]
            property_postcode = house_dict[i]['property']['location']['postalCode']
            property_type = house_dict[i]['property']['type']
            property_transaction_type = "te-koop"

            each_house_base_url = "https://www.immoweb.be/nl/zoekertje/"
            link = f"{each_house_base_url}{property_type}/{property_transaction_type}/{property_location}/{property_postcode}/{property_id}"
            link_list.append(link)

            keys = ['id', 'region', 'province', 'EPC']
            dict_house = collections.defaultdict(list)
            for j in keys:
                if j == 'region':
                    dict_house[j].append(house_dict[i]['property']['location']['region'])
                elif j == 'province':
                    dict_house[j].append(house_dict[i]['property']['location']['province'])
                elif j == 'EPC':
                    dict_house[j].append(house_dict[i]['transaction']['certificate'])
                    dict_info = dict(dict_house)


        def scrape(link):
            # to get each house's information
            property_request = requests.get(link, headers=header)
            property_soup = BeautifulSoup(property_request.text, 'html.parser')

            # convert json to dict, add location in the dict
            script_text = property_soup.find('script', text=re.compile("\s+window.dataLayer")).text.split('= ', 1)[1]
            json_data = json.loads(script_text[script_text.find('{'):script_text.rfind('}') + 1])
            property_info = json_data["classified"]
            property_info['location'] = property_location
            property_info.update(dict_info)

            # get required info from property_info
            key_lst = ['id', 'type', 'subtype', 'price', 'transactionType', 'kitchen', 'energy',
                       'bedroom', 'land',
                       'outdoor', 'wellnessEquipment', 'condition', 'location', 'region', 'province', 'EPC']
            required_property_info = {key: value
                                      for key, value in property_info.items()
                                      if key in key_lst}

            # flat the required_property_info
            flat_required_property_info = flatten(required_property_info)

            # print(flat_required_property_info)
            writer.writerow(flat_required_property_info)


        Parallel(n_jobs=-3, require="sharedmem", verbose=10)(delayed(scrape)(link) for link in link_list)
