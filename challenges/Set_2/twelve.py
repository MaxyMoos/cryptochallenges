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

    aes_cipher = AES.new(GLOBAL_KEY)

    # Append the unknown string
    if type(cleartext) == str:
        input_bytes = cleartext.encode('utf-8')
    elif type(cleartext) == bytes:
        input_bytes = cleartext
    else:
        print("Unsupported type for cleartext : {}".format(type(cleartext)))
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


def crack_ECB_cipher(cipher_function):
    # These two variables represent the 'unknown-string' param from the challenge
    unknown_bytes_array = bytearray()
    unknown_bytes = bytes(unknown_bytes_array)

    offset = 0

    while True:
        # Handle 'unknown-string's longer than 16 bytes:
        # if we've discovered a whole block, we need to continue analyze on the next block
        if len(unknown_bytes) > 0 and len(unknown_bytes) % 16 == 0:
            offset += 1

        if not is_cipher_ECB(cipher_function):
            raise Exception("Apparently not a ECB cipher, aborting crack...")

        block_size = detect_cipher_block_size(cipher_function)

        # Generate a cleartext of "A" characters repeated to the necessary length
        needed_length = (offset + 1) * block_size - len(unknown_bytes) - 1
        cleartext_bytes = bytearray([65] * needed_length)

        # Append what we already know of the 'unknown-string'
        cleartext_bytes_with_key = bytes(cleartext_bytes) + unknown_bytes

        # ...and generate all possible inputs for the next byte to be discovered
        all_possible_inputs = [bytes(cleartext_bytes_with_key + bytearray([i]))
                               for i in range(256)]

        # Map all ciphertexts to all the possible bytes...
        all_blocks = {cipher_function(all_possible_inputs[i])[offset*16:16*(offset+1)]: i for i in range(256)}

        # Compute the actual value
        ciphertext = cipher_function(bytes(cleartext_bytes))

        # If there's nothing to identify, it means we've found it all!
        if len(ciphertext[offset*16:(offset+1)*16]) == 0:
            break

        # And identify the actual byte with our dictionary
        key_byte = all_blocks[ciphertext[offset*16:(offset+1)*16]]

        # Append the new byte to the ones already found
        unknown_bytes_array += bytearray([key_byte])
        unknown_bytes = bytes(unknown_bytes_array)

    print("{}".format(unknown_bytes.decode('utf-8')))


if __name__ == '__main__':
    crack_ECB_cipher(encrypt_ECB_with_global_key)
