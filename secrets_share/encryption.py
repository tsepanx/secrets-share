# from builtins import bytes
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


def encode_b64(string):
    return base64.b64encode(string).decode("utf-8")


def decode_b64(string):
    return base64.b64decode(string.encode("utf-8"))


def password_to_key(password):
    """
    Use SHA-256 over our password to get a proper-sized AES key.
    This hashes our password into a 256 bit string.
    """
    return SHA256.new(password).digest()


def make_initialization_vector():
    """
    An initialization vector (IV) is a fixed-size input to a cryptographic
    primitive that is typically required to be random or pseudorandom.
    Randomization is crucial for encryption schemes to achieve semantic
    security, a property whereby repeated usage of the scheme under the
    same key does not allow an attacker to infer relationships
    between segments of the encrypted message.
    """
    return Random.new().read(AES.block_size)


def encrypt(string, password):
    def pad_string(string, chunk_size=AES.block_size):
        """
        Pad string the peculirarity that uses the first byte
        is used to store how much padding is applied
        """
        assert chunk_size <= 256, 'We are using one byte to represent padding'
        to_pad = (chunk_size - (len(string) + 1)) % chunk_size
        return bytes([to_pad]) + string + bytes([0] * to_pad)

    string = string.encode()
    password = password.encode()

    key = password_to_key(password)
    IV = make_initialization_vector()
    encryptor = AES.new(key, AES.MODE_CBC, IV)

    # store the IV at the beginning and encrypt
    result = IV + encryptor.encrypt(pad_string(string))
    return encode_b64(result)


def decrypt(string, password):
    def unpad_string(string):
        to_pad = string[0]
        return string[1:-to_pad]

    string = decode_b64(string)

    password = password.encode()
    key = password_to_key(password)

    # extract the IV from the beginning
    IV = string[:AES.block_size]
    decryptor = AES.new(key, AES.MODE_CBC, IV)

    string = decryptor.decrypt(string[AES.block_size:])
    result = unpad_string(string)
    return result.decode()
    # return string


if __name__ == "__main__":
    a = encrypt('text', '1234')
    print(a)

    b = decrypt(a, '1234')
    print(b)