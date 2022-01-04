import re

alpha_num = r"[a-zA-Z0-9_&()]"
stock = rf"(?P<stock>(?:{alpha_num}+\s*?)*?)"
short_stock = r"(?P<stock>(?:\w+\s*?)*?)"
amount = r"(?P<amount>-?(?:\d|\.)+)"
value = r"(?P<value>-?(?:\d|\,|\.)+)"
amount_at_value = rf"{amount}\s+\@\s+{value}"
TRANSACTION_PATTERN_DIVIDENDS = rf"{stock}\s*-(?:Foreign\s+)?\s*Dividends\s+\@{amount}"  # e.g. "Schroder European Real Estate Inv Trust PLC-Foreign Dividends @31.49625"

TRANSACTION_PATTERN_DIVIDEND_TAX = rf"(?:Foreign\s+)?Dividend Withholding Tax\s+{short_stock}-(?:Foreign\s+)?Dividend Withholding Tax\s+(?:on Dividends\s+)?\@(?P<perc>{amount})\%"  # e.g. "Dividend Withholding Tax SCD-Dividend Withholding Tax @20%"
TRANSACTION_PATTERN_BOUGHT = rf"Bought\s+{stock}\s+{amount_at_value}"  # example "Bought Check Point Software Tech 0.3132 @ 12,692.00"

TRANSACTION_PATTERN_CORPORATE_ACTION = rf"Corporate Action\s+{stock}\s+{amount}\s+\@\s+{value}"  # e.g. "Corporate Action COHN 25.6147 @ 0"

TRANSACTION_PATTERN_BROKER_COMMISSION = rf"Broker Commission\s+{stock}\s+\@\s+{value}\%?"  # e.g. "Broker Commission Western Digital Corp @ 0.25%"

TRANSACTION_PATTERN_SOLD = rf"Sold\s+{stock}\s+{amount_at_value}"  # e.g. "Sold RFG Holdings Limited 17.9682 @ 1,291.00"
TRANSACTION_PATTERN_PORTFOLIO_COST = rf"{stock}-Issuer Portfolio Cost\s+\@{value}"  # e.g. "SYGNIA ITRIX MSCI JAPAN-Issuer Portfolio Cost @-7.59871"
TRANSACTION_PATTERN_RELEASE_FUNDS = (
    r"RELEASE Reserved funds for Buying Instruction: (?P<instruction>\d+)"
)
TRANSACTION_PATTERN_CURRENCY_TRANSFER = (
    r"(?P<instruction>\d+)\s+(?P<accountnum>EE\d+-\d+)"
)

TRANSACTION_PATTERN_SECURITIES_INTEREST = rf"{stock}-Securities Interest\s+@{amount}"  # e.g. "SYGNIA ITRIX EUROSTOXX50-Securities Interest @1.70261"
TRANSACTION_PATTERN_REIT_DISTRIBUTION = rf"{stock}-REIT Distribution\s+@{amount}"  # e.g. "Satrix 40 ETF-REIT Distribution @2.64919"


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
    """
    e.g. "Schroder European Real Estate Inv Trust PLC-Foreign Dividends @31.49625"
    """
    return "Dividends" in value and re.compile(TRANSACTION_PATTERN_DIVIDENDS).fullmatch(
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


def match_broker_commission(value):
    """
    e.g. "Broker Commission Western Digital Corp @ 0.25%"
    """
    return "Broker Commission" in value and re.compile(
        TRANSACTION_PATTERN_BROKER_COMMISSION
    ).fullmatch(value)


def match_sold(value):
    """
    e.g. "Sold RFG Holdings Limited 17.9682 @ 1,291.00"
    """
    return "Sold" in value and re.compile(TRANSACTION_PATTERN_SOLD).fullmatch(value)


def match_portfolio_cost(value):
    """
    e.g. "SYGNIA ITRIX MSCI JAPAN-Issuer Portfolio Cost @-7.59871"
    """
    return "Issuer Portfolio Cost" in value and re.compile(
        TRANSACTION_PATTERN_PORTFOLIO_COST
    ).fullmatch(value)


def match_transfer(value):
    """
    e.g. "Transfer into 3125158"
    """
    return "Transfer" in value


def match_reserve_funds(value):
    """
    e.g. "Reserve funds for Buying Instruction: : 19132518"
    """
    return "Reserve funds for Buying Instruction" in value


def match_trading_fee(value):
    """
    e.g. "FINRA Trading Activity Fee"
    """
    return "Trading Activity Fee" in value


def match_release_reserved_funds(value):
    """
    e.g. "RELEASE Reserved funds for Buying Instruction: 16187687"
    """
    return "RELEASE Reserved funds for Buying Instruction" in value and re.compile(
        TRANSACTION_PATTERN_RELEASE_FUNDS
    ).fullmatch(value)


def match_other_expenses(value):
    """
    e.g. "SYGNIA ITRIX MSCI JAPAN-Other Expenses @-0.01307"
    """
    return "Other Expenses" in value


def match_securities_transfer_tax_and_administration(value):
    return "Securities transfer tax and administration" == value


def match_currency_transfer(value):
    """
    e.g. "62203342514 EE173766-504129"
    """
    return re.compile(TRANSACTION_PATTERN_CURRENCY_TRANSFER).fullmatch(value)


def match_clearing_services(value):
    return "Clearing Services and other administration" == value


def match_securities_interest(value):
    """
    e.g. "SYGNIA ITRIX EUROSTOXX50-Securities Interest @1.70261"
    """
    return "Securities Interest" in value and re.compile(
        TRANSACTION_PATTERN_SECURITIES_INTEREST
    ).fullmatch(value)


def match_reit_distribution(value):
    """
    e.g. "Satrix 40 ETF-REIT Distribution @2.64919"
    """
    return "REIT Distribution" in value and re.compile(
        TRANSACTION_PATTERN_REIT_DISTRIBUTION
    ).fullmatch(value)


def match_sec_fees(value):
    return "SEC Fees" == value


def match_vat(value):
    return (
        "Value Added Tax on costs (VAT)" == value
        or "Value Added Tax on costs (VAT) on fee." == value
    )


def match_investor_protection_levy(value):
    return "Investor protection levy (IPL) and administration"


transaction_matching_functions = [
    match_investor_protection_levy,
    match_vat,
    match_sec_fees,
    match_clearing_services,
    match_securities_transfer_tax_and_administration,
    match_balance_carried_forward,
    match_interest,
    match_cash_management_fee,
    match_cash_management_fee_vat,
    match_dividend_withholding_tax,
    match_dividends_received,
    match_bought,
    match_corporate_action,
    match_broker_commission,
    match_sold,
    match_portfolio_cost,
    match_transfer,
    match_reserve_funds,
    match_trading_fee,
    match_release_reserved_funds,
    match_other_expenses,
    match_securities_interest,
    match_reit_distribution,
    match_currency_transfer,
]
