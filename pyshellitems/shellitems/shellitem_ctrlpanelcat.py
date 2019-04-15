import struct

# https://github.com/libyal/libfwsi/blob/master/documentation/Windows%20Shell%20Item%20format.asciidoc#432-control-panel-category-shell-item

CATEGORY_MAPPING = {
    0: "All Control Panel Items",
    1: "Appearance and Personalization",
    2: "Hardware and Sound",
    3: "Network and Internet",
    4: "Sounds, Speech, and Audio Devices",
    5: "System and Security",
    6: "Clock, Language, and Region",
    7: "Ease of Access",
    8: "Programs",
    9: "User Accounts",
    10: "Security Center",
    11: "Mobile PC"
}


class ControlPanelCategoryItem(object):
    def __init__(self, raw_buffer):
        self._buffer = raw_buffer
        self.size = struct.unpack("<H", self._buffer[0:2])[0]
        self.type = struct.unpack("<B", self._buffer[2:3])[0]
        self.unknown1 = struct.unpack("<B", self._buffer[3:4])[0]
        self.signature = struct.unpack("<I", self._buffer[4:8])[0]
        self.category = struct.unpack("<I", self._buffer[8:12])[0]

    def get_category_name(self):
        category_int = self.category
        if category_int in CATEGORY_MAPPING:
            return CATEGORY_MAPPING[category_int]
        else:
            return "<UNKNOWN CATEGORY: {}>".format(
                category_int
            )

    def as_dict(self):
        return {
            "type": "0x{:02X}".format(self.type),
            "unknown1": self.unknown1,
            "signature": "{:04X}".format(self.signature),
            "category": self.get_category_name()
        }

