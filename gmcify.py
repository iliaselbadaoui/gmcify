import copy
from urllib.request import urlopen
import json
import sys
import html2text
from xmler import xmler

if len(sys.argv) != 2:
    print("Provide a store link")
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