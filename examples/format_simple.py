from pandiag import dot, markdown, mermaid
from pandiag.model import Graph, Subgraph, Edge

import argparse

FORMATTERS = {
    'dot': dot.format,
    'markdown': markdown.format,
    'mermaid': mermaid.format,
}

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
    parser.add_argument('-f', '--format', choices=sorted(FORMATTERS.keys()), default='dot')

    args = parser.parse_args()
    s = FORMATTERS[args.format](GRAPH)
    if args.output and args.output != '-':
        with open(args.output, 'w') as f:
            f.write(s)
    else:
        print(s)

if __name__ == '__main__':
    main()
