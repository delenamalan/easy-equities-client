import sys
from dataclasses import dataclass
from typing import List, Optional

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


@dataclass
class Account:
    id: str
    name: str
    trading_currency_id: str


class Holding(TypedDict, total=False):
    name: str
    contract_code: str
    purchase_value: str
    current_value: str
    current_price: str
    img: str
    view_url: str
    isin: str


class Transaction(TypedDict):
    TransactionId: int
    DebitCredit: float
    Comment: str
    TransactionDate: str
    LogId: int
    ActionId: int
    Action: str
    ContractCode: str


class LabelValue(TypedDict):
    Label: str
    Value: str


class Valuation(TypedDict):
    NetInterestOnCashItems: List[LabelValue]
    AccrualSummaryItems: List[LabelValue]
    TopSummary: dict
    InvestmentTypesAndManagers: dict
    InvestmentSummaryItems: list
    CostsSummaryItems: list
    FundSummaryItems: list
    AccrualIncomeSummaryItems: Optional[list]
    AccrualExpenseSummaryItems: Optional[list]
