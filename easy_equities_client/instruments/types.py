from enum import Enum
from typing import List
import sys

if sys.version_info >= (3, 8):
    from typing import TypedDict  # pylint: disable=no-name-in-module
else:
    from typing_extensions import TypedDict


class Period(Enum):
    ONE_MONTH = 'OneMonth'
    THREE_MONTHS = 'ThreeMonths'
    SIX_MONTHS = 'SixMonths'
    ONE_YEAR = 'OneYear'
    MAX = 'Max'


class ChartData(TypedDict):
    Dataset: List[float]
    Labels: List[str]
    DailyChange: float
    PeriodReturn: float
    YMax: float
    YMin: float
    DailyChangeMonetaryValue: float
    TradingCurrencySymbol: str
    HasData: bool


class HistoricalPrices(TypedDict):
    success: bool
    chartData: ChartData
