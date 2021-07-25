import urllib.parse

from requests import Session

from easy_equities_client import constants
from easy_equities_client.accounts.clients import AccountsClient
from easy_equities_client.instruments.clients import InstrumentsClient
from easy_equities_client.types import Client


class PlatformClient(Client):
    """
    Generic client for https://platform.easyequities.io
    and https://platform.satrixnow.co.za.
    """

    def __init__(self, base_url, session: Session = None):
        super().__init__(base_url, session)
        self.accounts = AccountsClient(base_url, self.session)
        self.instruments = InstrumentsClient(base_url, self.session)

    def login(self, username: str, password: str) -> bool:
        """
        Login to the platform.

        :param username: Username.
        :param password: Password.

        :return: boolean True if successfully logged in.
        :raises Exception: if request failed.
        """
        password = urllib.parse.quote(password)
        username = urllib.parse.quote(username)

        data = (
            f"UserIdentifier={username}&Password={password}"
            "&ReturnUrl=&OneSignalGameId=&IsUsingNewLayoutSatrixOrEasyEquitiesMobileApp=False"
        )
        self.session.headers["Accept"] = (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,image/webp,*/*;q=0.8"
        )
        self.session.headers["Connection"] = "keep-alive"
        self.session.headers["Connection-Type"] = "application/x-www-form-urlencoded"
        self.session.headers["Content-Type"] = "application/x-www-form-urlencoded"

        response = self.session.post(
            self._url(constants.PLATFORM_SIGN_IN_PATH),
            data=data,
            allow_redirects=False,
        )
        response.raise_for_status()
        if response.status_code != 302:
            raise Exception("Login failed")

        return True


class EasyEquitiesClient(PlatformClient):
    """
    Client to interact with EasyEquities.
    """

    def __init__(self, base_url: str = constants.EASY_EQUITIES_BASE_PLATFORM_URL):
        return super().__init__(base_url)


class SatrixClient(PlatformClient):
    """
    Client to interact with Satrix.
    """

    def __init__(self, base_url: str = constants.SATRIX_BASE_PLATFORM_URL):
        return super().__init__(base_url)
