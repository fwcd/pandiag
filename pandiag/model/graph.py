from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Edge:
    source: Optional[str]
    dest: Optional[str]

@dataclass
class Subgraph:
    edges: list[Edge] = field(default_factory=list)
    subgraphs: list[Subgraph] = field(default_factory=list)

@dataclass
class Graph:
    directed: bool = False
    rootgraph: Subgraph = field(default_factory=Subgraph)
