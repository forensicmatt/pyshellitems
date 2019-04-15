import sys
sys.path.append("..")
import re
import struct
import argparse
from pyshellitems.guid import Guid

RE_DEFINE_GUID = re.compile(
    r"^DEFINE_GUID\(\s{0,}?([a-zA-Z0-9_]{1,})\s{0,}?,\s{0,}?"
    r"(0x[0-9a-f]{1,8}L?|0),\s?(0x[0-9a-f]{1,4}|0),\s?"
    r"(0x[0-9a-f]{1,4}|0), \s?(0x[0-9a-f]{1,2}|0),\s?"
    r"(0x[0-9a-f]{1,2}|0),\s?(0x[0-9a-f]{1,2}|0),\s?"
    r"(0x[0-9a-f]{1,2}|0),\s?(0x[0-9a-f]{1,2}|0),\s?"
    r"(0x[0-9a-f]{1,2}|0),\s?(0x[0-9a-f]{1,2}|0),\s?"
    r"(0x[0-9a-f]{1,2}|0)\s{0,}?\)",
    re.I
)


def get_arguments():
    usage = "Create guid def from header file."

    arguments = argparse.ArgumentParser(
        description=usage,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    arguments.add_argument(
        "-s", "--source",
        dest="source",
        action="store",
        required=True,
        help="The source."
    )

    return arguments


def translate_guid(match):
    raw_buffer = b""

    p1 = struct.pack("<L", int(match.group(2).strip("L"), 16))
    p2 = struct.pack("<H", int(match.group(3), 16))
    p3 = struct.pack("<H", int(match.group(4), 16))

    raw_buffer += p1
    raw_buffer += p2
    raw_buffer += p3

    raw_buffer += struct.pack("<B", int(match.group(5), 16))
    raw_buffer += struct.pack("<B", int(match.group(6), 16))
    raw_buffer += struct.pack("<B", int(match.group(7), 16))
    raw_buffer += struct.pack("<B", int(match.group(8), 16))
    raw_buffer += struct.pack("<B", int(match.group(9), 16))
    raw_buffer += struct.pack("<B", int(match.group(10), 16))
    raw_buffer += struct.pack("<B", int(match.group(11), 16))
    raw_buffer += struct.pack("<B", int(match.group(12), 16))

    guid_obj = Guid(raw_buffer)

    raw_hex = raw_buffer.hex()

    return "{} {}".format(
        match.group(1), str(guid_obj)
    )


def main():
    arguments = get_arguments()
    options = arguments.parse_args()

    with open(options.source, "r") as fh:
        print("import pyshellitems.guid as guid")
        for line in fh:
            line = line.strip()
            match = RE_DEFINE_GUID.match(line)
            if match:
                print(translate_guid(match))


if __name__ == "__main__":
    main()
