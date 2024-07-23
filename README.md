# Pandiag

[![PyPI](https://img.shields.io/pypi/v/pandiag)](https://pypi.org/project/pandiag)

A tool for converting between different diagram formats, including

- draw.io (input only)
- DOT/GraphViz (output only)
- Mermaid (output only)

> [!IMPORTANT]
> The tool is highly experimental and can currently only parse/represent/format a small subset of diagrams.

## Example

Converting a draw.io diagram to DOT:

```sh
pandiag somediagram.drawio -o somediagram.dot
```

Converting a draw.io diagram to PDF (requires GraphViz to be installed):

```sh
pandiag somediagram.drawio -o somediagram.pdf
```
