from morningstar.models.instrument import Instrument


class TSResult:
    def __init__(self, instrument: Instrument, data: dict) -> None:
        self.data = data
        self.instrument = instrument

    @staticmethod
    def from_json(json_obj):
        return TSResult(
            instrument=Instrument(
                exchange=json_obj['exchangeid'],
                security_type=json_obj['type'],
                symbol=json_obj['symbol']
            ),
            data=json_obj['data']
        )