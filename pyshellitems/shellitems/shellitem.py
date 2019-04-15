import struct
from pyshellitems.shellitems.shellitem_propview import PropertyViewItem
from pyshellitems.shellitems.shellitem_propview_delegate import PropertyViewDelegateItem
from pyshellitems.shellitems.shellitem_apps import ApplicationShellItem
from pyshellitems.shellitems.shellitem_fileentry import FileEntryShellItem
from pyshellitems.shellitems.shellitem_x1f import ShellItem1F
from pyshellitems.shellitems.shellitem_x61 import ShellItem61


def parse_shell_item(raw_buffer):
    shell_size = struct.unpack(
        "<H", raw_buffer[0:2]
    )[0]
    if shell_size == 0:
        return None

    shell_class = struct.unpack(
        "<B", raw_buffer[2:3]
    )[0]

    shell_signature = struct.unpack(
        "<I", raw_buffer[6:10]
    )[0]

    if shell_signature == 1397772353:
        # APPS
        return ApplicationShellItem(
            raw_buffer
        )
    elif shell_signature == 603896814:
        # 0x23febbee
        return PropertyViewItem(
            raw_buffer
        )
    elif shell_signature == 0x23a3dfd5:
        # 0x23a3dfd5
        return PropertyViewDelegateItem(
            raw_buffer
        )

    if shell_class & 0x70 == 0x30:
        # File Entry Shell Item
        return FileEntryShellItem(
            raw_buffer
        )

    if shell_class == 0x00:
        return ShellItem(
            raw_buffer
        )
    elif shell_class == 0x1f:
        # URI shell item
        return ShellItem1F(
            raw_buffer
        )
    elif shell_class == 0x61:
        return ShellItem61(
            raw_buffer
        )
    else:
        return ShellItem(
            raw_buffer
        )


class ShellItem(object):
    def __init__(self, raw_buffer):
        self._buffer = raw_buffer

    @property
    def size(self):
        return struct.unpack("<H", self._buffer[0:2])[0]

    @property
    def type(self):
        return struct.unpack("<B", self._buffer[2:3])[0]

    @property
    def unknown1(self):
        return struct.unpack("<B", self._buffer[3:4])[0]

    @property
    def hex_buffer(self):
        return self._buffer.hex()

    def as_dict(self):
        return {
            "type": "0x{:02X}".format(self.type),
            "unknown": "0x{:02X}".format(self.unknown1),
            "raw": self._buffer.hex()
        }
