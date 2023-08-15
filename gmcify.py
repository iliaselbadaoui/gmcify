import copy
from urllib.request import urlopen
import json
import sys
import marko
import html2text
import pandas as pd
import html
from xmler import xmler

def find_gtin(brand:str, csvPath):
    file = pd.read_csv(csvPath)

    gtin = file.loc[file['brand'] == brand.lower()].get('gtin')

    if(len(gtin.to_numpy()) == 0):
        return ''
    else:
        return str(gtin.to_numpy()[0])

if len(sys.argv) not in range(5, 6):
    print("error parsing the command")
    print("example: python3.10 gmcify.py [store_link] title little_description output_file_name")
    sys.exit()

url = sys.argv[1]

response = urlopen(url+'/products.json')

Item = []
product = {
"g:id":' ',
"g:title":' ',
"g:link":' ',
"g:description":' ',
"g:image_link":' ',
"g:price":' ',
"g:availability":'in_stock',
"g:condition":'new',
"g:gtin":' ',
"g:mpn":' ',
"g:brand":' ',
"g:update_typ":'merge'
}

data_json = json.loads(response.read()).get('products')
h2t = html2text.HTML2Text()
h2t.ignore_links = True
for prod in data_json:
    cp_prod = copy.deepcopy(product)
    cp_prod['g:id'] = prod.get('id')
    cp_prod['g:title'] = prod.get('title')
    cp_prod['g:link'] = sys.argv[1].split('/products.json')[0] + "/products/" + prod.get('handle')
    cp_prod['g:description'] = html.escape(h2t.handle(marko.convert(prod.get('body_html'))))
    cp_prod['g:price'] = prod.get('variants')[0].get('price') + " USD"
    cp_prod['g:brand'] = prod.get('vendor')
    if len(sys.argv) == 3:
        cp_prod['g:gtin'] = find_gtin(prod.get('vendor'))
    else:
        cp_prod['g:gtin'] = prod.get('variants')[0].get('product_id')
    Item.append(cp_prod)

RSS = {
    "rss":
        {
            "@version": "2.0",
            "@xmlns:g": "http://base.google.com/ns/1.0",
            "chanel":
                {
                    'title': sys.argv[2],
                    'link': sys.argv[1],
                    'description': sys.argv[3],
                    'item': Item
                }
        }
}

out = open(sys.argv[4], 'a')
out.write(xmler(RSS))
out.close()