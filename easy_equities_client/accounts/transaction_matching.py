import re

stock = r"(?P<stock>(?:\S+\s*?)*?)"
amount = r"(?P<amount>\d+.\d+)"
value = r"(?P<value>(?:\d|\,|\.)+)"
TRANSACTION_PATTERN_DIVIDENDS = rf"{stock}\s*Dividends\s+\@{amount}"  # e.g. "Schroder European Real Estate Inv Trust PLC-Foreign Dividends @31.49625"
# TRANSACTION_PATTERN_DIVIDENDS = r"(?P<stock>(?:\S+\s*?)*?)\s*Dividends\s+\@(?P<amount>\d+.\d+)" # e.g. "Schroder European Real Estate Inv Trust PLC-Foreign Dividends @31.49625"

TRANSACTION_PATTERN_DIVIDEND_TAX = r"Dividend Withholding Tax (?P<stock>(?:\S+\s*?)+?)-Dividend Withholding Tax \@(?P<perc>\d+)\%"  # e.g. "Dividend Withholding Tax SCD-Dividend Withholding Tax @20%"
TRANSACTION_PATTERN_BOUGHT = r"Bought\s+(?P<stock>(?:\S+\s*?)+?)\s+(?P<amount>(?:\d|\.)+)\s+\@\s+(?P<value>(?:\d|\,|\.)+)"  # example "Bought Check Point Software Tech 0.3132 @ 12,692.00"

TRANSACTION_PATTERN_CORPORATE_ACTION = rf"Corporate Action\s+{stock}\s+{amount}\s+\@\s+{value}"  # e.g. "Corporate Action COHN 25.6147 @ 0"


def eq(pattern, value):
    return pattern == value


def match_balance_carried_forward(value):
    return (
        value == "Account Balance Carried Forward"
        or value == "Account Balance Brought Forward"
    )


def match_interest(value):
    return value == "Interest"


def match_cash_management_fee(value):
    return value == "Cash Management Fee"


def match_cash_management_fee_vat(value):
    return value == "VAT on Cash Management Fee"


def match_dividends_received(value):
    return "Dividens" in value and re.compile(TRANSACTION_PATTERN_DIVIDENDS).fullmatch(
        value
    )


def match_dividend_withholding_tax(value):
    return "Dividend Withholding Tax" in value and re.compile(
        TRANSACTION_PATTERN_DIVIDEND_TAX
    ).fullmatch(value)


def match_bought(value):
    """
    Example: "Bought Check Point Software Tech 0.3132 @ 12,692.00"
    """
    return "Bought" in value and re.compile(TRANSACTION_PATTERN_BOUGHT).fullmatch(value)


def match_corporate_action(value):
    """
    e.g. "Corporate Action COHN 25.6147 @ 0"
    """
    return "Corporate Action" in value and re.compile(
        TRANSACTION_PATTERN_CORPORATE_ACTION
    ).fullmatch(value)


transaction_matching_functions = [
    match_balance_carried_forward,
    match_interest,
    match_cash_management_fee,
    match_cash_management_fee_vat,
    match_dividends_received,
    match_dividend_withholding_tax,
    match_bought,
]
