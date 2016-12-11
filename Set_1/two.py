import one
from operator import xor


def xor_bytes_to_bytes(first, second):
	if len(first) != len(second):
		return None

	xor_array = []

	for i in range(len(first)):
		xor_array.append(first[i] ^ second[i])

	return bytes(xor_array)

def xor_hex_string_to_bytes(first, second):
	return xor_bytes_to_bytes(one.hex_string_to_bytes(first),
							  one.hex_string_to_bytes(second))


if __name__ == "__main__":
	input_1 = "1c0111001f010100061a024b53535009181c"
	input_2 = "686974207468652062756c6c277320657965"
	print(xor_hex_string_to_bytes(input_1, input_2))