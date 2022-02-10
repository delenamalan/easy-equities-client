from pydantic import BaseModel

from easy_equities_client.transactions.base_matchers import ContainStringAndRegexMatcher

alpha_num = r"[a-zA-Z0-9_&()]"
stock = rf"(?P<stock>(?:{alpha_num}+\s*?)*?)"
short_stock = r"(?P<stock>(?:\w+\s*?)*?)"
amount = r"(?P<amount>-?(?:\d|\.)+)"
value = r"(?P<value>-?(?:\d|\,|\.)+)"
amount_at_value = rf"{amount}\s+\@\s+{value}"


class BoughtTransaction(BaseModel):
    stock: str
    amount: float
    value: float


class BoughtMatcher(ContainStringAndRegexMatcher):
    """
    Example: "Bought Check Point Software Tech 0.3132 @ 12,692.00"
    """

    STRING_TO_CONTAIN = "Bought"
    REGEX_PATTERN = rf"Bought\s+{stock}\s+{amount_at_value}"
