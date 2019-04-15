import struct
import pyshellitems.guid as guid
from pyshellitems.extensionblocks.extensionblock import parse_extension_block


class ShellItem1F(object):
    def __init__(self, raw_buffer):
        self._buffer = raw_buffer
        self.size = struct.unpack("<H", self._buffer[0:2])[0]
        self.type = struct.unpack("<B", self._buffer[2:3])[0]
        self.unknown1 = struct.unpack("<B", self._buffer[3:4])[0]
        self.extension_block = None

        if self.size == 0x14:
            self.guid = guid.Guid(
                self._buffer[4:20]
            )
        elif self.size == 50 or self.size == 58:
            self.guid = guid.Guid(
                self._buffer[4:20]
            )

            if self.size > 20:
                self.extension_block = parse_extension_block(
                    self._buffer[20:]
                )
        else:
            raise(Exception("Unhandled: {}".format(
                self._buffer.hex()
            )))



    def as_dict(self):
        extension_block_dict = self.extension_block
        if extension_block_dict:
            extension_block_dict = self.extension_block.as_dict()

        return {
            "type": "0x{:02X}".format(self.type),
            "unknown1": "0x{:02X}".format(self.unknown1),
            "guid": str(self.guid),
            "extension": extension_block_dict
        }
