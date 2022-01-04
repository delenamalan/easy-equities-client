# Easy Equities and Satrix Python Client

Unofficial Python client for [Easy Equities](easyequities.io/) and 
[Satrix](satrix.co.za/). **Intended for personal use.**

Supports Python 3.6+.

[Pypi](https://pypi.org/project/easy-equities-client/)


## Installation

```
pip install easy-equities-client
```

## Features

Accounts:
- Get accounts for a user: `client.accounts.list()`
- Get account holdings: `client.accounts.holdings(account.id)`
- Get account valuations: `client.accounts.valuations(account.id)`
- Get account transactions: `client.accounts.transactions(account.id)`

Instruments:
- Get the historical prices for an instrument: 
  `client.instruments.historical_prices('EQU.ZA.SYGJP', Period.ONE_MONTH)`

## Usage

```python
from easy_equities_client.clients import EasyEquitiesClient # or SatrixClient

client = EasyEquitiesClient()
client.login(username='your username', password='your password')

# List accounts
accounts = client.accounts.list()
"""
[
    Account(id='12345', name='EasyEquities ZAR', trading_currency_id='2'),
    Account(id='12346', name='TFSA', trading_currency_id='3'),
    ...
]
"""

# Get account holdings
holdings = client.accounts.holdings(accounts[0].id)
"""
[
    {
        "name": "CoreShares Global DivTrax ETF",
        "contract_code": "EQU.ZA.GLODIV",
        "purchase_value": "R2 000.00",
        "current_value": "R3 000.00",
        "current_price": "R15.50",
        "img": "https://resources.easyequities.co.za/logos/EQU.ZA.GLODIV.png",
        "view_url": "/AccountOverview/GetInstrumentDetailAction/?IsinCode=ZAE000254249",
        "isin": "ZAE000254249"
    },
    ...
]
"""
# Optionally include number of shares for each holding (creates another API call for each holding)
holdings = client.accounts.holdings(accounts[0].id, include_shares=True)
"""
[
    {
        "name": "CoreShares Global DivTrax ETF",
        "contract_code": "EQU.ZA.GLODIV",
        "purchase_value": "R2 000.00",
        "current_value": "R3 000.00",
        "current_price": "R15.50",
        "img": "https://resources.easyequities.co.za/logos/EQU.ZA.GLODIV.png",
        "view_url": "/AccountOverview/GetInstrumentDetailAction/?IsinCode=ZAE000254249",
        "isin": "ZAE000254249",
        "shares": "200.123"
    },
    ...
]
"""

# Get account valuations
valuations = client.accounts.valuations(accounts[0].id)
"""
{
    "TopSummary": {
        "AccountValue": 300000.50,
        "AccountCurrency": "ZAR",
        "AccountNumber": "EE123456-111111",
        "AccountName": "EasyEquities ZAR",
        "PeriodMovements": [
            {
                "ValueMoveLabel": "Profit & Loss Value",
                "ValueMove": "R5 000.00",
                "PercentageMoveLabel": "Profit & Loss",
                "PercentageMove": "15.00%",
                "PeriodMoveHeader": "Movement on Current Holdings:"
            }
        ]
    },
    "NetInterestOnCashItems": [
        {
            "Label": "Total Interest on Free Cash",
            "Value": "R10.55"
        },
        ...
    ],
    "AccrualSummaryItems": [
        {
            "Label": "Net Accrual",
            "Value": "R2.00"
        },
        ...
    ],
    ...
}
"""

# Get account transactions
transactions = client.accounts.transactions(accounts[0].id)
"""
[
    {
        "TransactionId": 0,
        "DebitCredit": 200.00,
        "Comment": "Account Balance Carried Forward",
        "TransactionDate": "2020-07-21T01:00:00",
        "LogId": 123456789,
        "ActionId": 0,
        "Action": "Account Balance Carried Forward",
        "ContractCode": ""
    },
        {
        "TransactionId": 0,
        "DebitCredit": 50.00,
        "Comment": "CoreShares Global DivTrax ETF-Foreign Dividends @15.00",
        "TransactionDate": "2020-11-19T14:30:00",
        "LogId": 123456790,
        "ActionId": 122,
        "Action": "Foreign Dividend",
        "ContractCode": "EQU.ZA.GLODIV"
    },
    ...
]
"""

# Get historical data for an equity/instrument
from easy_equities_client.instruments.types import Period
historical_prices = client.instruments.historical_prices('EQU.ZA.SYGJP', Period.ONE_MONTH)
"""
{
    "chartData": {
        "Dataset": [
            41.97,
            42.37,
            ...
        ],
        "Labels": [
            "25 Jun 21",
            "28 Jun 21",
            ...
        ],
        "TradingCurrencySymbol": "R",
        ...
    }
}
"""
```

## Example Use Cases

### Show holdings total profits/losses

Run a script to show your holdings and their total profits/losses, e.g.  
[show_holdings_profit_loss.py](https://github.com/delenamalan/easy-equities-client/blob/master/examples/show_holdings_profit_loss.py).

![show_holdings_profit_loss.py example output](https://raw.githubusercontent.com/delenamalan/easy-equities-client/master/examples/show_holdings_profit_loss_example.png)



## Contributing

See [Contributing](./CONTRIBUTING.md)
