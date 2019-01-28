from morningstar.models.ms_result import MSResult

class MSResponse():
    def __init__(self, errors: list, results: list) -> None:
        self.errors = errors
        self.results = results

    @staticmethod
    def from_dict(d: dict):
        quotes = d['quotes']
        errors = quotes.get('error', [])  # optional
        results = quotes['results']
        if results:
            results = [MSResult.from_dict(r) for r in results]
        return MSResponse(errors=errors, results=results)
