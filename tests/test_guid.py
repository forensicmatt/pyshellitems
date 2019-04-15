import sys
sys.path.append("..")
import json
import unittest
from pyshellitems.guid import Guid


class TestGuids(unittest.TestCase):
    def test_guid(self):
        g1 = Guid.from_str(
            "{01a3057a-74d6-4e80-bea7-dc4c212ce50a}"
        )

        self.assertEqual(str(g1), "01a3057a-74d6-4e80-bea7-dc4c212ce50a")


if __name__ == '__main__':
    unittest.main()
