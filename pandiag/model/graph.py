from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Edge:
    source: str
    dest: str

@dataclass
class Subgraph:
    edges: list[Edge] = field(default_factory=list)
    subgraphs: list[Subgraph] = field(default_factory=list)

@dataclass
class Graph:
    directed: bool = False
    rootgraph: Subgraph = field(default_factory=Subgraph)
