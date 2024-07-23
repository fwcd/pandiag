from typing import Optional
from pandiag.model.graph import Edge, Graph, Node, Subgraph
from pandiag.utils import indent

import subprocess

def _format_label(label: Optional[str]) -> str:
    return f'"{label.strip()}"' if label else None

def _format_node(node: Node) -> str:
    return f'{_format_label(node.label)};'

def _format_edge(edge: Edge, graph: Graph) -> str:
    return f"{_format_label(edge.source)} {'->' if graph.directed else '--'} {_format_label(edge.dest)};"

def _format_subgraph(subgraph: Subgraph, graph: Graph) -> list[str]:
    return [
        *(_format_node(n) for n in subgraph.nodes),
        *(_format_edge(e, graph=graph) for e in subgraph.edges),
        *(l for g in subgraph.subgraphs for l in [
            f"subgraph {_format_label(f'cluster_{g.name}')} {{",
            *indent([
                *([f'label = {_format_label(g.name)};'] if g.name else ''),
                *_format_subgraph(g, graph),
            ]),
            '}',
        ]),
    ]

def _format_graph(graph: Graph) -> list[str]:
    return [
        f"{'digraph' if graph.directed else 'graph'} {_format_label(graph.rootgraph.name)} {{",
        *indent(_format_subgraph(graph.rootgraph, graph=graph)),
        '}',
    ]

def format(graph: Graph) -> str:
    return '\n'.join(_format_graph(graph))

def format_rendered(graph: Graph, render_format: str) -> bytes:
    result = subprocess.run(
        ['dot', '-T', render_format],
        input=format(graph).encode(),
        capture_output=True
    )
    return result.stdout

def format_png(graph: Graph) -> bytes:
    return format_rendered(graph, 'png')

def format_pdf(graph: Graph) -> bytes:
    return format_rendered(graph, 'pdf')
