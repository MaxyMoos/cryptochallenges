import one
import two

import binascii
import string
import operator

def xor_hexstring_with_one_byte(hexStr, byte):
	"""XORs the hexStr variable with a single byte"""
	bytes_array = bytes([byte for char in hexStr[::2]])
	bytes_array_as_hexStr = binascii.hexlify(bytes_array)

	return two.xor_hex_string_to_bytes(hexStr, bytes_array_as_hexStr)

def text_score(text_as_bytes):
	# print(text_as_bytes)
	text_as_chr = [chr(i) for i in text_as_bytes if chr(i) in string.ascii_letters + ' ']
	return len(text_as_chr)

def try_decode_single_xor(hexStr):
	current_winner = None
	highest_score = 0
	good_byte = 0

	for i in range(256):
		result_bytes = xor_hexstring_with_one_byte(hexStr, i)
		if text_score(result_bytes) > highest_score:
			highest_score = text_score(result_bytes)
			current_winner = result_bytes
			good_byte = i

	return good_byte

if __name__ == "__main__":
	encoded_hexStr = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
	cipher_byte = try_decode_single_xor(encoded_hexStr)
	print("The encoding byte is : {}".format(cipher_byte))
	print("Decoded string is : {}".format(xor_hexstring_with_one_byte(encoded_hexStr, cipher_byte)))

