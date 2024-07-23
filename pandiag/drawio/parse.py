from __future__ import annotations
from dataclasses import dataclass, field
from pandiag.model.graph import Edge, Graph, Subgraph

import base64
import re
import urllib.parse
import xml.etree.ElementTree as ET
import zlib

@dataclass
class _Cell:
    element: ET.Element
    childs: list[_Cell] = field(default_factory=list)

def _strip_html(raw: str) -> str:
    # TODO: Be cleverer about this, perhaps use a proper HTML parser
    raw = raw.replace('<br>', ' ')
    raw = re.sub(f'<[^>]+>', '', raw)
    return raw

def _construct_subgraph(cells: list[_Cell], cells_by_id: dict[str, _Cell]) -> Subgraph:
    subgraph = Subgraph()

    # TODO: Perhaps support nodes and ids so we don't have to write the full labels into each edge?
    for cell in cells:
        if cell.element.attrib.get('edge') == '1':
            source = cells_by_id[cell.element.attrib['source']] if 'source' in cell.element.attrib else None
            target = cells_by_id[cell.element.attrib['target']] if 'target' in cell.element.attrib else None

            subgraph.edges.append(Edge(
                source=_strip_html(source.element.get('value')) if source else None,
                dest=_strip_html(target.element.get('value')) if target else None,
            ))
        
        if len(cell.childs) > 0:
            subsubgraph = _construct_subgraph(
                cells=cell.childs,
                cells_by_id=cells_by_id,
            )
            subsubgraph.name = cell.element.get('value')
            if subsubgraph.name:
                subgraph.subgraphs.append(subsubgraph)
            else:
                # Merge the subsubgraph into the current one
                subgraph.edges += subsubgraph.edges
                subgraph.subgraphs += subsubgraph.subgraphs
    
    return subgraph

def _parse_graph(element: ET.Element) -> Graph:
    cells_by_id = {cell.attrib['id']: _Cell(cell) for cell in element.findall('.//mxCell')}
    root_cells: list[_Cell] = []

    # Construct tree
    for id, cell in list(cells_by_id.items()):
        if parent := cell.element.attrib.get('parent'):
            cells_by_id[parent].childs.append(cell)
        else:
            root_cells.append(cell)

    return Graph(
        directed=True,
        rootgraph=_construct_subgraph(
            cells=root_cells,
            cells_by_id=cells_by_id
        ),
    )

def parse(raw: str) -> Graph:
    root_element = ET.fromstring(raw)

    graph_compressed = base64.b64decode(root_element.find('diagram[@name="New"]').text)
    graph_decompressed = zlib.decompress(graph_compressed, wbits=-15)
    graph_xml = urllib.parse.unquote(graph_decompressed)
    graph_element = ET.fromstring(graph_xml)

    return _parse_graph(graph_element)
