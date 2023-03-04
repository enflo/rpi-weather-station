import requests
from src.settings import API_HOST, API_HEADER_TOKEN, API_URL_TOKEN, API_METHOD


class SendDataAPI:
    def __init__(self, data):
        self.data = data

    def send(self):
        self._make_request()

    def _make_request(self):
        requests.request(
            method=API_METHOD,
            url=self._get_url(),
            headers=self._get_headers(),
            json=self.data,
        )

    @staticmethod
    def _get_headers():
        headers = {
            "Content-Type": "application/json",
        }
        if API_HEADER_TOKEN:
            headers.update(API_HEADER_TOKEN)

        return headers

    @staticmethod
    def _get_url():
        return f"{API_HOST}{API_URL_TOKEN}"
