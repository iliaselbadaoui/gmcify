import copy
from urllib.request import urlopen
import json
import sys
import html2text
import pandas as pd
from xmler import xmler

def find_gtin(brand:str):
    file = pd.read_csv(sys.argv[2])

    gtin = file.loc[file['brand'] == brand.lower()].get('gtin')

    if(len(gtin.to_numpy()) == 0):
        return ''
    else:
        return str(gtin.to_numpy()[0])

if len(sys.argv) != 3:
    print("error parsing the command")
    print("example: python3.10 gmcify.py [store_link]/products.json gtin.csv")
    print("csv format [brand, gtin]")
    sys.exit()

url = sys.argv[1]

response = urlopen(url)

Item = []
product = {
"id":'',
"title":'',
"link":'',
"description":'',
"g:image_link":'',
"g:price":'',
"g:availability":'in_stock',
"g:gtin":'',
"g:mpn":'',
"g:brand":'',
"g:update_typ":'merge'
}
data_json = json.loads(response.read()).get('products')
h2t = html2text.HTML2Text()
h2t.ignore_links = True
for prod in data_json:
    cp_prod = copy.deepcopy(product)
    cp_prod['id'] = prod.get('id')
    cp_prod['title'] = prod.get('title')
    cp_prod['link'] = sys.argv[1].split('/products.json')[0] + "/products/" + prod.get('handle')
    cp_prod['description'] = h2t.handle(prod.get('body_html'))
    cp_prod['g:price'] = prod.get('variants')[0].get('price')
    cp_prod['g:brand'] = prod.get('vendor')
    cp_prod['g:gtin'] = find_gtin(prod.get('vendor'))
    Item.append(cp_prod)

RSS = {
    "rss":
        {
            "version": "2.0",
            "xmlns:g": "http://base.google.com/ns/1.0",
            "chanel":
                {
                    'item': Item
                }
        }
}
print(xmler(RSS))
# xmler(RSS)