import nine
import base64
import binascii

from Crypto.Cipher import AES


def xor_bytes_to_bytes(first, second):
    if len(first) != len(second):
        return None

    xor_array = []

    for i in range(len(first)):
        xor_array.append(first[i] ^ second[i])

    return bytes(xor_array)


def AES_CBC_encrypt(plaintext, key, IV):
    if len(plaintext) % 16 != 0:
        padded_plaintext = nine.pad_string(plaintext, 4, 16)
    else:
        padded_plaintext = plaintext

    # Prepare inputs
    padded_plaintext_bytes = padded_plaintext.encode('latin1')

    prev = IV
    nb_blocks = int(len(padded_plaintext_bytes) / 16)
    aes_cipher = AES.new(key)
    result = []

    for block in [padded_plaintext_bytes[i*16:(i+1)*16] for i in range(nb_blocks)]:
        xored_blocks = xor_bytes_to_bytes(block, prev)
        ciphered_block = aes_cipher.encrypt(xored_blocks)
        prev = ciphered_block
        result.append(ciphered_block)

    result = b"".join(result)
    return result

def AES_CBC_decrypt(ciphertext, key, IV):
    if len(ciphertext) % 16 != 0:
        if type(ciphertext) == str or type(ciphertext) == unicode:
            padded_ciphertext = nine.pad_string(ciphertext, 4, 16)
        else:
            padded_ciphertext = nine.pad_bytes(ciphertext, 4, 16)
    else:
        padded_ciphertext = ciphertext

    # Prepare inputs
    if type(padded_ciphertext) == str:
        padded_ciphertext_bytes = padded_ciphertext.encode('utf-8')
    else:
        padded_ciphertext_bytes = padded_ciphertext

    prev = IV
    nb_blocks = int(len(padded_ciphertext_bytes) / 16)
    aes_cipher = AES.new(key)
    result = []

    for block in [padded_ciphertext_bytes[i*16:(i+1)*16] for i in range(nb_blocks)]:
        deciphered_block = aes_cipher.decrypt(block)
        xored_blocks = xor_bytes_to_bytes(deciphered_block, prev)
        prev = block
        result.append(xored_blocks)

    result = b"".join(result)
    return result


if __name__ == '__main__':
    with open("./data/10.txt", "r") as f:
        lines = []
        for line in f:
            lines += line.strip()
        ciphered = "".join(lines)
    ciphered = base64.b64decode(ciphered)

    cleartext = AES_CBC_decrypt(ciphered, "YELLOW SUBMARINE", bytes(16))
    print(cleartext.decode('utf-8'))
