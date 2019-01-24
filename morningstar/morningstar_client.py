import logging
from datetime import datetime

from morningstar.config import config
from morningstar.models.instrument import Instrument
from morningstar.provider.morningstar import Morningstar
from morningstar.spec.web_service_spec import FieldNames, FieldCode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MorningstarClient():

    def __init__(self, provider=None):
        """ Wraps Provider

        Args:
            provider (Provider): provider instance
        """
        if provider is None:
            provider = Morningstar(config=config.get("provider")['morningstar'])
        self.provider = provider

    def get_instrument_price_info(self, instrument: str, start_date: str, end_date: str, bar_type='dailybar'):
        return self.provider.index_ts({
            'pricechangeadjusted&instrument': instrument,
            'sdate': start_date,
            'edate': end_date,
            'type': bar_type
        })

    def get_instrument_prices(self, instrument: str, start_date: str, end_date: str, bar_type='dailybar'):
        """Fetches prices for a specific instrument

        Args:
            instrument (str): e.g. "126.1.AMZN"
            start_date (str): "%d-%m-%Y"
            end_date (str): "%d-%m-%Y"

        Returns:
            Dict of timestamps and prices for given asset.
            {
                datetime(2018, 10, 1, 0, 0) : 329.98,
                ...
            }
        """
        hist_prices = self.get_instrument_price_info(
            instrument=instrument,
            start_date=start_date,
            end_date=end_date,
            bar_type=bar_type
        )
        historical_price_dict = {}
        for obs in hist_prices:
            timestamp = datetime.strptime(obs['Date Received (GMT)'], '%d-%m-%Y')
            price = float(obs['Last price'])
            historical_price_dict[timestamp] = price
        return historical_price_dict

    def get_fx_prices(self, base_currency, counter_currency, start_date, end_date, bar_type='dailybar'):
        """Fetches FX prices for a currency pair (BASE/COUNTER)

        Args:
            base_currency (str): e.g. "USD"
            counter_currency (str): CHF
            start_date (str): "%d-%m-%Y"
            end_date (str): "%d-%m-%Y"

        Returns:
            Dict of timestamps and prices FX rates, e.g. 1 BASE = x COUNTER.
            {
                datetime(2018, 10, 1, 0, 0) : 0.98377,
                ...
            }
        """
        if base_currency == counter_currency:
            raise ValueError("Base- and counter currency must be different.")
        instrument = Instrument(
            exchange='245',
            security_type='20',
            symbol='{}{}LITE'.format(base_currency, counter_currency)
        )
        return self.get_instrument_prices(
            instrument=instrument.__str__(),
            start_date=start_date,
            end_date=end_date,
            bar_type=bar_type
        )

    def get_traded_currencies(self, instrument: str):
        """Finds all traded/listed currencies for a specific instrument

        Args:
            instrument (str): e.g. "126.1.AMZN"

        Returns:
            List of currencies, e.g. ["CHF", "USD"]
        """
        results = self.provider.index({
            'instrument': instrument,
            'fields': '{},D204'.format(FieldCode.ListedCurrency.value)
        })
        if not results:
            return []

        traded_currency_field = 'Traded Currency'
        traded_currencies = [x[traded_currency_field] for x in results if traded_currency_field in x]
        if traded_currencies:
            return traded_currencies
        logger.info(
            'No traded currency found for instrument {}, attempt use listed currency instead'.format(instrument))
        listed_currencies = [x[FieldNames.ListedCurrency.value] for x in results if
                             FieldNames.ListedCurrency.value in x]
        if listed_currencies:
            return listed_currencies
        logger.info('No listed currency found for instrument {}'.format(instrument))
        return []

    def get_prices_by_most_available(self, isin, currency, start_date, end_date, bar_type='dailybar'):
        """Fetches prices for a specific asset from the exchange which provides most results

        Note:
            A search using the ISIN is being executed after which prices are fetched from all returned exchanges which
            list the security.

        Args:
            isin (str): e.g. "US46625H1005"
            currency (str): e.g. "USD"
            start_date (str): "%d-%m-%Y"
            end_date (str): "%d-%m-%Y"

        Returns:
            Tuple of instrument and a dict of prices for given asset.

            exchange.security_type.symbol,
            {
                datetime(2018, 10, 1, 0, 0) : 0.98377,
                ...
            }
        """
        search_response = self.provider.search({'isin': isin})
        logger.info('Found {} search results for ISIN {}'.format(len(search_response), isin))
        max_nr_of_obs = 0
        max_prices = {}
        max_instrument = None
        for search_result in search_response:
            if search_result[FieldNames.SecurityType.value]:
                instrument = Instrument(
                    exchange=search_result['Exchange'],
                    security_type=search_result['Security Type'],
                    symbol=search_result['Symbol']
                )
                traded_currencies = self.get_traded_currencies(instrument.__str__())
                if currency not in traded_currencies:
                    logger.info('Skip exchange {} as desired asset currency {} is neither traded nor listed'
                                .format(search_result['Exchange'], currency))
                    continue

                hist_prices = self.get_instrument_prices(
                    instrument=instrument.__str__(),
                    start_date=start_date,
                    end_date=end_date,
                    bar_type=bar_type
                )
                if hist_prices:
                    nr_of_prices = len(hist_prices)
                    if nr_of_prices > max_nr_of_obs:
                        max_nr_of_obs = nr_of_prices
                        max_prices = hist_prices
                        max_instrument = instrument
                else:
                    nr_of_prices = 0

                logger.info('Collected {} historical prices for ISIN {} (instrument: {})'
                            .format(nr_of_prices, isin, instrument))
        return max_instrument, max_prices
