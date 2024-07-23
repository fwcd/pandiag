from pandiag import mermaid
from pandiag.model.graph import Graph

def format(graph: Graph) -> str:
    return '\n'.join([
        '```mermaid',
        mermaid.format(graph),
        '```',
    ])
