import re
import os
import csv
import glob
import time
import shutil
import requests


def save_model_links_csv(prods, brand_name, model_name):
    for prod in prods:
        if not os.path.exists(brand_name):
            os.mkdir(brand_name)
        with open(os.path.join(os.path.dirname(__file__), brand_name, model_name), 'a', encoding='utf-8') as file:
            add_data = csv.writer(file, delimiter=';', lineterminator='\n')
            add_data.writerow((prod['name'], prod['href']))


def save_error_code(ercs, brand_name, model_name):
    if not os.path.exists(brand_name):
        os.mkdir(brand_name)
    for erc in ercs:
        with open(os.path.join(os.path.dirname(__file__), brand_name, f'{model_name}.csv'), 'a',
                  encoding='utf-8') as file:
            try:
                add_data = csv.writer(file, delimiter=';', lineterminator='\n')
                add_data.writerow((erc['caption'], erc['value']))
            except:
                pass


def spaseSub(text):
    result = re.sub('\s', '', text)
    return result


def load_link(file_name):
    model_link = []
    with open(file_name, 'r', newline='') as file:
        line_read = csv.reader(file, delimiter=';', lineterminator='\n')
        for row in line_read:
            model_link.append({
                'name': row[0],
                'href': row[1],
            })
    return model_link


def load_links_brand():
    models_links = []
    files = glob.glob('./links/*')
    for f in files:
        models_links.append(load_link(os.path.join(os.path.dirname(__file__), f)))
    return models_links


def save_img(url, brand_name, model_name):
    r = requests.get('http://printcopy.info/' + url, stream=True)
    if r.status_code == 200:
        timestamp = str(round(time.time() * 1000))

        if not os.path.exists(brand_name + '_image'):
            os.mkdir(brand_name + '_image')
        file_name = spaseSub(model_name) + '_' + timestamp + '.png'
        with open(os.path.join(os.path.dirname(__file__), brand_name + '_image', file_name),
                  'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    file_name = brand_name + '/' + file_name
    return file_name
