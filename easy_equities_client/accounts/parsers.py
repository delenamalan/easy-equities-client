import re
from dataclasses import dataclass
from typing import Any, List, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from easy_equities_client import constants
from easy_equities_client.accounts.types import Account, Holding


def extract_account_info(account_div: Tag) -> Optional[Account]:
    trading_currency = account_div.parent.attrs.get("data-tradingcurrencyid")
    if not trading_currency:
        return None
    return Account(
        name=account_div.text.strip(),
        trading_currency_id=trading_currency.strip(),
        id=account_div.parent.attrs["data-id"].strip(),
    )


@dataclass
class AccountOverviewParser:
    """
    Parse the accounts overview page (/AccountOverview) given the html
    contents of the page.
    """

    page: str

    def extract_accounts(self) -> List[Account]:
        """
        Return the accounts found on the account overview page.
        """
        soup = BeautifulSoup(self.page, "html.parser")
        accounts_divs = soup.find_all(attrs={"id": "trust-account-types"})
        return [
            account
            for account in [
                extract_account_info(account_div) for account_div in accounts_divs
            ]
            if account
        ]


class HoldingFieldNotFoundException(Exception):
    def __init__(self, field, exception):
        return super().__init__(
            f"Field '{field}' not found in holding div. Exception: f{exception}"
        )


class HoldingDivParser:
    def __init__(self, div: Tag):
        self.div = div

    def __eq__(a, b):
        return a.name == b.name

    def __hash__(self):
        return hash(self.name)

    @property
    def name(self) -> str:
        return self.div.find(attrs={'class': 'equity-image-as-text'}).text.strip()

    @property
    def purchase_value(self) -> str:
        return self.div.find(attrs={'class': 'purchase-value-cell'}).text.strip()

    @property
    def current_value(self) -> str:
        return self.div.find(attrs={'class': 'current-value-cell'}).text.strip()

    @property
    def current_price(self) -> str:
        return self.div.find(attrs={'class': 'current-price-cell'}).text.strip()

    @property
    def img(self) -> str:
        return self.div.find(attrs={'class': 'instrument'}).attrs['src']

    @property
    def contract_code(self) -> str:
        return self.img[self.img.rindex('/') + 1 : self.img.index('.png')]

    @property
    def view_url(self) -> str:
        return (
            self.div.find(attrs={'class': 'collapse-container'})
            .find('span')
            .attrs['data-detailviewurl']
        )

    @property
    def isin(self) -> str:
        return (
            self.div.find(attrs={'class': 'collapse-container'})
            .find('span')
            .attrs['data-detailviewurl']
            .split('=')[-1]
        )

    def to_dict(self) -> Holding:
        fields = [
            'name',
            'contract_code',
            'purchase_value',
            'current_value',
            'current_price',
            'img',
            'view_url',
            'isin',
        ]
        data: Holding = {}
        for field in fields:
            try:
                data[field] = getattr(self, field)  # type: ignore
            except Exception as e:
                raise HoldingFieldNotFoundException(field, e)

        return data


@dataclass
class AccountHoldingsParser:
    """
    Parse the accounts holdings page given the html contents of the page.
    """

    page: bytes

    def extract_holdings(self) -> List[Holding]:
        """
        Return the holdings found on the holdings page.
        """
        soup = BeautifulSoup(self.page, "html.parser")
        holdings_divs = soup.find_all(attrs={'class': 'holding-inner-container'})
        # Get unique holdings (skip first row because it is the header row)
        divs = set([HoldingDivParser(holding_div) for holding_div in holdings_divs[1:]])
        return [div.to_dict() for div in divs]


def get_transactions_from_page(page_body: bytes) -> List[Any]:
    """
    :param page_body: Page html from response.content.
    """
    soup = BeautifulSoup(page_body, "html.parser")
    table = soup.find("div", {"id": "TransactionHistory"}).find("tbody")
    if table is None:
        validation_error = soup.find(class_='validation-summary-errors')
        if validation_error:
            raise Exception(validation_error.text.strip())
        return []
    rows = table.find_all("tr")
    transactions = []
    for row in rows:
        columns = row.find_all("td")
        amount_pattern = re.compile(constants.RE_AMOUNT_PATTERN)
        amount_match = amount_pattern.match(columns[2].text.strip())
        if amount_match is None:
            raise Exception(
                f"Could not parse amount {columns[2].text.strip()} into currency and value."
            )
        transactions.append(
            {
                'date': columns[0].text.strip(),
                'description': columns[1].text.strip(),
                'currency': amount_match.group('currency'),
                'value': float(
                    (
                        amount_match.group('symbol')
                        if amount_match.group('symbol')
                        else ''
                    )
                    + amount_match.group('value').replace(" ", "")
                ),
                'amount': columns[2].text.strip(),
            }
        )
    return transactions
