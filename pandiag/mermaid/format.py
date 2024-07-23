from typing import Optional
from pandiag.model.graph import Edge, Graph, Subgraph
from pandiag.utils import indent

import hashlib
import re

def _format_node(label: Optional[str]) -> str:
    # TODO: Generate more readable node names than SHA1 hashes
    # TODO: Find a better way to sanitize the label
    label = re.sub(r'[()]', '', label).strip() if label else None
    return f"{hashlib.sha1(label.encode()).hexdigest()}[{label}]" if label else 'None'

def _format_edge(edge: Edge, graph: Graph) -> str:
    return f"{_format_node(edge.source)} {'-->' if graph.directed else '---'} {_format_node(edge.dest)}"

def _format_subgraph(subgraph: Subgraph, graph: Graph) -> list[str]:
    return [
        *(_format_edge(e, graph=graph) for e in subgraph.edges),
        *(l for g in subgraph.subgraphs for l in [
            f'subgraph {_format_node(g.name)}',
            *indent(_format_subgraph(g, graph)),
            'end',
        ]),
    ]

def _format_graph(graph: Graph) -> list[str]:
    return [
        'flowchart TD',
        *indent(_format_subgraph(graph.rootgraph, graph=graph)),
    ]

def format(graph: Graph) -> str:
    return '\n'.join(_format_graph(graph))

def format_markdown(graph: Graph) -> str:
    return '\n'.join([
        '```mermaid',
        format(graph),
        '```',
    ])
