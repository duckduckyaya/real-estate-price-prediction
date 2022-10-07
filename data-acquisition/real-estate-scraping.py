import csv

import requests
from bs2json import bs2json
from bs4 import BeautifulSoup
import json
import re
import csv

root_url = "https://www.immoweb.be/nl/zoeken/huis-en-appartement/te-koop?countries=BE&page="
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
    dict_json = json1[0]['main'][0]['iw-search']['attributes'][':results']
    new_dict = json.loads(dict_json)

    # to get each page's url
    for i in range(0, 29):
        property_id = new_dict[i]['id']
        property_location = new_dict[i]['property']['location']["district"]
        property_postcode = new_dict[i]['property']['location']['postalCode']
        property_type = new_dict[i]['property']['type']
        property_transaction_type = "te-koop"

        each_house_base_url = "https://www.immoweb.be/nl/zoekertje/"
        each_house_url = f"{each_house_base_url}{property_type}/{property_transaction_type}/{property_location}/{property_postcode}/{property_id}"

        # to get each house's information

        property_request = requests.get(each_house_url, headers=header)
        property_soup = BeautifulSoup(property_request.text, 'html.parser')

        # convert json string to dict
        script_text = property_soup.find('script', text=re.compile("\s+window.dataLayer")).text.split('= ', 1)[1]
        json_data = json.loads(script_text[script_text.find('{'):script_text.rfind('}') + 1])
        property_info = json_data['classified']
        property_info['location'] = property_location
        #print(property_info)

# convert to csv

        colum_name = ['id', 'type', 'subtype', 'price', 'transactionType', 'zip', 'visualisationOption', 'kitchen',
                      'building',
                      'energy', 'certificates', 'bedroom', 'land', 'atticExists', 'basementExists', 'outdoor',
                      'specificities',
                      'wellnessEquipment', 'parking', 'condition', 'location']
        file_name = 'scrape_immoweb.csv'
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter='\t', fieldnames=colum_name)
            writer.writeheader()
            writer.writerow(property_info)
