from pandiag.model.graph import Graph

import xml.etree.ElementTree as ET

def parse(s: str) -> Graph:
    element = ET.fromstring(s)
    print(element.find('diagram[name="New"]'))

    raise NotImplementedError()
