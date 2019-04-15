import struct
from pyshellitems.guid import Guid
from pyshellitems.propertystore.propertystore import PropertyStoreList
from pyshellitems.extensionblocks.extensionblock import parse_extension_block

# https://github.com/libyal/libfwsi/blob/master/documentation/Windows%20Shell%20Item%20format.asciidoc#472-users-property-view-delegate-item
# https://docs.microsoft.com/en-us/windows/desktop/stg/the-documentsummaryinformation-and-userdefined-property-sets


class PropertyViewDelegateItem(object):
    def __init__(self, raw_buffer):
        self._buffer = raw_buffer
        self.size = struct.unpack("<H", self._buffer[0:2])[0]
        self.type = struct.unpack("<B", self._buffer[2:3])[0]
        self.unknown1 = struct.unpack("<B", self._buffer[3:4])[0]
        self.data_size = struct.unpack("<H", self._buffer[4:6])[0]
        self.signature = struct.unpack("<I", self._buffer[6:10])[0] # 0x23a3dfd5
        self.property_store_size = struct.unpack("<H", self._buffer[10:12])[0]
        self.identifier_size = struct.unpack("<H", self._buffer[12:14])[0]

        ptr = 14
        self.identifier_data = None
        if self.identifier_size > 0:
            self.identifier_data = self._buffer[ptr:ptr+self.identifier_size]
            ptr += self.identifier_size

        self.property_store = None
        if self.property_store_size > 0:
            self.property_store = PropertyStoreList(
                self._buffer[ptr:ptr+self.property_store_size]
            )
            ptr += self.property_store_size

        self.unknown2 = struct.unpack("<H", self._buffer[ptr:ptr + 2])[0]
        ptr += 2

        self.delegate_guid = Guid(self._buffer[ptr:ptr + 16])
        ptr += 16

        self.item_guid = Guid(self._buffer[ptr:ptr + 16])
        ptr += 16

        self.extension_blocks = []
        while True:
            extension_block = parse_extension_block(
                self._buffer[ptr:]
            )
            self.extension_blocks.append(
                extension_block
            )
            ptr += extension_block.size

            if ptr >= self.size:
                break

    def as_dict(self):
        extension_block_list = []
        for block in self.extension_blocks:
            extension_block_list.append(block.as_dict())

        prop_store_dict = self.property_store
        if prop_store_dict:
            prop_store_dict = prop_store_dict.as_dict()

        return {
            "type": "0x{:02X}".format(self.type),
            "unknown1": self.unknown1,
            "size2": self.data_size,
            "signature": "{:04X}".format(self.signature),
            "identifier_data": self.identifier_data.hex(),
            "delegate_guid": str(self.delegate_guid),
            "item_guid": str(self.item_guid),
            "prop_store": prop_store_dict,
            "extension_block_list": extension_block_list
        }
