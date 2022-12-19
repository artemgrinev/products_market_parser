from datetime import datetime

from response import Response
from data import Product


class ProductVprok:
    market_name = 'vprok'
    domain = 'https://www.vprok.ru'
    current_datetime = datetime.now()
    response = Response()

    def get_category(self):
        self.response.url = self.domain
        soup = self.response.get_soup()
        menu_urls = soup.find('nav', class_='fo-catalog-menu__nav').find_all('a')

        for i in menu_urls:
            name_category = i.text.replace('\n', '').strip()
            links_category = i.attrs['href']
            try:
                self.response.url = self.domain + links_category
                soup = self.response.get_soup()
                print(f'pars: {name_category} {links_category}')
                yield links_category
            except:
                print(f'missed {name_category}')
                continue

    def get_product(self):
        for link in self.get_category():
            page = 1
            next_page = 2

            while page <= next_page:
                print(f'Парсинг страницы {page}')
                links_page = f'{link}?page={page}'
                print(link)
                self.response.url = self.domain + links_page
                soup = self.response.get_soup()
                try:
                    next_page = int(
                        soup.find('a', class_='xf-paginator__item js-paginator__next').attrs['href'].split('=')[1])
                except AttributeError:
                    next_page = 1
                    print('В категории одна страница')
                try:
                    catalog_items = soup.find('ul', id='catalogItems').find_all('li')
                    for li in catalog_items:
                        product = Product()
                        try:
                            product_attrs = li.find('div', class_='xf-product js-product').attrs

                            product.market_name = self.market_name
                            product.domain = self.domain
                            product.product_id = product_attrs.get('data-owox-product-id')
                            product.product_name = product_attrs.get('data-owox-product-name')
                            product.price = product_attrs.get('data-owox-product-price')
                            product.is_available = product_attrs.get('data-owox-is-available')
                            product.measure = product_attrs.get('data-owox-fraction-text')
                            product.product_url = product_attrs.get('data-product-card-url')
                            product.vendor_name = product_attrs.get('data-owox-product-vendor-name')
                            product.category_name = product_attrs.get('data-owox-portal-name')
                            product.subcategory_name = product_attrs.get('data-owox-category-name')
                            product.category_url = product_attrs.get('data-category-url')
                            product.date = self.current_datetime.strftime("%d-%m-%y")

                            print('product: ' + product_attrs.get('data-owox-product-name') + ' recorded')
                            yield product.__dict__

                        except AttributeError:
                            pass
                except AttributeError:
                    pass
                page += 1

    def start_parser(self):
        products = self.get_product()
        return products
