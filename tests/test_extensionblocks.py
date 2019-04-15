import sys
sys.path.append("..")
import json
import unittest
from pyshellitems.extensionblocks import extensionblock


BEEF0x26 =  b"\x26\x00\x01\x00\x26\x00\xEF\xBE\x10\x00\x00\x00\xB5\xBA\x02\x82"\
            b"\x1E\x1A\xD4\x01\xA5\x8E\xFD\x03\xCC\x1A\xD4\x01\x78\xEE\xCC\x53"\
            b"\x07\x1B\xD4\x01\x14\x00"


class Test1F(unittest.TestCase):
    def test_beef26(self):
        eb = extensionblock.parse_extension_block(
            BEEF0x26
        )
        print(json.dumps(eb.as_dict()))


if __name__ == '__main__':
    unittest.main()
