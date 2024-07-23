import argparse

from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Utility for converting between diagram formats')
    parser.add_argument('-o', '--output', type=Path, metavar='PATH', help='The path to the output document')
    parser.add_argument('input', help='The path to the input document')

    args = parser.parse_args()

    # TODO
