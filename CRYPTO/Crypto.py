import crypto_utils as cu


# --------------CIPHER ALGORITHMS--------------


class Cipher:
    """Super-class of the different cyphering algorithms"""

    def __init__(self):
        """General init of ciphers"""
        self.alphabet_size = 95
        self.alphabet = list(
            r"!\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~")

    def encode(self):
        """dummy"""

    def decode(self):
        """dummy"""


class Caesar(Cipher):
    """The Caesar algorithm"""



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

    def operate_cipher(self):
        """dummy"""


class Sender(Person):
    """For generating cypher text"""

    def operate_cipher(self):
        """using the cipher algorithm clear->cipher"""


class Receiver(Person):
    """For generating clear text"""

    def operate_cipher(self):
        """using the cipher algorithm cipher->clear"""


class Hacker(Receiver):
    """For forcefully generating best possible clear text"""

