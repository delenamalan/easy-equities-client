import json
import logging
from datetime import date
from typing import Any, List

from bs4 import BeautifulSoup

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
        Switch the currently selected account.
        """
        data = {'trustAccountId': account_id}
        response = self.session.post(
            self._url(constants.PLATFORM_UPDATE_CURRENCY_PATH), data
        )
        response.raise_for_status()
        assert (
            response.status_code == 200
        ), "Update currency request should return 200 status code"

    def valuations(self, account_id: str) -> Valuation:
        self._switch_account(account_id)
        response = self.session.get(
            self._url(constants.PLATFORM_ACCOUNT_VALUATIONS_PATH)
        )
        response.raise_for_status()
        return json.loads(response.json())

    def transactions(self, account_id: str) -> List[Transaction]:
        logger.warning(
            "AccountsClient.transactions is deprecated. Use AccountsClient.transactions_last_year or AccountsClient.transactions_for_period instead"
        )
        return self.transactions_last_year(account_id)

    def transactions_last_year(self, account_id: str) -> List[Transaction]:
        """
        Gets the last year's transactions.
        """
        self._switch_account(account_id)
        response = self.session.get(self._url(constants.PLATFORM_TRANSACTIONS_PATH))
        response.raise_for_status()
        return response.json()

    def transactions_for_period(
        self, account_id: str, start_date: date, end_date: date
    ) -> List[Any]:
        """
        Gets transactions for a given period (max. 3 months).

        :param account_id:
        :param start_date:
        :param end_date:
        """
        # TODO: check if more than 93 days
        # TODO: loop through to get by max 93-day periods

        self._switch_account(account_id)
        page_number = 1
        transactions: List[Any] = []
        while True:
            next_url = self._url(
                constants.PLATFORM_TRANSACTIONS_SEARCH_PATH_NEXT_PAGE.format(
                    start_date=f"{start_date.month}/{start_date.day}/{start_date.year}",
                    end_date=f"{end_date.month}/{end_date.day}/{end_date.year}",
                    page_number=page_number,
                )
            )
            response = self.session.get(next_url)
            new_transactions = get_transactions_from_page(response.content)
            if len(new_transactions) == 0:
                # No more transactions left
                break
            transactions += new_transactions
            page_number += 1
        return transactions

    def holdings(self, account_id: str, include_shares: bool = False) -> List[Holding]:
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
