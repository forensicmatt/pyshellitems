import sys
sys.path.append("..")
import unittest
from pyshellitems.shellitems.shellitem import parse_shell_item


class TestShellItem_1F(unittest.TestCase):
    def test_1f_01(self):
        with open("../testdata/0x1F.ed9f55d3e9914a48b7927398142d220c.0.shellitem", "rb") as fh:
            raw_data = fh.read()
            si = parse_shell_item(
                raw_data
            )
            print(si.as_dict())

    def test_1f_02(self):
        with open("../testdata/0x1F.e8f0160f79e8455c8c4e796d257d8b02.0.shellitem", "rb") as fh:
            raw_data = fh.read()
            si = parse_shell_item(
                raw_data
            )
            print(si.as_dict())


class TestShellItem_00(unittest.TestCase):
    def test_app_shell_item(self):
        with open("../testdata/shellitem.0x00.appitem.raw", "rb") as fh:
            raw_data = fh.read()
            si = parse_shell_item(
                raw_data
            )
            print(si.as_dict())

    def test_23febbee_shell_item(self):
        with open("../testdata/shellitem.0x00.23febbee.raw", "rb") as fh:
            raw_data = fh.read()
            si = parse_shell_item(raw_data)
            print(si.as_dict())


if __name__ == '__main__':
    unittest.main()
