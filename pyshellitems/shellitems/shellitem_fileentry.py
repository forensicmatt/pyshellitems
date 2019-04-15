import struct
from pyshellitems.extensionblocks.extensionblock import parse_extension_block
from pyshellitems.utils import get_ascii_str, get_unicode_str

SUB_FLAG_MAPPING = {
    0x01: "Directory",
    0x02: "File",
    0x04: "Has Unicode"
}


def get_sub_flag_str(flag_int):
    flag_str_list = []
    for key, value in SUB_FLAG_MAPPING:
        if flag_int & key:
            flag_str_list.append(
                value
            )

    return "|".join(flag_str_list)


class FileEntryShellItem(object):
    def __init__(self, raw_buffer):
        self._buffer = raw_buffer
        self.size = struct.unpack("<H", self._buffer[0:2])[0]
        self.type = struct.unpack("<B", self._buffer[2:3])[0]
        self.sub_flag = self.type - 0x30
        self.unknown1 = struct.unpack("<B", self._buffer[3:4])[0]
        self.file_size = struct.unpack("<I", self._buffer[4:8])[0]
        self.modified = struct.unpack("<I", self._buffer[8:12])[0]
        self.file_attributes = struct.unpack("<H", self._buffer[12:14])[0]

        sub_flag = self.sub_flag
        self.name = None
        if sub_flag & 0x08:
            # Unicode
            self.name = get_unicode_str(
                self._buffer[14:]
            )
        else:
            self.name = get_ascii_str(
                self._buffer[14:]
            )

        name_start_offset = 14
        name_len = len(self.name) + 1
        padding = name_len % 2
        eb_offset = name_start_offset + name_len + padding
        self.extension_block = None
        self.extension_block = parse_extension_block(
            self._buffer[eb_offset:]
        )

    def as_dict(self):
        extension_dict = None
        if self.extension_block:
            extension_dict = self.extension_block.as_dict()

        return {
            "type": "0x{:02X}".format(self.type),
            "sub_flag": "0x{:02X}".format(self.sub_flag),
            "file_size": self.file_size,
            "modified": self.modified,
            "file_attributes": self.file_attributes,
            "name": self.name,
            "extension_block": extension_dict
        }
