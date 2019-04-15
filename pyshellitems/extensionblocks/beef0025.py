import struct


class Beef0025(object):
    def __init__(self, raw_buffer):
        self._buffer = raw_buffer
        self.size = struct.unpack("<H", self._buffer[0:2])[0]
        self.version = struct.unpack("<H", self._buffer[2:4])[0]
        self.signature = struct.unpack("<I", self._buffer[4:8])[0]
        self.unknown1 = struct.unpack("<I", self._buffer[8:12])[0]
        self.created = struct.unpack("<Q", self._buffer[12:20])[0]
        self.modified = struct.unpack("<Q", self._buffer[20:28])[0]
        self.accessed = struct.unpack("<Q", self._buffer[28:36])[0]
        self.offset = struct.unpack("<H", self._buffer[36:38])[0]

    def as_dict(self):
        return {
            "signature": "{:X}".format(self.signature),
            "version": self.version,
            "unknown1": self.unknown1,
            "created": self.created,
            "modified": self.modified,
            "accessed": self.accessed,
            "offset": self.offset
        }
