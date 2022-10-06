import requests
from bs2json import bs2json
from bs4 import BeautifulSoup
import json

root_url = "https://www.immoweb.be/nl/zoeken/huis-en-appartement/te-koop?countries=BE&page="
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'referer': 'https://www.immoweb.be/en'
}


# to get general house list
def get_house_list():
    for page in range(1, 334):
        link = root_url + str(page)

        house_html = requests.get(link, headers=header)
        soup = BeautifulSoup(house_html.text, 'html.parser')

        house_container = soup.find_all('main', class_='main')
        converter = bs2json()
        json1 = converter.convertAll(house_container, join=True)
        dict_json = json1[0]['main'][0]['iw-search']['attributes'][':results']

        new_dict = json.loads(dict_json)
        return new_dict


# to get each page's url
def get_house_url():
    for i in range(0, 29):
        property_id = get_house_list()[i]['id']
        property_location = get_house_list()[i]['property']['location']["district"]
        property_postcode = get_house_list()[i]['property']['location']['postalCode']
        property_type = get_house_list()[i]['property']['type']
        propert_transaction_type = "te-koop"

        # get page's url
        each_house_base_url = "https://www.immoweb.be/nl/zoekertje/"
        each_house_url = f"{each_house_base_url}{property_type}/{propert_transaction_type}/{property_location}/{str(property_postcode)}/{str(property_id)}"

        # to request each house's url
        property_request = requests.get(each_house_url, headers=header)
        property_soup = BeautifulSoup(property_request.text, 'html.parser')

        # get js from each house html page convert them to dict
        value = property_soup.find_all('script', type='text/javascript')[0].text
        value_to_dict = value[value.find('{'):value.rfind('}') + 1]
        value_dict = dict(json.loads(value_to_dict))
        return value_dict


# to get each house's information
def get_house_dict():
    house_value_dict = {}
    for key in get_house_url():
        property_info = get_house_url()['property']
        property_info['price'] = get_house_url()['price']['mainValue']
        print(property_info)
        '''
        locality = property_info['location']
        locality_values = dict(list(locality.items())[:8])
        property_type = property_info['type']
        '''


get_house_list()
get_house_url()
get_house_dict()
