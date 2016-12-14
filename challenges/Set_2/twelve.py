import base64
import eleven

from Crypto.Cipher import AES


GLOBAL_KEY = None
UNKNOWN_STRING_B64 = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
UNKNOWN_STRING = base64.b64decode(UNKNOWN_STRING_B64)


def encrypt_ECB_with_global_key(cleartext):
    global GLOBAL_KEY
    global UNKNOWN_STRING

    if GLOBAL_KEY is None:
        GLOBAL_KEY = eleven.generate_random_bytes(16)

    # ECB it is
    aes_cipher = AES.new(GLOBAL_KEY)

    # Append the unknown string
    input_bytes = cleartext.encode('utf-8')
    input_bytes += UNKNOWN_STRING

    # PKCS7 padding for cleartext
    while len(input_bytes) % 16 != 0:
        input_bytes += bytes(1)
    ciphertext = aes_cipher.encrypt(input_bytes)
    return ciphertext


def detect_cipher_block_size(cipher_function):
    ciphertexts = []
    for i in range(128):
        cleartext = "A" * i
        ciphertext = cipher_function(cleartext)
        ciphertexts.append(ciphertext)

    last = ciphertexts[-1]
    candidate = ciphertexts[0]
    # The 5 index is kinda arbitrary - we consider that getting 5 consecutive identical bytes
    # is statistically impossible unless we're already at/past block length
    while candidate[0:5] != last[0:5]:
        candidate = ciphertexts[ciphertexts.index(candidate) + 1]
    i = 0
    while candidate[i] == last[i]:
        i += 1
    return i


def is_cipher_ECB(cipher_function, block_size=None):
    if block_size is None:
        block_size = detect_cipher_block_size(cipher_function)

    cleartext = "A" * 2 * block_size
    ciphertext = cipher_function(cleartext)
    return ciphertext[0:block_size] == ciphertext[block_size:2*block_size]


if __name__ == '__main__':
    print(detect_cipher_block_size(encrypt_ECB_with_global_key))
    print("Cipher is ECB : {}".format(is_cipher_ECB(encrypt_ECB_with_global_key)))
