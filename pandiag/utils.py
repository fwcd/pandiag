def indent(lines: list[str], indent: str='  ') -> list[str]:
    return [f'{indent}{l}' for l in lines]
