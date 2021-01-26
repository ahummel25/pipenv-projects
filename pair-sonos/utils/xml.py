from xml.dom.minidom import parseString


def prettify_xml(xml_string: str) -> str:
    """Prettify XML"""
    dom = parseString(xml_string)
    return dom.toprettyxml()
