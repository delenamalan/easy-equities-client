from dataclasses import asdict
from typing import Iterable, List, TypeVar

_T = TypeVar("_T")


def list_of_dataclasses_to_dicts(values: Iterable[_T]) -> List[dict]:
    return list(map(asdict, values))
