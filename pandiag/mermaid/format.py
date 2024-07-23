from pandiag.model.graph import Edge, Graph, Subgraph
from pandiag.utils import indent

def _format_edge(edge: Edge, graph: Graph) -> str:
    return f"{edge.source} {'-->' if graph.directed else '---'} {edge.dest}"

def _format_subgraph(subgraph: Subgraph, graph: Graph) -> list[str]:
    # TODO: Subgraphs
    return [_format_edge(e, graph=graph) for e in subgraph.edges]

def _format_graph(graph: Graph) -> list[str]:
    return [
        'flowchart TD',
        *indent(_format_subgraph(graph.rootgraph, graph=graph)),
    ]

def format(graph: Graph) -> str:
    return '\n'.join(_format_graph(graph))
