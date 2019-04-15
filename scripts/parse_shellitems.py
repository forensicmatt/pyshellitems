import os
import sys
sys.path.append("..")
import json
import argparse
from pyshellitems.shellitems.shellitem import parse_shell_item


def get_arguments():
    usage = "Parse a raw file containing a shell item or a folder of shell items. "\
            "This script looks for *.shellitem or *BagMRU.* file names."

    arguments = argparse.ArgumentParser(
        description=usage,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    arguments.add_argument(
        "-s", "--source",
        dest="source",
        action="store",
        required=True,
        help="The source folder or file."
    )

    return arguments


def parse_shellitem_file(source):
    print("Parsing: {}".format(source))
    with open(source, "rb") as fh:
        raw_data = fh.read()
        si = parse_shell_item(
            raw_data
        )
        print("{}".format(
            json.dumps(si.as_dict())
        ))


def main():
    arguments = get_arguments()
    options = arguments.parse_args()
    print("Source: {}".format(options.source))

    if os.path.isfile(options.source):
        parse_shellitem_file(
            options.source
        )
    elif os.path.isdir(options.source):
        for subdir, dirs, files in os.walk(options.source):
            for file in files:
                file_path = subdir + os.sep + file
                if file_path.endswith(".shellitem") or "BagMRU" in file_path:
                    parse_shellitem_file(
                        file_path
                    )
    else:
        raise (Exception("File or Path needed."))


if __name__ == "__main__":
    main()
