import random

import ten

from Crypto.Cipher import AES


def generate_random_bytes(size):
    key_data = []
    random.seed()

    while len(key_data) < size:
        key_data.append(random.randint(0, 255))
    return bytes(bytearray(key_data))

def AES_encrypt_random_mode_with_unknown_key(cleartext):
    key = generate_random_bytes(16)

    nb_of_prebytes = random.randint(5, 10)
    nb_of_postbytes = random.randint(5, 10)

    prebytes_bytearray = generate_random_bytes(nb_of_prebytes)
    postbytes_bytearray = generate_random_bytes(nb_of_postbytes)

    prebytes_str = bytes(prebytes_bytearray).decode('latin1')
    postbytes_str = bytes(postbytes_bytearray).decode('latin1')

    padded_cleartext = prebytes_str + cleartext + postbytes_str

    ecb_or_cbc = random.randint(1, 2)
    if ecb_or_cbc == 1:
        # ECB it is
        aes_cipher = AES.new(key)
        # PKCS7 padding for cleartext
        cleartext = padded_cleartext.encode('utf-8')
        while len(cleartext) % 16 != 0:
            cleartext += bytes(1)
        ciphertext = aes_cipher.encrypt(cleartext)
    else:
        # CBC then
        iv = generate_random_bytes(16)
        ciphertext = ten.AES_CBC_encrypt(padded_cleartext, key, iv)
    return ciphertext

def get_16_bytes_blocks_frequency(ciphertext):
    blocks = [ciphertext[i*16:(i+1)*16] for i in range(int(len(ciphertext) / 16))]
    return len(set(blocks)) / len(blocks)

def analyze_ECB_or_CBC(ciphertext):
    score = get_16_bytes_blocks_frequency(ciphertext)
    if score < 1:
        print("Analysis : Probably ECB")
    else:
        print("Analysis : Probably CBC")

def is_algo_ECB_or_CBC(cipher_function):
    cleartext = "A" * 100  # Lots of redundancy to detect ECB
    ciphertext = cipher_function(cleartext)
    analyze_ECB_or_CBC(ciphertext)

if __name__ == '__main__':
    is_algo_ECB_or_CBC(AES_encrypt_random_mode_with_unknown_key)
