import eleven
import twelve

from Crypto.Cipher import AES

class parsedObject(object):
    SEP = '&'
    VALUE_SEP = '='

    def __init__(self, input_str):
        print("input to parsedObject = {}".format(input_str))
        key_values = input_str.split(self.SEP)
        for item in key_values:
            if not self.VALUE_SEP in item:
                raise ValueError("Badly formatted input")
            split = item.split(self.VALUE_SEP)
            print("Key = {} ; Value = {}".format(split[0], split[1]))
            setattr(self, split[0], split[1])

def profile_for(email_address):
    metachars = ['=', '&']

    for metachar in metachars:
        email_address = email_address.replace(metachar, '')

    return "email={}&uid={}&role={}".format(email_address, 10, 'user')

def encrypt_user_profile(u_profile, key):
    print("Want to encrypt: {}".format(u_profile))
    if type(u_profile) == str:
        u_profile_bytes = u_profile.encode('utf-8')
    else:
        u_profile_bytes = u_profile

    while len(u_profile_bytes) % 16 != 0:
        u_profile_bytes += bytes(1)

    aes_cipher = AES.new(key)
    return aes_cipher.encrypt(u_profile_bytes)

def decrypt_and_parse_user_profile(ciphertext, key):
    aes_cipher = AES.new(key)
    return parsedObject(aes_cipher.decrypt(ciphertext).decode('utf-8'))

if __name__ == '__main__':
    random_aes_key = eleven.generate_random_bytes(16)
    print("key = {}".format(random_aes_key))
    email = "A" * 32
    prof = profile_for(email)
    print(prof)
    print(encrypt_user_profile(prof, random_aes_key)[0:16])
    print(encrypt_user_profile(prof, random_aes_key))
    # print(twelve.crack_ECB_cipher(lambda x: encrypt_user_profile(profile_for(x), random_aes_key)))
    # u_prof = profile_for(email)
    # ciphertext = encrypt_user_profile(u_prof, random_aes_key)
    # decrypt_and_parse_user_profile(ciphertext, random_aes_key)
