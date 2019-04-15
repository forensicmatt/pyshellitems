import struct
from pyshellitems.utils import get_unicode_str, get_ascii_str
# https://github.com/libyal/libfwsi/blob/master/documentation/Windows%20Shell%20Item%20format.asciidoc#65-file-entry-extension-block-0xbeef0004


class Beef0004(object):
    def __init__(self, raw_buffer):
        self._buffer = raw_buffer
        self.size = struct.unpack("<H", self._buffer[0:2])[0]
        self.version = struct.unpack("<H", self._buffer[2:4])[0]
        self.signature = struct.unpack("<I", self._buffer[4:8])[0]
        self.created = struct.unpack("<I", self._buffer[8:12])[0]
        self.accessed = struct.unpack("<I", self._buffer[12:16])[0]
        self.identifier = struct.unpack("<H", self._buffer[16:18])[0]

        index = 18
        self.mft_reference = None
        if self.version >= 7:
            index += 2
            self.mft_reference = struct.unpack("<Q", self._buffer[index:index+8])[0]
            index += 8
            index += 8

        if self.version >= 3:
            long_str_size = struct.unpack("<H", self._buffer[index:index+2])[0]
            index += 2

        if self.version >= 9:
            unknown = struct.unpack("<I", self._buffer[index:index + 4])[0]
            index += 4

        if self.version >= 8:
            unknown = struct.unpack("<I", self._buffer[index:index + 4])[0]
            index += 4

        self.long_name = None
        if self.version >= 3:
            self.long_name = get_unicode_str(
                self._buffer[index:]
            )
            index += (len(self.long_name) * 2) + 2

        self.localized_name = None
        if long_str_size > 0:
            if self.version >= 7:
                self.localized_name = get_unicode_str(
                    self._buffer[index:]
                )
                index += (len(self.localized_name) * 2) + 2
            elif self.version >= 3:
                self.localized_name = get_ascii_str(
                    self._buffer[index:]
                )
                index += (len(self.localized_name)) + 1

        self.version_offset = None
        if self.version >= 3:
            self.version_offset = struct.unpack("<H", self._buffer[index:index+2])[0]
            index += 2

    def as_dict(self):
        return {
            "signature": "{:X}".format(self.signature),
            "version": self.version,
            "created": self.created,
            "accessed": self.accessed,
            "identifier": self.identifier,
            "mft_reference": self.mft_reference,
            "long_name": self.long_name,
            "localized_name": self.localized_name,
            "version_offset": self.version_offset,
        }
