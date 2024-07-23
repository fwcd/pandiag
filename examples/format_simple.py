from pandiag import FORMATS
from pandiag.model import Graph, Subgraph, Edge

import argparse

GRAPH = Graph(
    directed=True,
    rootgraph=Subgraph(
        edges=[
            Edge('a', 'b'),
            Edge('b', 'c'),
            Edge('b', 'd'),
        ]
    )
)

def main():
    parser = argparse.ArgumentParser(description='Formats a simple graph')
    parser.add_argument('-o', '--output', help='The output file path')
    parser.add_argument('-f', '--format', choices=sorted(FORMATS.keys()), default='dot')

    args = parser.parse_args()
    raw_output = FORMATS[args.format].format(GRAPH)

    if args.output and args.output != '-':
        with open(args.output, 'w' if isinstance(raw_output, str) else 'wb') as f:
            f.write(raw_output)
    else:
        print(raw_output)

if __name__ == '__main__':
    main()
