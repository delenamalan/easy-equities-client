import re
from typing import Any, Optional, Tuple


class BaseMatcher:
    def match(self, value: str) -> Tuple[bool, Optional[Any]]:
        raise NotImplementedError()


class ContainsStringMatcher:
    STRING_TO_CONTAIN = ""

    def match(self, value: str) -> bool:
        return self.STRING_TO_CONTAIN in value


class ContainStringAndRegexMatcher:
    STRING_TO_CONTAIN = ""
    REGEX_PATTERN = r""

    def match(self, value: str) -> Tuple[bool, Optional[Any]]:
        if self.STRING_TO_CONTAIN in value:
            re_match = re.compile(self.REGEX_PATTERN).fullmatch(value)
            if re_match:
                return True, re_match.groupdict()
        return False, None
