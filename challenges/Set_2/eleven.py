import random

import ten


def generate_random_key(size):
	key = ""
	random.seed()

	while len(key) < size:
		key += chr(random.randint(0, 255))
	return key

def AES_encrypt_with_unknown_key(cleartext):
	key = generate_random_key(16)

	nb_of_prebytes = random.randint(5, 10)
	nb_of_postbytes = random.randint(5, 10)

	prebytes = generate_random_key(nb_of_prebytes)
	postbytes = generate_random_key(nb_of_postbytes)

	padded_cleartext = prebytes + cleartext + postbytes
	print(padded_cleartext)

	ecb_or_cbc = random.randint(1, 2)
	if ecb_or_cbc == 1:
		# ECB it is
		# TODO
		print("ECB")
		pass
	else:
		# CBC then
		ciphertext = ten.AES_CBC_encrypt(padded_cleartext, key, generate_random_key(16))

if __name__ == '__main__':
	AES_encrypt_with_unknown_key("coucou")