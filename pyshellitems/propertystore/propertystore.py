import struct
from pyshellitems.guid import Guid

# https://github.com/libyal/libfwps/blob/master/documentation/Windows%20Property%20Store%20format.asciidoc#22-serialized-numeric-property-value-aka-numeric-shell-property
# https://github.com/libyal/libfole/blob/master/documentation/OLE%20definitions.asciidoc#2-property-value-types

OLE_TYPE_KNOWN_MAPPING = {
    0x0000: "VT_EMPTY",
    0x0001: "VT_NULL",
    0x0002: "VT_I2",
    0x0003: "VT_I4",
    0x0004: "VT_R4",
    0x0005: "VT_R8",
    0x0006: "VT_CY",
    0x0007: "VT_DATE",
    0x0008: "VT_BSTR",
    0x0009: "VT_DISPATCH",
    0x000a: "VT_ERROR",
    0x000b: "VT_BOOL",
    0x000c: "VT_VARIANT",
    0x000d: "VT_UNKNOWN",
    0x000e: "VT_DECIMAL",
    0x0010: "VT_I1",
    0x0011: "VT_UI1",
    0x0012: "VT_UI2",
    0x0013: "VT_UI4",
    0x0014: "VT_I8",
    0x0015: "VT_UI8",
    0x0016: "VT_INT",
    0x0017: "VT_UINT",
    0x0018: "VT_VOID",
    0x0019: "VT_HRESULT",
    0x001a: "VT_PTR",
    0x001b: "VT_SAFEARRAY",
    0x001c: "VT_CARRAY",
    0x001d: "VT_USERDEFINED",
    0x001e: "VT_LPSTR",
    0x001f: "VT_LPWSTR",
    0x0024: "VT_RECORD",
    0x0025: "VT_INT_PTR",
    0x0026: "VT_UINT_PTR",
    0x0040: "VT_FILETIME",
    0x0041: "VT_BLOB",
    0x0042: "VT_STREAM",
    0x0043: "VT_STORAGE",
    0x0044: "VT_STREAMED_OBJECT",
    0x0045: "VT_STORED_OBJECT",
    0x0046: "VT_BLOB_OBJECT",
    0x0047: "VT_CF",
    0x0048: "VT_CLSID",
    0x0049: "VT_VERSIONED_STREAM"
}


def iterate_serialized_values(raw_buffer):
    ptr = 0

    while ptr < len(raw_buffer):
        size = struct.unpack("<I", raw_buffer[ptr:ptr+4])[0]
        if size == 0:
            break

        sv = SerializedValue(
            raw_buffer[ptr:ptr+size]
        )

        yield sv

        ptr += size


def format_serial_value(type_int, raw_buffer):
    if type_int == 0x0002:
        # VT_I2
        return struct.unpack("<h", raw_buffer[0:2])[0]
    elif type_int == 0x0003:
        # VT_I4
        return struct.unpack("<l", raw_buffer[0:2])[0]
    elif type_int == 0x0004:
        # VT_R4
        return struct.unpack("<f", raw_buffer[0:4])[0]
    elif type_int == 0x0005:
        # VT_R8
        return struct.unpack("<d", raw_buffer[0:8])[0]
    elif type_int == 0x0010:
        # VT_I1
        return struct.unpack("<b", raw_buffer[0:1])[0]
    elif type_int == 0x0011:
        # VT_UI1
        return struct.unpack("<B", raw_buffer[0:1])[0]
    elif type_int == 0x0012:
        # VT_UI2
        return struct.unpack("<H", raw_buffer[0:2])[0]
    elif type_int == 0x0013:
        # VT_UI4
        return struct.unpack("<I", raw_buffer[0:4])[0]
    elif type_int == 0x0014:
        # VT_I8
        return struct.unpack("<q", raw_buffer[0:8])[0]
    elif type_int == 0x0015:
        # VT_UI8
        return struct.unpack("<Q", raw_buffer[0:8])[0]
    elif type_int == 0x0015:
        # VT_UI8
        return struct.unpack("<Q", raw_buffer[0:8])[0]
    elif type_int == 0x001F:
        # VT_LPWSTR
        byte_length = struct.unpack("<I", raw_buffer[0:4])[0]
        return raw_buffer[4:(4+(byte_length*2))-2].decode("utf-16le")
    else:
        return raw_buffer.hex()


class SerializedValue(object):
    def __init__(self, raw_buffer):
        self._buffer = raw_buffer
        self.size = struct.unpack("<I", self._buffer[0:4])[0]
        self.identifier = struct.unpack("<I", self._buffer[4:8])[0]
        self.reserved = struct.unpack("<B", self._buffer[8:9])[0]
        self.property_value_type = struct.unpack("<H", self._buffer[9:11])[0]

    def get_raw_property(self):
        return self._buffer[13:self.size]

    @property
    def value(self):
        raw_property = self.get_raw_property()
        formatted_property = format_serial_value(
            self.property_value_type,
            raw_property
        )

        return formatted_property

    def get_type_name(self):
        id_int = self.property_value_type
        if id_int in OLE_TYPE_KNOWN_MAPPING:
            return OLE_TYPE_KNOWN_MAPPING[id_int]
        else:
            return "<UNKNOWN OLE TYPE NAME>".format(id_int)

    def as_dict(self):
        return {
            "identifier": "{:04X} [{}]".format(
                self.property_value_type,
                self.get_type_name()
            ),
            "value": self.value
        }


class PropertySheet(object):
    def __init__(self, raw_buffer):
        self._buffer = raw_buffer
        self.size = struct.unpack("<I", self._buffer[0:4])[0]
        self.version = self._buffer[4:8]
        self.guid = Guid(self._buffer[8:24])

    def get_values(self):
        value_list = list(iterate_serialized_values(
            self._buffer[24:self.size]
        ))
        return value_list

    @property
    def raw_value(self):
        return self._buffer[24:self.size]

    def as_dict(self):
        value_list = []
        for serialized_value in iterate_serialized_values(self._buffer[24:self.size]):
            value_list.append(
                serialized_value.as_dict()
            )

        return {
            "version": self.version.decode("ascii", errors="replace"),
            "guid": str(self.guid),
            "values": value_list
        }


class PropertyStoreList(object):
    def __init__(self, raw_buffer):
        self._buffer = raw_buffer

    def __iter__(self):
        ptr = 0
        while ptr < len(self._buffer):
            sheet_size = struct.unpack("<I", self._buffer[ptr:ptr+4])[0]

            if sheet_size == 0:
                break

            sheet = PropertySheet(
                self._buffer[ptr:ptr+sheet_size]
            )

            yield sheet

            ptr += sheet.size

    def as_dict(self):
        ps_list = []
        for ps_sheet in self:
            ps_list.append(
                ps_sheet.as_dict()
            )
        return ps_list
