import json
import logging
from datetime import date, timedelta
from typing import Any, List, Optional

from bs4 import BeautifulSoup
from requests import Session

from easy_equities_client import constants
from easy_equities_client.accounts.parsers import (
    AccountHoldingsParser,
    AccountOverviewParser,
    get_transactions_from_page,
)
from easy_equities_client.accounts.types import Account, Holding, Transaction, Valuation
from easy_equities_client.types import Client

logger = logging.getLogger(__name__)


class AccountsClient(Client):
    def __init__(self, base_url: str = "", session: Session = None):
        super().__init__(base_url, session)
        self.current_account: Optional[str] = None

    def _get_account_overview_page(self) -> str:
        response = self.session.get(self._url(constants.PLATFORM_ACCOUNT_OVERVIEW_PATH))
        assert (
            response.status_code == 200
        ), "Account overview page should return 200 status code"
        assert "My Investments" in str(response.content)
        return str(response.content)

    def list(self) -> List[Account]:
        page = self._get_account_overview_page()
        parser = AccountOverviewParser(page)
        return parser.extract_accounts()

    def _switch_account(self, account_id: str) -> None:
        """
        Switch the currently selected account to account with ID account_id.
        """
        if self.current_account != account_id:
            data = {'trustAccountId': account_id}
            response = self.session.post(
                self._url(constants.PLATFORM_UPDATE_CURRENCY_PATH), data
            )
            response.raise_for_status()
            assert (
                response.status_code == 200
            ), "Update currency request should return 200 status code"
            self.current_account = account_id

    def valuations(self, account_id: str) -> Valuation:
        self._switch_account(account_id)
        response = self.session.get(
            self._url(constants.PLATFORM_ACCOUNT_VALUATIONS_PATH)
        )
        response.raise_for_status()
        return json.loads(response.json())

    def transactions(self, account_id: str) -> List[Transaction]:
        """
        Gets JSON-formatted transactions for the last year.
        """
        self._switch_account(account_id)
        response = self.session.get(self._url(constants.PLATFORM_TRANSACTIONS_PATH))
        response.raise_for_status()
        return response.json()

    def transactions_for_period(
        self, account_id: str, start_date: date, end_date: date
    ) -> List[Any]:
        """
        Gets transactions for a given period. Unfortunately not JSON-formatted
        and contains less useful data than the yearly data.

        :param account_id:
        :param start_date:
        :param end_date:
        """
        self._switch_account(account_id)
        transactions: List[Any] = []

        current_start = start_date
        current_end = min(end_date, current_start + timedelta(days=90))

        while current_start < end_date:
            print(f"Current start: {current_start}, Current end: {current_end}")
            transactions_for_date_range = []

            page_number = 1
            while True:
                next_url = self._url(
                    constants.PLATFORM_TRANSACTIONS_SEARCH_PATH_NEXT_PAGE.format(
                        start_date=f"{current_start.month}/{current_start.day}/{current_start.year}",
                        end_date=f"{current_end.month}/{current_end.day}/{current_end.year}",
                        page_number=page_number,
                    )
                )
                response = self.session.get(next_url)
                new_transactions = get_transactions_from_page(response.content)
                if len(new_transactions) == 0:
                    # No more transactions left
                    break
                transactions_for_date_range += new_transactions
                page_number += 1
            
            print(json.dumps(transactions_for_date_range, indent=4))
            transactions = transactions_for_date_range + transactions

            current_start = current_end + timedelta(days=1)
            current_end = min(end_date, current_start + timedelta(days=90))

        transactions.reverse()
        return transactions

    def holdings(self, account_id: str, include_shares: bool = False) -> List[Holding]:
        """
        Get an account's holdings/stocks.

        :param account_id: String account ID.
        :param include_shares: Whether to fetch the number of shares per holding. Create an extra
        HTTP request per holding.
        """
        self._switch_account(account_id)
        response = self.session.get(self._url(constants.PLATFORM_HOLDINGS_PATH))
        response.raise_for_status()
        parser = AccountHoldingsParser(response.content)
        holdings = parser.extract_holdings()
        if include_shares:
            for holding in holdings:
                response = self.session.get(self._url(holding['view_url']))
                soup = BeautifulSoup(response.content, "html.parser")
                whole_shares = soup.find(
                    lambda tag: '#Shares' in tag
                ).next_sibling.next_sibling.text.strip()
                partial_shares = soup.find(
                    lambda tag: '#FSR' in tag
                ).next_sibling.next_sibling.text.strip()
                holding['shares'] = f"{whole_shares}{partial_shares}"
        return holdings
