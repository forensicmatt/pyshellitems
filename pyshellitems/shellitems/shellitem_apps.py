import struct
from pyshellitems.propertystore.propertystore import PropertyStoreList


class ApplicationShellItem(object):
    def __init__(self, raw_buffer):
        self._buffer = raw_buffer
        self.size = struct.unpack("<H", self._buffer[0:2])[0]
        self.type = struct.unpack("<B", self._buffer[2:3])[0]
        self.unknown1 = struct.unpack("<B", self._buffer[3:4])[0]
        self.size2 = struct.unpack("<H", self._buffer[4:6])[0]
        self.signature = self._buffer[6:10]
        self.property_store_size = struct.unpack("<H", self._buffer[10:12])[0]
        self.unknown2 = struct.unpack("<H", self._buffer[12:14])[0]
        self.unknown5 = struct.unpack("<H", self._buffer[14:16])[0]

    def get_property_store_list(self):
        return PropertyStoreList(
            self._buffer[22:22+self.property_store_size]
        )

    def as_dict(self):
        property_list = self.get_property_store_list()
        if property_list:
            property_list = property_list.as_dict()

        return {
            "type": "0x{:02X}".format(self.type),
            "unknown1": self.unknown1,
            "size2": self.size2,
            "signature": self.signature.decode("ascii", errors="replace"),
            "property_store_size": self.property_store_size,
            "property_store": property_list
        }
