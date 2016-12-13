import three
import five
import base64
import binascii

from itertools import zip_longest

def bitcount(byte):
	"""Return the number of set bits in a byte"""
	count = 0
	while(byte):
		byte &= byte - 1
		count += 1
	return count

def hamming_distance_bytes(bytes1, bytes2):
	"""Return the hamming distance (number of differing bits between bytes)"""
	total = 0

	for byte1, byte2 in zip(bytes1, bytes2):
		xor_byte = byte1 ^ byte2
		total += bitcount(xor_byte)
	return total

def hamming_distance_strings(str1, str2):
	"""Compute the hamming distance between strings"""
	str1_b = str1.encode('utf-8')
	str2_b = str2.encode('utf-8')

	return hamming_distance_bytes(str1_b, str2_b)
		
def open_cipher_file(file):
	"""Open the file and return it as a single string"""
	with open(file, "r") as f:
		cipher_text = ""
		for line in f:
			cipher_text += line.strip()
	return cipher_text

def get_top_n_keysizes(cipher_bytes, n_samples, number_of_keysizes):
	"""Return the n keysizes with the minimum normalized distance"""
	sorted_tuples = []
	top_3_keysizes = [50, 50, 50]
	top_3_distances = [100, 100, 100]

	for keysize in range(2, 41):
		samples = [cipher_bytes[i*keysize:(i+1)*keysize] for i in range(n_samples + 1)]
		distances = [hamming_distance_bytes(samples[i], samples[i+1]) for i in range(len(samples) - 1)]
		avg_dist = sum(distances) / len(distances)
		sorted_tuples.append((keysize, avg_dist / keysize))

	sorted_tuples.sort(key=lambda item: item[1])
	return sorted_tuples[0:number_of_keysizes]


# Let's do this
if __name__ == "__main__":
	final_key = ""
	base64_encoded_ciphertext = open_cipher_file("./data/6.txt")
	cipher_bytes = base64.b64decode(base64_encoded_ciphertext)

	# Get the 3 most probable keysizes, using 16 samples of KEYSIZE bytes for analysis
	# as it gives out a better precision than just using two samples
	top_3_keys = get_top_n_keysizes(cipher_bytes, 16, 3)
	print(top_3_keys)

	top_3_keysizes = [item[0] for item in top_3_keys]
	final_keys = []

	# For each candidate, crack the corresponding key
	for probable_keysize in top_3_keysizes:
		split_cipherbytes = list(zip_longest(*(iter(cipher_bytes),) * probable_keysize))
		transposed_split_cipherbytes = list(zip_longest(*split_cipherbytes))
		final_key = ""

		for element in transposed_split_cipherbytes:
			element = [elem for elem in element if elem is not None]
			elem_bytes = bytes(element)
			key = three.try_decode_single_xor(binascii.hexlify(elem_bytes))
			final_key += chr(key)
		final_keys.append(final_key)
		print("Keysize candidate = {} - Key = {}".format(probable_keysize, final_key))

	# Take the most likely key and decode the input bytes
	final_key = final_keys[0]
	cipher_text = cipher_bytes.decode('utf-8')
	decoded_hexStr = five.repeating_key_xor(cipher_text, final_key)
	decoded_string = binascii.unhexlify(decoded_hexStr)
	print("decoded text:\n{}".format(decoded_string))