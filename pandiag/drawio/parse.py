from pandiag.model.graph import Graph

import base64
import urllib.parse
import xml.etree.ElementTree as ET
import zlib

def parse(s: str) -> Graph:
    root_element = ET.fromstring(s)

    diag_compressed = base64.b64decode(root_element.find('diagram[@name="New"]').text)
    diag_decompressed = zlib.decompress(diag_compressed, wbits=-15)
    diag_xml = urllib.parse.unquote(diag_decompressed)
    diag_element = ET.fromstring(diag_xml)

    print(diag_xml)

    raise NotImplementedError()
