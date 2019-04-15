import struct
from pyshellitems.utils import get_unicode_str, get_ascii_str
from pyshellitems.extensionblocks.extensionblock import parse_extension_block
# https://github.com/libyal/libfwsi/blob/master/documentation/Windows%20Shell%20Item%20format.asciidoc#37-uri-shell-item


class ShellItem61(object):
    def __init__(self, raw_buffer):
        self._buffer = raw_buffer
        self.size = struct.unpack("<H", self._buffer[0:2])[0]
        self.type = struct.unpack("<B", self._buffer[2:3])[0]
        self.flags = struct.unpack("<B", self._buffer[3:4])[0]
        self.data_size = struct.unpack("<H", self._buffer[4:6])[0]

        ptr = 6
        if self.data_size > 0:
            raise(
                Exception(
                    "Unhandled shell item x61 with data size: {}".format(
                        self._buffer.hex()
                    )
                )
            )

            unknown1 = struct.unpack("<I", self._buffer[ptr:ptr+4])[0]
            ptr += 4

            unknown2 = struct.unpack("<I", self._buffer[ptr:ptr+4])[0]
            ptr += 4

            timestamp = struct.unpack("<Q", self._buffer[ptr:ptr+8])[0]
            ptr += 8

            unknown3 = struct.unpack("<I", self._buffer[ptr:ptr+4])[0]
            ptr += 4

            unknown4 = self._buffer[ptr:ptr+12]
            ptr += 12

            unknown5 = struct.unpack("<I", self._buffer[ptr:ptr+4])[0]
            ptr += 4

            string1_size = struct.unpack("<I", self._buffer[ptr:ptr + 4])[0]
            ptr += 4
            if self.flags & 0x80:
                # Unicode flag
                string1 = get_unicode_str(
                    self._buffer[ptr:]
                )
            else:
                string1 = get_ascii_str(
                    self._buffer[ptr:]
                )
            ptr += string1_size

            string2_size = struct.unpack("<I", self._buffer[ptr:ptr + 4])[0]
            ptr += 4
            if self.flags & 0x80:
                # Unicode flag
                string2 = get_unicode_str(
                    self._buffer[ptr:]
                )
            else:
                string2 = get_ascii_str(
                    self._buffer[ptr:]
                )
            ptr += string1_size

            string3_size = struct.unpack("<I", self._buffer[ptr:ptr + 4])[0]
            ptr += 4
            if self.flags & 0x80:
                # Unicode flag
                string3 = get_unicode_str(
                    self._buffer[ptr:]
                )
            else:
                string3 = get_ascii_str(
                    self._buffer[ptr:]
                )
            ptr += string1_size
        else:
            ptr = 8
            if self.flags & 0x80:
                # Unicode flag
                self.uri = get_unicode_str(
                    self._buffer[ptr:]
                )
            else:
                self.uri = get_ascii_str(
                    self._buffer[ptr:]
                )

    def as_dict(self):
        return {
            "type": "0x{:02X}".format(self.type),
            "flags": "0x{:02X}".format(self.flags),
            "uri": self.uri
        }
