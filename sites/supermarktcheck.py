import requests
from bs4 import BeautifulSoup
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

base_url = 'https://www.supermarktcheck.de/'

categories_page = requests.get(base_url + 'lebensmittel-nach-kategorie/?search=vegan', headers=headers)

categories_soup = BeautifulSoup(categories_page.text, 'html.parser')

categories_divs = categories_soup.find(id='initialResults').find_all('div')

data = {
     'categories': {}
}

for categories_div in categories_divs:
     data['categories'].update({categories_div.find('a').text : []})
     

def extract_data(category, soup):
        items = soup.select('.productListElement')

        for item in items:
            data['categories'][category].append(item.find(class_='h3').text)

for category_div in categories_divs:
    category = category_div.find('a').text

    category_url = base_url + category_div.find('a').get('href')

    first_pagination_page = requests.get(category_url, headers=headers)

    first_pagination_soup = BeautifulSoup(first_pagination_page.text, 'html.parser')

    extract_data(category, first_pagination_soup)

    next_pagination_page = first_pagination_soup.find('a', attrs={"rel": "next"})

    while next_pagination_page is not None:
        current_pagination_soup = BeautifulSoup(next_pagination_page.text, 'html.parser')

        extract_data(category, current_pagination_soup)
        
        next_pagination_page = current_pagination_soup.find('a', attrs={"rel": "next"})

print(json.dumps(data, indent=2))