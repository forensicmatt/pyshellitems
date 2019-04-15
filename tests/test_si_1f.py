import sys
sys.path.append("..")
import json
import unittest
import pyshellitems.shellitems.shellitem_x1f as shellitem_x1f

ITEM_01 = b"\x14\x00\x1F\x50\xE0\x4F\xD0\x20\xEA\x3A\x69\x10\xA2\xD8\x08\x00"\
          b"\x2B\x30\x30\x9D"

ITEM_02 = b"\x3A\x00\x1F\x44\x47\x1A\x03\x59\x72\x3F\xA7\x44\x89\xC5\x55\x95"\
          b"\xFE\x6B\x30\xEE\x26\x00\x01\x00\x26\x00\xEF\xBE\x10\x00\x00\x00"\
          b"\xB5\xBA\x02\x82\x1E\x1A\xD4\x01\xA5\x8E\xFD\x03\xCC\x1A\xD4\x01"\
          b"\x78\xEE\xCC\x53\x07\x1B\xD4\x01\x14\x00"


class Test1F(unittest.TestCase):
    def test_1f_01(self):
        si = shellitem_x1f.ShellItem1F(ITEM_01)
        print(json.dumps(si.as_dict()))

    def test_1f_02(self):
        si = shellitem_x1f.ShellItem1F(ITEM_02)
        print(json.dumps(si.as_dict()))


if __name__ == '__main__':
    unittest.main()
