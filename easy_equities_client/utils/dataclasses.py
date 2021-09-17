from typing import Iterable, List, TypeVar

from dataclasses import asdict

_T = TypeVar("_T")


def list_of_dataclasses_to_dicts(values: Iterable[_T]) -> List[dict]:
    return list(map(asdict, values))
