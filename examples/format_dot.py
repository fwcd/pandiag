from pandiag import dot
from pandiag.model import Graph, Subgraph, Edge

g = Graph(
    directed=True,
    rootgraph=Subgraph(
        edges=[
            Edge('a', 'b'),
            Edge('b', 'c'),
        ]
    )
)

print(dot.format(g))
