import requests
import logging

from morningstar.models.ms_response import MSResponse
from morningstar.models.ts_response import TSResponse
from morningstar.provider.provider import Provider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Morningstar(Provider):
    """Morningstar API

    Note:
        This class combines multiple endpoints:
            - http://msuxml.morningstar.com/IndexTS
            - http://msxml.tenfore.com/search
            - http://msxml.tenfore.com/index.php

    Attributes:
        credentials (dict): Provider specific configuration including "username" and "password"
    """

    def __init__(self, config):
        super().__init__(config)

    def _build_url(self, base: str, params: dict):
        url_params = ''.join(['&{}={}'.format(k, v) for k, v in params.items()])
        url = base + \
              '?username={}&password={}'.format(self.config['username'], self.config['password']) + \
              url_params + \
              '&json'
        return url

    def _request(self, base: str, params: dict):
        response = requests.get(self._build_url(base=base, params=params))
        return response.json()

    def _tenfore(self, endpoint: str, params: dict):
        base = 'http://msxml.tenfore.com/{}'.format(endpoint)
        return self._request(base=base, params=params)

    def _morningstar(self, endpoint: str, params: dict):
        base = 'http://msuxml.morningstar.com/{}'.format(endpoint)
        return self._request(base=base, params=params)

    def search(self, params):
        response = self._tenfore('search', params)
        return MSResponse.from_dict(response)

    def index(self, params):
        response = self._tenfore('index.php', params)
        return MSResponse.from_dict(response)

    def index_ts(self, params):
        response = self._morningstar('IndexTS', params)
        return TSResponse.from_dict(response)

