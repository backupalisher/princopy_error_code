import re
import requests
import file_utils
from time import sleep
from random import uniform
from bs4 import BeautifulSoup as bs


def get_html(url, useragent=None, proxy=None):
    t = uniform(2, 6)
    sleep(t)
    session = requests.Session()
    request = session.get(url=url, headers=useragent, proxies=proxy)
    if request.status_code == 200:
        return bs(request.text, 'lxml')
    else:
        print("Error " + str(request.status_code))
        return request.status_code


def get_pagination_index_models(soup):
    try:
        pagination = soup.find_all('div', class_='btnCell')[-1]
        pagination_links = pagination.find('a')['href']
        count = re.search(r'\d*$', pagination_links)
        return int(count[0])
    except:
        return 1


def parser_errors(soup, brand_name, model_name):
    result = []
    erc_list = soup.find('div', class_='ercList')
    erc_row = erc_list.find_all('li')
    for erc_li in erc_row:
        caption = erc_li.find('span').text.strip()
        if caption == 'Image:':
            img = erc_li.find('img')['src']
            value = file_utils.save_img(img, brand_name, model_name)
        else:
            value = re.sub(caption.strip(), '', erc_li.text).strip()
        result.append({
            'caption': caption[0:-1],
            'value': value,
        })
    return result


def get_brand_model_links(soup, parser_class_name):
    prod_list = []
    brand_list = soup.find('ul', class_=str(parser_class_name))
    brands = brand_list.find_all('li')
    for brand in brands:
        name = brand.find('a').text.strip()
        href = brand.find('a')['href']
        prod_list.append({
            'name': name,
            'href': 'https://printcopy.info/' + href,
        })
    return prod_list
