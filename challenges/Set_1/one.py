import binascii
import base64


def hex_string_to_bytes(hexStr):
	return binascii.unhexlify(hexStr)

def hex_string_to_string(hexStr):
	return hex_string_to_bytes(hexStr).decode('utf-8')

def hex_string_to_base64_bytes(hexStr):
	return base64.b64encode(hex_string_to_bytes(hexStr))

def hex_string_to_base64_string(hexStr):
	return hex_string_to_base64_bytes(hexStr).decode('utf-8')


if __name__ == "__main__":
	input_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
	print(hex_string_to_base64_string(input_string))