import sys
sys.path.append("..")
import unittest
from pyshellitems.propertystore.propertystore import PropertyStoreList


class TestPropertyStore(unittest.TestCase):
    def test_iterate_properties(self):
        with open("../testdata/shellitem.0x00.appitem.raw", "rb") as fh:
            fh.seek(22)
            raw_property_store_list = fh.read(1040)
            p_store = PropertyStoreList(
                raw_property_store_list
            )
            print(p_store.as_dict())


if __name__ == '__main__':
    unittest.main()
