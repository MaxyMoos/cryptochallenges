import binascii

def get_16_bytes_blocks_frequency(ciphertext):
    blocks = [ciphertext[i*16:(i+1)*16] for i in range(int(len(ciphertext) / 16))]
    return len(set(blocks))

if __name__ == '__main__':
    with open("./data/8.txt", "r") as f:
        cipher_texts = [line.strip() for line in f]

    minScore = 100

    for ciphertext in cipher_texts:
        curScore = get_16_bytes_blocks_frequency(ciphertext)
        if curScore < minScore:
            winner = ciphertext
            minScore = curScore

    print("The best candidate is {}... with {} repeating blocks".format(winner[:16],
                                                                     int(len(winner)/16) - minScore))
