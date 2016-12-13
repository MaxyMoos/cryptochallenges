def pad_bytes(input_bytes, padding_byte, block_size):
    while len(input_bytes) % block_size != 0:
        input_bytes += padding_byte
    return input_bytes

def pad_string(input_string, padding_byte, block_size):
    while len(input_string) % block_size != 0:
        input_string += chr(padding_byte)
    return input_string

if __name__ == "__main__":
    input_str = "YELLOW SUBMARINE"
    input_bytes = input_str.encode('utf-8')
    print(pad_bytes(input_bytes, bytes.fromhex("04"), 20))
    print(pad_string(input_str, 4, 20))
