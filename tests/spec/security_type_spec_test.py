import unittest

from morningstar.spec.security_type_spec import SecurityTypeSpec


class SecurityTypeSpecTest(unittest.TestCase):

    def test_get_value(self):
        self.assertEqual("Stocks", SecurityTypeSpec.get_value(2))

    def test_get_value_none(self):
        self.assertIsNone(SecurityTypeSpec.get_value(200))
