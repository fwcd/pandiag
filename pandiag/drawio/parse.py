from pandiag.model.graph import Edge, Graph

import base64
import re
import urllib.parse
import xml.etree.ElementTree as ET
import zlib

def _strip_html(raw: str) -> str:
    # TODO: Be cleverer about this, perhaps use a proper HTML parser
    raw = raw.replace('<br>', ' ')
    raw = re.sub(f'<[^>]+>', '', raw)
    return raw

def _parse_graph(element: ET.Element) -> Graph:
    graph = Graph(directed=True)
    cells = {cell.attrib['id']: cell for cell in element.findall('.//mxCell')}

    # TODO: Perhaps support nodes and ids so we don't have to write the full labels into each edge?
    for cell in cells.values():
        if cell.attrib.get('edge') == '1':
            source = cells[cell.attrib['source']] if 'source' in cell.attrib else None
            target = cells[cell.attrib['target']] if 'target' in cell.attrib else None

            graph.rootgraph.edges.append(Edge(
                source=_strip_html(source.get('value')) if source else None,
                dest=_strip_html(target.get('value')) if target else None,
            ))

    return graph

def parse(raw: str) -> Graph:
    root_element = ET.fromstring(raw)

    graph_compressed = base64.b64decode(root_element.find('diagram[@name="New"]').text)
    graph_decompressed = zlib.decompress(graph_compressed, wbits=-15)
    graph_xml = urllib.parse.unquote(graph_decompressed)
    graph_element = ET.fromstring(graph_xml)

    return _parse_graph(graph_element)
