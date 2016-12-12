from Crypto.Cipher import AES  # Using pycrypto module
import base64

if __name__ == "__main__":
    with open("./data/7.txt", "r") as f:
        ciphered_text = "".join([line.strip() for line in f])
    ciphered_text = base64.b64decode(ciphered_text)
    aes = AES.new("YELLOW SUBMARINE")
    cleartext = aes.decrypt(ciphered_text)
    print("Cleartext:\n{}".format(cleartext.decode('utf-8')))
