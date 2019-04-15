import struct
from pyshellitems.guid import Guid


class PropertyViewItem(object):
    def __init__(self, raw_buffer):
        self._buffer = raw_buffer
        self.size = struct.unpack("<H", self._buffer[0:2])[0]
        self.type = struct.unpack("<B", self._buffer[2:3])[0]
        self.unknown1 = struct.unpack("<B", self._buffer[3:4])[0]
        self.size2 = struct.unpack("<H", self._buffer[4:6])[0]
        self.signature = struct.unpack("<I", self._buffer[6:10])[0]
        self.property_store_size = struct.unpack("<H", self._buffer[10:12])[0]
        self.identifier_size = struct.unpack("<H", self._buffer[12:14])[0]

        self.property_store_list = None
        if self.property_store_size > 0:
            raise(Exception("Unhandled"))

        self.identifier_guid = None
        if self.identifier_size > 0:
            self.identifier_guid = Guid(self._buffer[14:30])

    def as_dict(self):
        property_list = self.property_store_list
        if property_list:
            property_list = property_list.as_dict()

        identifier_guid = None
        if self.identifier_guid:
            identifier_guid = str(self.identifier_guid)

        return {
            "type": "0x{:02X}".format(self.type),
            "unknown1": self.unknown1,
            "size2": self.size2,
            "signature": "{:04X}".format(self.signature),
            "property_store_size": self.property_store_size,
            "property_store": property_list,
            "identifier_guid": identifier_guid
        }
