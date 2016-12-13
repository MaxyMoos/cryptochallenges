import two

import binascii


def repeating_key_xor(cleartext, key):
	repeated_key = key * int(len(cleartext) / len(key)) + key[0:(len(cleartext) % len(key))]
	
	cleartxt_as_bytes = cleartext.encode('utf-8')
	repeated_key_as_bytes = repeated_key.encode('utf-8')

	xor_results = two.xor_bytes_to_bytes(cleartxt_as_bytes, repeated_key_as_bytes)
	return binascii.hexlify(xor_results)

if __name__ == "__main__":
	ref_txt = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
	key = "ICE"
	result = repeating_key_xor(ref_txt, key).decode('utf-8')
	print(binascii.unhexlify(repeating_key_xor(binascii.unhexlify(result).decode('utf-8'), key)))
