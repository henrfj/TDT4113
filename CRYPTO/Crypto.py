import crypto_utils as cu


# --------------CIPHER ALGORITHMS--------------


class Cipher:
    """Super-class of the different cyphering algorithms"""

    alphabet = list(
        r" !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~")

    def __init__(self):
        """General init of ciphers"""
        self.alphabet_size = 95

    def encode(self, text, key):
        """dummy"""
        return None

    def decode(self, text, key):
        """dummy"""
        return None

    def verify(self, decoded, encoded, key):
        return decoded == self.decode(
            encoded, key) and encoded == self.encode(decoded, key)

    def generate_keys(self, key):
        """for distributing keys to sender and receiver (used by some algorithms)"""
        return None


class Caesar(Cipher):
    """The Caesar algorithm"""

    def encode(self, text, key):
        """Encodes by adding a simple integer key"""
        encoded_text = ""
        for symbol in text:
            i = self.alphabet.index(symbol)
            j = (i + key) % self.alphabet_size
            encoded_text += self.alphabet[j]
        return encoded_text

    def decode(self, text, key):
        """As there is only 95 possible letters, double encoding (where sum of
         keys is 95) will lead to the same clear text result"""
        return self.encode(text, (self.alphabet_size - key) % self.alphabet_size)

    def __str__(self):
        return "Caesar algorithm"


class Multi(Cipher):
    """The multiplication algorithm. Only possible to decode if the key has a modulo inverse;
    which is only possible if the encrypted letters are 1-1 (two letters cannot be encoded to the same letter)"""

    def encode(self, text, key):
        """encoding by multiplying a integer key. Needs to be modulo inversible"""
        encoded_text = ""
        for symbol in text:
            i = self.alphabet.index(symbol)
            j = (i * key) % self.alphabet_size
            encoded_text += self.alphabet[j]
        return encoded_text

    def decode(self, text, key):
        """decoding by a modulo inversed key"""
        

    def generate_keys(self, key):
        """The receiver needs the modulo inverse key of the sender"""
        return cu.modular_inverse(key, self.alphabet_size)

# --------------PERSONS/AGENTS--------------


class Person:
    """Super-class for different actors"""

    def __init__(self, key, cipher):
        self.key = key
        self.cipher = cipher

    def set_key(self, key):
        """for updating the key"""
        self.key = key

    def get_key(self):
        """for getting the key"""
        return self.key

    def operate_cipher(self, text):
        """dummy"""


class Sender(Person):
    """For generating cypher text"""

    def operate_cipher(self, text):
        """using the cipher algorithm clear->cipher"""
        return self.cipher.encode(text, self.key)


class Receiver(Person):
    """For generating clear text"""

    def operate_cipher(self, text):
        """using the cipher algorithm cipher->clear"""
        return self.cipher.decode(text, self.key)


class Hacker(Receiver):
    """For forcefully generating best possible clear text"""


# TESTING GROUNDS -----------------------------------------------
def tester(text, key, cipher):
    print("---------------------\n", "Original:", text)
    key1 = 88
    sender1 = Sender(key1, cipher)
    receiver1 = Receiver(key1, cipher)

    encrypt = sender1.operate_cipher(text)
    print("Sender encrypts using", key1, ":", encrypt)

    decrypt = receiver1.operate_cipher(encrypt)
    print("Receiver encrypts using", key, ":", decrypt)

    if cipher.verify(decrypt, encrypt, key):
        print(cipher, "works!")
    else:
        print(cipher, "workn'th!")


def main():
    """testing and executing"""
    text = "Holy mother, that is some real yankee zulu shit!"
    tester(text, 88, Caesar())


main()
