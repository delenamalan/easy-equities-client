from easy_equities_client import constants


class TestPlatformClient:
    def test_login(
        self, platform_client, base_platform_url, mock_success_login_response
    ):
        mock_success_login_response(base_platform_url)
        assert platform_client.login('username', 'password') is True


class TestEasyEquitiesClient:
    def test_login(self, easy_equities_client, mock_success_login_response):
        mock_success_login_response(constants.EASY_EQUITIES_BASE_PLATFORM_URL)
        assert easy_equities_client.login('username', 'password') is True


class TestSatrixClient:
    def test_login(self, satrix_client, mock_success_login_response):
        mock_success_login_response(constants.SATRIX_BASE_PLATFORM_URL)
        assert satrix_client.login('username', 'password') is True
