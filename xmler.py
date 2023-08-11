def xmler(doc_object, xml_doc_str=None, ver='1.0', encode='utf-8'):
    if xml_doc_str is None:
        xml_doc = f'<?xml version="{ver}" encoding="{encode}"?>'
    else:
        xml_doc = xml_doc_str

    for prop in doc_object.keys():
        attr = ''
        if type(doc_object[prop]) == dict:
            xml_doc = xml_doc + f'\n<{prop}'
            if type(doc_object[prop]) == dict:
                for key in doc_object[prop].keys():
                    if type(doc_object[prop][key]) == str:
                        attr = attr + f' {key}="'+doc_object[prop][key]+'"'
            xml_doc = xml_doc + attr + ">"
            xml_doc = xmler(doc_object[prop], xml_doc)
        if type(doc_object[prop]) == list:
            lst = doc_object[prop]
            for i in range(0, len(lst)):
                item = lst[i]
                xml_doc = xml_doc + f'\n<{prop}>'
                for key in item.keys():
                    if type(item[key]) == str:
                        xml_doc = xml_doc + f'\n<{key}>{item[key]}</{key}>'
                    xml_doc = xmler(item, xml_doc)
                xml_doc = xml_doc + f'\n</{prop}>'
        if type(doc_object[prop]) == dict:
            xml_doc = xml_doc + f'\n</{prop}>'

    return xml_doc
