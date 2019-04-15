import struct
from pyshellitems.guid import Guid

# https://github.com/libyal/libfwsi/blob/master/documentation/Windows%20Shell%20Item%20format.asciidoc#619-extension-block-0xbeef0019


class Beef0019(object):
    def __init__(self, raw_buffer):
        self._buffer = raw_buffer
        self.size = struct.unpack("<H", self._buffer[0:2])[0]
        self.version = struct.unpack("<H", self._buffer[2:4])[0]
        self.signature = struct.unpack("<I", self._buffer[4:8])[0]
        self.folder_guid = Guid(self._buffer[8:24])
        self.unknown_guid = Guid(self._buffer[24:40])
        self.offset = struct.unpack("<H", self._buffer[40:42])[0]

    def as_dict(self):
        return {
            "signature": "{:X}".format(self.signature),
            "version": self.version,
            "folder_guid": str(self.folder_guid),
            "unknown_guid": str(self.unknown_guid),
            "offset": self.offset
        }
