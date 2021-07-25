from enum import Enum


class CustomEnum(Enum):
    @classmethod
    def values(cls):
        return [p.value for p in cls.__members__.values()]


class Platform(CustomEnum):
    EASY_EQUITIES_ZA = "EasyEquitiesZA"
    SATRIX = "Satrix"


# Platform constants

EASY_EQUITIES_BASE_PLATFORM_URL = "https://platform.easyequities.io"
SATRIX_BASE_PLATFORM_URL = "https://platform.satrixnow.co.za"

PLATFORM_SIGN_IN_PATH = "/Account/SignIn"
PLATFORM_ACCOUNT_OVERVIEW_PATH = "/AccountOverview"
PLATFORM_CAN_USE_ACCOUNT_PATH = "/Menu/CanUseSelectedAccount"
PLATFORM_UPDATE_CURRENCY_PATH = "/Menu/UpdateCurrency"
PLATFORM_ACCOUNT_VALUATIONS_PATH = "/AccountOverview/GetTrustAccountValuations"
PLATFORM_HOLDINGS_PATH = "/AccountOverview/GetHoldingsView?stockViewCategoryId=12"
PLATFORM_TRANSACTIONS_PATH = "/TransactionHistory/GetTransactions"
PLATFORM_GET_CHART_DATA_PATH = "/Equity/GetChartDataByContractCode"
