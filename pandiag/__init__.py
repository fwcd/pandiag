import argparse
import sys

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from pandiag import dot, drawio, markdown, mermaid
from pandiag.model.graph import Graph

@dataclass
class Format:
    extensions: list[str] = field(default_factory=list)
    format: Optional[Callable[[Graph], str]] = None
    parse: Optional[Callable[[str], Graph]] = None

FORMATS = {
    'dot': Format(extensions=['dot'], format=dot.format),
    'drawio': Format(extensions=['drawio'], parse=drawio.parse),
    'markdown': Format(extensions=['md', 'markdown'], format=markdown.format),
    'mermaid': Format(extensions=[], format=mermaid.format),
}

def guess_format(path: Path) -> Optional[Format]:
    extension = path.name.rsplit('.', maxsplit=1)[-1]
    return next((f for f in FORMATS.values() if extension in f.extensions), None)

def main():
    parser = argparse.ArgumentParser(description='Utility for converting between diagram formats')
    parser.add_argument('-o', '--output', type=Path, required=True, metavar='PATH', help='The path to the output document')
    parser.add_argument('input', type=Path, help='The path to the input document')

    args = parser.parse_args()
    
    if not (input_format := guess_format(args.input)):
        print(f'Unrecognized input format: {args.input.name}')
        sys.exit(1)
    
    if not (output_format := guess_format(args.output)):
        print(f'Unrecognized output format: {args.output.name}')
        sys.exit(1)

    if not input_format.parse:
        print('Input format does not support parsing')
        sys.exit(1)

    if not output_format.format:
        print('Output format does not support formatting')
        sys.exit(1)

    with open(args.input, 'r') as f:
        raw_input = f.read()

    graph = input_format.parse(raw_input)
    raw_output = output_format.format(graph)

    with open(args.output, 'w') as f:
        f.write(raw_output)
