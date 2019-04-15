import struct
from pyshellitems.extensionblocks.beef0004 import Beef0004
from pyshellitems.extensionblocks.beef0019 import Beef0019
from pyshellitems.extensionblocks.beef0026 import Beef0026
from pyshellitems.extensionblocks.beef0025 import Beef0025


def parse_extension_block(raw_buffer):
    size = struct.unpack("<H", raw_buffer[0:2])[0]
    signature = struct.unpack("<I", raw_buffer[4:8])[0]

    if signature == 0xbeef0004:
        return Beef0004(
            raw_buffer[:size]
        )
    elif signature == 0xbeef0019:
        return Beef0019(
            raw_buffer[:size]
        )
    elif signature == 0xbeef0025:
        return Beef0025(
            raw_buffer[:size]
        )
    elif signature == 0xbeef0026:
        return Beef0026(
            raw_buffer[:size]
        )
    else:
        return ExtensionBlock(
            raw_buffer[:size]
        )


class ExtensionBlock(object):
    def __init__(self, raw_buffer):
        self._buffer = raw_buffer
        self.size = struct.unpack("<H", self._buffer[0:2])[0]
        self.version = struct.unpack("<H", self._buffer[2:4])[0]
        self.signature = struct.unpack("<I", self._buffer[4:8])[0]

    def as_dict(self):
        return {
            "size": self.size,
            "version": self.version,
            "signature": "{:X}".format(self.signature),
            "raw": self._buffer.hex()
        }
