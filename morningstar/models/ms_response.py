from morningstar.models.ms_result import MSResult


class MSResponse:
    def __init__(self, errors: list, results: list) -> None:
        self.errors = errors
        self.results = results

    @staticmethod
    def from_dict(d: dict):
        errors = d.get('error', [])
        results = d.get('results', [])
        if results:
            results = [MSResult.from_dict(r) for r in results]
        return MSResponse(errors=errors, results=results)
