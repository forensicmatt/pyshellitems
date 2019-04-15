import os
import uuid
import pylnk
import struct
import argparse


def get_arguments():
    usage = "Extract shell items from link files for research purposes."

    arguments = argparse.ArgumentParser(
        description=usage
    )

    arguments.add_argument(
        "-s", "--source",
        dest="source",
        action="store",
        required=True,
        help="The source folder or link file."
    )

    arguments.add_argument(
        "-o", "--output",
        dest="output",
        action="store",
        required=True,
        help="The output folder."
    )

    return arguments


def iter_shell_items(target_data, out_file_base):
    ptr = 0
    count = 0
    while ptr < len(target_data):
        size = struct.unpack("<H", target_data[ptr:ptr+2])[0]
        if size == 0:
            break

        shell_buffer = target_data[ptr:ptr+size]
        shell_item = ShellItem(
            shell_buffer
        )

        base_name = os.path.basename(out_file_base)
        base_path = os.path.dirname(out_file_base)

        out_location = base_path + os.sep + "0x{:02X}.{}.{}.shellitem".format(
            shell_item.type,
            base_name,
            count
        )
        with open(out_location, "wb") as out:
            out.write(shell_buffer)

        print(shell_item.as_dict())

        ptr += size
        count += 1


def handle_lnk_file(lnk_location, options):
    print("handling {}".format(lnk_location))
    out_file_base = os.path.join(
        options.output,
        uuid.uuid4().hex
    )

    with open(lnk_location, "rb") as lnk_fh:
        lnk_file = pylnk.file()
        lnk_file.open_file_object(lnk_fh)

        if lnk_file.link_target_identifier_data is not None:
            iter_shell_items(
                lnk_file.link_target_identifier_data,
                out_file_base
            )


def main():
    arguments = get_arguments()
    options = arguments.parse_args()
    print("Source: {}".format(options.source))

    if os.path.isfile(options.source):
        handle_lnk_file(
            options.source,
            options
        )
    elif os.path.isdir(options.source):
        for subdir, dirs, files in os.walk(options.source):
            for file in files:
                file_path = subdir + os.sep + file
                if file_path.endswith(".lnk"):
                    handle_lnk_file(
                        file_path,
                        options
                    )
    else:
        raise(Exception("File or Path needed."))


class ShellItem(object):
    def __init__(self, raw_buffer):
        self._buffer = raw_buffer
        self.size = struct.unpack(
            "<H", self._buffer[0:2]
        )[0]
        self.type = struct.unpack(
            "<B", self._buffer[2:3]
        )[0]

    @property
    def hex_buffer(self):
        return self._buffer.hex()

    def as_dict(self):
        return {
            "type": "{:02X}".format(self.type),
            "raw": self.hex_buffer
        }


if __name__ == "__main__":
    main()
