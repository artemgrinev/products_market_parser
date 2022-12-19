from datetime import datetime

from response import Response
from data import Product


class ProductOkay:
    market_name = 'okay'
    domain = 'https://www.okeydostavka.ru'
    current_datetime = datetime.now()
    response = Response()

    def get_category(self):
        self.response.url = self.domain
        soup = self.response.get_soup()
        all_menu = soup.find('ul', id='allDepartmentsMenu').find_all('li', class_='catalog-menu__department')

        for i in all_menu:
            product = Product()
            product.category_name = i.find('div', class_="menu-label").text.replace("\n", "").replace("\t", "")
            url_list = i.find('ul', class_='categoryList catalog-menu__category-list')
            if url_list is not None:
                subcategory_list = url_list.find_all('li')
                for j in subcategory_list:
                    product.subcategory_name = j.find('a', class_='menuLink').text.strip()
                    product.category_url = j.find('a', class_='menuLink').attrs['href']
                    print(product.subcategory_name)
                    yield product

    def get_product(self):
        for product in self.get_category():
            self.response.url = self.domain + product.category_url
            soup = self.response.proxy_zyte()
            try:
                products_soup = soup.find('ul', class_='grid_mode grid rows').find_all('li')
                for i in products_soup:
                    try:
                        product_weight = i.find('div', class_='product-weight').text.split()
                        self.response.url = self.domain + i.find('a').attrs['href']
                        product_soup = self.response.proxy_zyte()

                        product.product_id = i.find('div', class_='product-cart').find('a').attrs['data-entry-id']
                        product.product_name = i.find('a').attrs['title']
                        product.price = i.find('div', class_='product-cart').find('a').attrs['data-price']
                        product.is_available = product_weight[0]
                        product.measure = product_weight[1]
                        product.product_url = i.find('a').attrs['href']
                        product.vendor_name = product_soup.find('div', class_='tab-container-bordered') \
                            .find('div', class_='attributes__value').text.strip()
                        product.date = self.current_datetime.strftime("%d-%m-%y")
                        print(f'        {product.product_name}')
                        yield product.__dict__
                    except:
                        continue
            except:
                continue

    def start_parser(self):
        products = self.get_product()
        return products
