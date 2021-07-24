from requests import Session


class Client:
    def __init__(self, base_url: str = "", session: Session = None):
        self.base_url = base_url
        if session is None:
            self.session = Session()
        else:
            self.session = session

    def _url(self, path: str):
        return f"{self.base_url}{path}"
