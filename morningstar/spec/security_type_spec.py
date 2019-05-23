from typing import Optional

security_types = {
    1: "Not used",
    2: "Stocks",
    3: "Stock and index options",
    4: "Future options",
    5: "Spots",
    6: "Not used",
    7: "Corporate bonds",
    8: "Mutual funds / ETFs",
    9: "Government bonds",
    10: "Indices",
    11: "Municipal bonds",
    12: "Not used",
    13: "Spread instruments",
    14: "Statistic symbols",
    15: "Monetary funds",
    16: "Unspecified bonds",
    17: "Certificates",
    18: "Warrants",
    19: "Money market symbols",
    20: "Forex symbols",
}


class SecurityTypeSpec:
    """ Morningstar Security Types

    Morningstar_Exchange_and_Field_Codes_v4.28.pdf - Page 25
    """

    @staticmethod
    def get_value(security_type: int) -> Optional[str]:
        return security_types.get(security_type, None)
