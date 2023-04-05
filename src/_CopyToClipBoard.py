
from typing import List, Union

import pyperclip


def materials(name: Union[str, List[str]], quality: Union[str, List[str]]) -> None:
    """
        MaterialType.TEST       : Material(MaterialType.TEST, Quality.COMMON),
    """
    if isinstance(name, list) & isinstance(quality, list):
        out = '\n'.join(
            f"    MaterialType.{n.upper():<11}: Material(MaterialType.{n.upper()}, Quality.{q.upper()}),"
            for n, q
            in zip(name, quality)
        )

    elif isinstance(name, str) & isinstance(quality, str):
        out = f"    MaterialType.{name.upper():<11}: Material(MaterialType.{name.upper()}, Quality.{quality.upper()}),"

    else:
        raise ValueError("Expected either two strings or two lists of strings.")

    print(out)
    pyperclip.copy(out)


def material_type(name: Union[str, List[str]]) -> None:
    """
        TEST        = "Test"
    """
    out = None

    if isinstance(name, list):
        out = '\n'.join(
            f'    {n.upper():<12}= "{n.title()}"'
            for n
            in name
        )

    elif isinstance(name, str):
        out = f'    {name.upper():<12}= "{name.title()}"'

    else:
        raise ValueError("Expected either a string or a list of strings.")

    print(out)
    pyperclip.copy(out)
