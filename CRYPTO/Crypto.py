import crypto_utils as cu


# --------------CIPHER ALGORITHMS--------------


class Cipher:
    """Super-class of the different cyphering algorithms"""

    alphabet = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*',
                '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5',
                '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a',
                'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                'x', 'y', 'z', '{', '|', '}', '~']

    def __init__(self):
        """General init of ciphers"""
        self.alphabet_size = len(self.alphabet)

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

    def __str__(self):
        return "Unnamed algorithm"


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
        return self.encode(
            text, (self.alphabet_size - key) %
            self.alphabet_size)

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
        """decoding by a modulo inversed key, we assume he has one from \"generate key\" function"""
        return self.encode(text, self.generate_keys(key))

    def generate_keys(self, key):
        """The receiver needs the modulo inverse key of the sender"""
        if cu.modular_inverse(key, self.alphabet_size):
            return cu.modular_inverse(key, self.alphabet_size)
        print("This key is invalid, no modulo inverse")
        return 0

    def __str__(self):
        return "Multi-algorithm"


class Affine(Cipher):
    """uses algorithm caesar and multi with a tuple of two keys"""

    def encode(self, text, key):
        """The key is a tuple now, k[0] is caesar key and k[1] is multi-key"""
        return Caesar().encode(Multi().encode(text, key[1]), key[0])

    def decode(self, text, key):
        """important to decode in the opposite order of the encoding"""
        return Multi().decode(Caesar().decode(text, key[0]), key[1])

    def __str__(self):
        return "Affine algorithm"
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
    print(
        "----------------------------------------------------\n" +
        "Original:",
        text)
    sender = Sender(key, cipher)
    receiver = Receiver(key, cipher)

    encrypt = sender.operate_cipher(text)
    print("Sender encrypts using", key, ":", encrypt)

    decrypt = receiver.operate_cipher(encrypt)
    print("Receiver encrypts using", key, ":", decrypt)

    if decrypt == text:
        print(cipher, "works!")
    else:
        print(cipher, "workn'th!")


def main():
    """testing and executing"""
    text = "How are we doing here mister/madam? Is there a problem?"
    tester(text, 199, Caesar())
    tester(text, 4, Multi())
    tester(text, (27, 13), Affine())


main()
