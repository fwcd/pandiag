import argparse
import sys

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from pandiag import dot, drawio, mermaid
from pandiag.model.graph import Graph
from pandiag.utils import help_escape

PLACEHOLDER = '%'

@dataclass
class Format:
    extensions: list[str] = field(default_factory=list)
    format: Optional[Callable[[Graph], str | bytes]] = None
    parse: Optional[Callable[[str], list[Graph]]] = None

FORMATS = {
    'dot': Format(extensions=['dot'], format=dot.format),
    'drawio': Format(extensions=['drawio'], parse=drawio.parse),
    'markdown': Format(extensions=['md', 'markdown'], format=mermaid.format_markdown),
    'mermaid': Format(extensions=[], format=mermaid.format),
    'pdf': Format(extensions=['pdf'], format=dot.format_pdf),
    'png': Format(extensions=['png'], format=dot.format_png),
}

def guess_format(path: Path) -> Optional[Format]:
    extension = path.name.rsplit('.', maxsplit=1)[-1]
    return next((f for f in FORMATS.values() if extension in f.extensions), None)

def main():
    parser = argparse.ArgumentParser(description='Utility for converting between diagram formats')
    parser.add_argument('-o', '--output', type=Path, required=True, metavar='PATH', help=f'The path to the output document. The file name must contain a {help_escape(PLACEHOLDER)} placeholder if the input document contains multiple graphs.')
    parser.add_argument('input', type=Path, help='The path to the input document.')

    args = parser.parse_args()
    input_path: Path = args.input
    output_template: Path = args.output
    
    if not (input_format := guess_format(input_path)):
        print(f'Unrecognized input format: {input_path.name}')
        sys.exit(1)
    
    if not (output_format := guess_format(output_template)):
        print(f'Unrecognized output format: {output_template.name}')
        sys.exit(1)

    if not input_format.parse:
        print('Input format does not support parsing')
        sys.exit(1)

    if not output_format.format:
        print('Output format does not support formatting')
        sys.exit(1)

    with open(input_path, 'r') as f:
        raw_input = f.read()

    graphs = input_format.parse(raw_input)

    if len(graphs) == 0:
        print('Input contains no graphs')
        sys.exit(1)

    if len(graphs) > 1 and (PLACEHOLDER not in output_template.stem):
        print(f'Output file name must contain a placeholder {PLACEHOLDER} since the input contains multiple ({len(graphs)}) graphs')
        sys.exit(1)

    for i, graph in enumerate(graphs):
        raw_output = output_format.format(graph)
        is_binary = isinstance(raw_output, bytes)

        if len(graphs) > 1:
            output_path = output_template.with_stem(output_template.stem.replace(PLACEHOLDER, f'{i:02d}'))
        else:
            output_path = output_template

        with open(output_path, 'wb' if is_binary else 'w') as f:
            f.write(raw_output)
