import unittest
import yaml
import logging

from morningstar.provider.morningstar import Morningstar

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONFIG_PATH = 'config-morningstar.yml.dist'
CONFIG = yaml.safe_load(open(CONFIG_PATH))['provider']['morningstar']
CONFIG_LIVE = None
try:
    from morningstar.config import config
    CONFIG_LIVE = config.get("provider")['morningstar']
except:
    logger.info("Skipping live tests.")
    pass


class MorningstarTest(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.provider = Morningstar(config=CONFIG)
        if CONFIG_LIVE is not None:
            self.provider_live = Morningstar(config=CONFIG_LIVE)

    def test_build_url(self):
        self.assertEqual(
            'endpoint?username=foo&password=bar&json',
            self.provider._build_url(base="endpoint", params={})
        )

    def test_build_url_params(self):
        self.assertEqual(
            'endpoint?username=foo&password=bar&isin=CH0038863350&json',
            self.provider._build_url(base="endpoint", params={'isin': 'CH0038863350'})
        )

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration missing")
    def test_search(self):
        r = self.provider_live.search({'isin': 'CH0038863350'})
        self.assertEqual([], r.errors)
        self.assertEqual(True, r.results[0].has_instrument())

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration required")
    def test_search_invalid(self):
        r = self.provider_live.search({'invalid_field': 'CH0038863350'})
        self.assertEqual(['Invalid request'], r.errors)

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration required")
    def test_search_empty(self):
        r = self.provider_live.search({'isin': 'nonexistent'})
        self.assertEqual([], r.errors)
        self.assertEqual([], r.results)

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration required")
    def test_index(self):
        r = self.provider_live.index({'instrument': '50.1.MSFT', 'fields': 'S9,D204'})
        self.assertEqual(
            {'Listed Currency': 'USD', 'Traded Currency': 'MXN'},
            r.results[0].data
        )

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration required")
    def test_index_invalid(self):
        r = self.provider_live.index({'instrument': '0.0.NONEXISTENT', 'fields': 'S9,D204'})
        self.assertEqual(['Invalid Instrument=0.0.NONEXISTENT'], r.errors)
        self.assertEqual([], r.results)

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration required")
    def test_indexts(self):
        r = self.provider_live.index_ts(
            {'instrument': '28.10.F00000JQA9', 'sdate': '01-01-2019', 'edate': '10-01-2019', 'type': 'dailybar'})
        self.assertEqual([], r.errors)
        self.assertEqual(7, len(r.results[0].data))

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration required")
    def test_indexts_no_data(self):
        r = self.provider_live.index_ts(
            {'instrument': '28.10.F00000JQA9', 'sdate': '01-01-2019', 'edate': '01-01-2019', 'type': 'dailybar'})
        self.assertEqual(['No Data'], r.errors)
        self.assertEqual(1, len(r.results))  # instrument is correct
        self.assertEqual(0, len(r.results.data))  # but doesnt contain data

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration required")
    def test_indexts_no_data(self):
        r = self.provider_live.index_ts(
            {'instrument': '0.0.NONEXISTENT', 'sdate': '01-01-2019', 'edate': '01-01-2019', 'type': 'dailybar'})
        self.assertEqual(['Invalid Instrument=0.0.NONEXISTENT', 'Invalid request'], r.errors)
        self.assertEqual([], r.results)
