from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Edge:
    source: str
    dest: str

@dataclass
class Subgraph:
    edges: list[Edge]
    subgraphs: list[Subgraph]

@dataclass
class Graph:
    directed: bool
    rootgraph: Subgraph
