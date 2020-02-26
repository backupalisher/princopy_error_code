import os
import re
import get_proxy
import http_utils as parser
import file_utils


def get_save_links():
    url = 'https://printcopy.info/?mod=erc'
    proxy = {'http': 'http://' + get_proxy.get_proxies_list()}
    useragent = {'User-Agent': get_proxy.get_useregent_list()}
    brand_list = parser.get_brand_model_links(parser.get_html(url, useragent, proxy), 'brandList')

    for brand in brand_list:
        print(brand['name'])
        proxy = {'http': 'http://' + get_proxy.get_proxies_list()}
        useragent = {'User-Agent': get_proxy.get_useregent_list()}

        # присваиваем html страницу в переменную soup
        soup = parser.get_html(brand['href'], useragent, proxy)
        page_count = parser.get_pagination_index_models(soup)
        print(page_count)
        model_link = parser.get_brand_model_links(soup, 'modelList')
        file_utils.save_model_links_csv(model_link, brand['name'], brand['name'])
        if page_count > 1:
            for i in range(page_count):
                index = i + 2
                if index <= page_count:
                    model_link = parser.get_brand_model_links(
                        parser.get_html(brand['href'] + f'&page={index}', useragent, proxy),
                        'modelList')
                    file_utils.save_model_links_csv(model_link, brand['name'], brand['name'])


def parser_models():
    i = 0
    model_links = file_utils.load_links_brand()
    for brand in model_links:
        for model in brand:
            i += 1
            proxy = {'http': 'http://' + get_proxy.get_proxies_list()}
            useragent = {'User-Agent': get_proxy.get_useregent_list()}

            # присваиваем html страницу в переменную soup
            soup = parser.get_html(model['href'], useragent, proxy)
            page_count = parser.get_pagination_index_models(soup)
            model_name = model['name']
            brands = re.findall('^[^\s]+', model_name)
            brand_name = brands[0]
            print(str(i) + ': ' + model_name + ', page count: ' + str(page_count))
            erc_csv = parser.parser_errors(soup, brand_name, model_name)
            file_utils.save_error_code(erc_csv, brand_name, model_name)
            if page_count > 1:
                for i in range(page_count):
                    index = i + 2
                    if index <= page_count:
                        soup = parser.get_html(model['href'] + f'&page={index}', useragent, proxy)
                        erc_csv = parser.parser_errors(soup, brand_name, model_name)
                        file_utils.save_error_code(erc_csv, brand_name, model_name)
            break
        break


# code
# image
# display
# causes
# description
# remedy

def main():
    parser_models()
    # get_save_links()


if __name__ == '__main__':
    main()
