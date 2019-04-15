import struct

# https://github.com/libyal/libfwsi/blob/master/documentation/Windows%20Shell%20Item%20format.asciidoc#619-extension-block-0xbeef0019


class Beef0013(object):
    def __init__(self, raw_buffer):
        self._buffer = raw_buffer
        self.size = struct.unpack("<H", self._buffer[0:2])[0]
        self.version = struct.unpack("<H", self._buffer[2:4])[0]
        self.signature = struct.unpack("<I", self._buffer[4:8])[0]

    def as_dict(self):
        return {
            "signature": "{:X}".format(self.signature),
            "version": self.version,
            "raw": self._buffer.hex()
        }
