import os
import re
import argparse
from yarp import Registry


class UsrClassHandler(object):
    def __init__(self, usrclass_location):
        self.hive = Registry.RegistryHive(
            open(usrclass_location, 'rb')
        )

        log_mapping = {
            "log": None,
            "log1": None,
            "log2": None
        }
        base_name = os.path.basename(
            usrclass_location
        )
        base_location = os.path.dirname(
            usrclass_location
        )
        for file_name in os.listdir(base_location):
            full_path = os.path.join(
                base_location,
                file_name
            )
            if os.path.isfile(full_path):
                match = re.search('^{}[.](LOG\d?)$'.format(base_name), file_name, flags=re.I)
                if match:
                    group = match.group(1)
                    log_mapping[group.lower()] = open(full_path, 'rb')

        print("Attempting Hive Recovery...")
        recovery_result = self.hive.recover_auto(
            log_mapping['log'],
            log_mapping['log1'],
            log_mapping['log2']
        )
        print("Recovery: {}".format(recovery_result.recovered))

    def get_bagmru_key(self):
        key = self.hive.find_key("Local Settings\\Software\\Microsoft\\Windows\\Shell\\BagMRU")
        return key


def get_arguments():
    usage = "Extract shellbags from usrclass hive for research purposes."

    arguments = argparse.ArgumentParser(
        description=usage
    )

    arguments.add_argument(
        "-s", "--source",
        dest="source",
        action="store",
        required=True,
        help="The source USRCLASS.DAT file."
    )

    arguments.add_argument(
        "-p", "--prefix",
        dest="prefix",
        action="store",
        default="",
        required=False,
        help="Prefix to append to file names."
    )

    arguments.add_argument(
        "-o", "--output",
        dest="output",
        action="store",
        required=True,
        help="The output folder."
    )

    return arguments


def extract_value(key_value, out_path, out_stack, prefix):
    value_name = key_value.name()
    if re.match(r"\d{1,}$", value_name):
        value_data = key_value.data_raw()

        file_name = ".".join(out_stack)
        file_name = ".".join([file_name, value_name])
        file_name = prefix + file_name

        out_file = os.path.join(
            out_path,
            file_name
        )
        print("Writing out: {}".format(out_file))
        with open(out_file, 'wb') as fh:
            fh.write(value_data)


def key_extraction(key, out_path, out_stack, prefix):
    for key_value in key.values():
        extract_value(
            key_value,
            out_path,
            out_stack,
            prefix
        )

    for sub_key in key.subkeys():
        out_stack.append(sub_key.name())
        key_extraction(
            sub_key,
            out_path,
            out_stack,
            prefix
        )
        out_stack.pop()


def handle_usrclass_reg(options):
    handler = UsrClassHandler(
        options.source
    )
    bagmru_key = handler.get_bagmru_key()
    key_extraction(
        bagmru_key,
        options.output,
        ["BagMRU"],
        options.prefix
    )


def main():
    arguments = get_arguments()
    options = arguments.parse_args()
    print("Source: {}".format(options.source))

    if not os.path.exists(options.output):
        os.makedirs(options.output)

    if os.path.isfile(options.source):
        handle_usrclass_reg(
            options
        )
    else:
        raise(Exception("File needed."))


if __name__ == "__main__":
    main()
