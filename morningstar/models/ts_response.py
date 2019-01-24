from morningstar.models.ts_result import TSResult


class TSResponse:
    def __init__(self, errors: list, results: list) -> None:
        self.errors = errors
        self.results = results

    @staticmethod
    def from_json(json_obj):
        errors = json_obj.get('error', [])
        results = json_obj.get('results', [])
        if results:
            results = [TSResult.from_json(r) for r in results]
        return TSResponse(errors=errors, results=results)
