import xml.etree.ElementTree as ET

def parse_webdav_xml(xml_text: str):
    ns = {
        "d": "DAV:",
        "oc": "http://owncloud.org/ns",
        "nc": "http://nextcloud.org/ns"
    }

    root = ET.fromstring(xml_text)
    items = []

    for resp in root.findall("d:response", ns):
        href = resp.find("d:href", ns)
        if href is None:
            continue

        propstat = resp.find("d:propstat", ns)
        if propstat is None:
            continue

        prop = propstat.find("d:prop", ns)
        if prop is None:
            continue

        item = {
            "path": href.text,
            "is_dir": prop.find("d:resourcetype/d:collection", ns) is not None,
            "last_modified": (prop.find("d:getlastmodified", ns).text
                              if prop.find("d:getlastmodified", ns) is not None else None),
            "size": (prop.find("d:getcontentlength", ns).text
                     if prop.find("d:getcontentlength", ns) is not None else None),
            "mime": (prop.find("d:getcontenttype", ns).text
                     if prop.find("d:getcontenttype", ns) is not None else None),
            "etag": (prop.find("d:getetag", ns).text
                     if prop.find("d:getetag", ns) is not None else None)
        }

        items.append(item)

    return items
