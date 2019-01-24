from morningstar.models.instrument import Instrument


class MSResult:
    def __init__(self, data) -> None:
        self.data = data

    @staticmethod
    def from_dict(d: dict):
        return MSResult(data=d)

    def has_instrument(self):
        return self.get_instrument() is not None

    def get_instrument(self):
        try:
            instrument = Instrument.from_dict(self.data)
        except KeyError:
            instrument = None
        return instrument
