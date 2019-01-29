import datetime
import logging
import unittest

import yaml

from morningstar.models.instrument import Instrument
from morningstar.morningstar_client import MorningstarClient
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


class MorningstarClientTest(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.client = MorningstarClient(Morningstar(config=CONFIG))
        if CONFIG_LIVE is not None:
            self.client_live = MorningstarClient(Morningstar(config=CONFIG_LIVE))

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration missing")
    def test_get_traded_currencies(self):
        currencies = self.client_live.get_traded_currencies(instrument="182.1.NESN")
        self.assertEqual(["CHF"], currencies)

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration missing")
    def test_get_prices_by_most_available(self):
        instrument, prices = self.client_live.get_prices_by_most_available(
            isin="CH0038863350",
            currency="CHF",
            start_date="01-01-2019",
            end_date="03-01-2019"
        )
        self.assertEqual(Instrument.from_string("182.1.NESN"), instrument)

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration missing")
    def test_find_instruments_by_isin_and_currency(self):
        instruments = self.client_live.find_instruments_by_isin_and_currency(isin="CH0038863350", currency="CHF")
        self.assertTrue(Instrument.from_string("182.1.NESN") in instruments)

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration missing")
    def test_get_instrument_prices(self):
        prices = self.client_live.get_instrument_prices(
            instrument="182.1.NESN",
            start_date="03-01-2019",
            end_date="04-01-2019"
        )
        self.assertEqual(
            [
                datetime.datetime(2019, 1, 4, 0, 0),
                datetime.datetime(2019, 1, 3, 0, 0)
            ],
            list(prices.keys())
        )

    @unittest.skipIf(CONFIG_LIVE is None, "Live configuration missing")
    def test_get_fx_prices(self):
        prices = self.client_live.get_fx_prices(
            base_currency="USD",
            counter_currency="CHF",
            start_date="01-01-2019",
            end_date="03-01-2019"
        )
        self.assertEqual(
            [
                datetime.datetime(2019, 1, 3, 0, 0),
                datetime.datetime(2019, 1, 2, 0, 0),
                datetime.datetime(2019, 1, 1, 0, 0)
            ],
            list(prices.keys())
        )