def get_unicode_str(raw_buffer):
    raw_string = b''
    for i in range(0, len(raw_buffer), 2):
        if raw_buffer[i:i+2] == b'\x00\x00':
            break
        else:
            raw_string += raw_buffer[i:i+2]

    uni_str = raw_string.decode("utf-16le")
    return uni_str


def get_ascii_str(raw_buffer):
    index = raw_buffer.find(b"\x00")
    ascii_str = raw_buffer[:index]
    return ascii_str.decode("ascii")
