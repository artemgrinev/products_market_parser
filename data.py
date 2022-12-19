from dataclasses import dataclass
import csv
from datetime import datetime


@dataclass
class Product:
    market_name: str = None
    product_id: str = None
    product_name: str = None
    price: str = None
    is_available: str = None
    measure: str = None
    product_url: str = None
    vendor_name: str = None
    category_name: str = None
    subcategory_name: str = None
    category_url: str = None
    date: str = None


def writer_csv(name, products):
    current_datetime = datetime.now()
    file_name = name + current_datetime.strftime("%d-%b-%y") + '.csv'
    print(file_name)
    with open(file_name, mode='w', encoding='utf-8') as csv_file:
        fieldnames = ['product_id', 'market_name', 'domain', 'product_name', 'vendor_name',
                      'price', 'is_available', 'measure', 'product_url',
                      'category_name', 'subcategory_name', 'category_url', 'date']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in products:
            writer.writerow(i)
