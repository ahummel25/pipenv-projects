import xml.dom.minidom


def prettify_xml(xml_string: str) -> str:
    """Prettify XML"""
    dom = xml.dom.minidom.parseString(xml_string)
    return dom.toprettyxml()
