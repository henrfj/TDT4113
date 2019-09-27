"""Crypto module includes several cipher-algorithms
 as well as actors to execute send-receive operations"""
import crypto_utils as cu


# --------------CIPHER ALGORITHMS--------------


class Cipher:
    """Super-class of the different cyphering algorithms;
    contains dummy-methods for all subclasses"""

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

    def decode(self, text, key):
        """dummy"""

    def generate_keys(self, key):
        """for distributing keys to sender and receiver (used by some algorithms)"""

    def verify(self, decoded, encoded, key):
        """returns True if the algorithm works, false otherwise"""
        return decoded == self.decode(
            encoded, key) and encoded == self.encode(decoded, key)

    def __str__(self):
        return "Unnamed algorithm"


class Caesar(Cipher):
    """The Caesar algorithm"""

    def __init__(self, ):
        """adding the 'possible keys' attribute"""
        super().__init__()
        self.possible_keys = [a for a in range(0, self.alphabet_size)]

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
    """The multiplication algorithm.
    Only possible to decode if the key has a modulo inverse;
    which is only possible if the encrypted letters
    are 1-1 (two letters cannot be encoded to the same letter)"""

    def __init__(self, ):
        """adding the 'possible keys' attribute"""
        super().__init__()
        self.possible_keys = []
        for i in range(0, self.alphabet_size):
            if self.generate_keys(
                    i) != -1:   # There is no modulo inverse for the key: it is not a possible key
                self.possible_keys.append(i)

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
        # print("This key is invalid, no modulo inverse")
        return -1

    def __str__(self):
        return "Multi-algorithm"


class Affine(Cipher):
    """uses algorithm caesar and multi with a tuple of two keys"""

    def __init__(self, ):
        """adding the 'possible keys' attribute"""
        super().__init__()
        self.possible_keys = []
        for i in range(0, self.alphabet_size):
            for j in range(0, self.alphabet_size):
                if Multi().generate_keys(i) != -1:
                    self.possible_keys.append((i, j))

    def encode(self, text, key):
        """The key is a tuple now, k[0] is caesar key and k[1] is multi-key"""
        return Caesar().encode(Multi().encode(text, key[1]), key[0])

    def decode(self, text, key):
        """important to decode in the opposite order of the encoding"""
        return Multi().decode(Caesar().decode(text, key[0]), key[1])

    def __str__(self):
        return "Affine algorithm"


class Unbreakable(Cipher):
    """Uses a word as key"""

    def __init__(self, ):
        """adding the 'possible keys' attribute"""
        super().__init__()
        file = open("english_words.txt", "r")
        words = file.read()
        file.close()
        self.possible_keys = words.split("\n")
        self.possible_keys.pop()

    def encode(self, text, key):
        """key is now a word"""
        t_block = cu.blocks_from_text(text, 1)
        k_block = cu.blocks_from_text(key, 1)
        while len(k_block) < len(t_block):
            k_block += k_block
        for i in range(len(t_block)):
            t_block[i] = (t_block[i] - 32 + k_block[i] - 32) % self.alphabet_size
            t_block[i] = self.alphabet[t_block[i]]
        return "".join(t_block)

    def decode(self, text, key):
        """key is now the the 'opposite' word of the original encoding key"""
        return self.encode(text, self.generate_keys(key))

    def generate_keys(self, key):
        """return the opposite of the key"""
        k = cu.blocks_from_text(key, 1)
        for i in range(len(k)):
            k[i] = (self.alphabet_size - ((k[i] - 32) % self.alphabet_size))
            k[i] = self.alphabet[k[i]]
        return "".join(k)

    def __str__(self):
        return "Unbreakable algorithm"


class RSA(Cipher):
    """The sender and receiver doesn't  need to share keys"""

    def encode(self, text, key):
        """key here is the public key of the receiver, a tuple (n,e)"""
        t_block = cu.blocks_from_text(text, 1)
        for i in range(len(t_block)):
            t_block[i] = pow(t_block[i], key[1], key[0])
        return t_block

    def decode(self, text, key):
        """key here is the receivers own private key, a tuple (n,d).
        'text' is in this case a list of encrypted integers"""
        for i in range(len(text)):
            text[i] = pow(text[i], key[1], key[0])
        return cu.text_from_blocks(text, 8)

    def __str__(self):
        return "RSA algorithm"

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

    def __init__(self, key, cipher):
        """The receiver needs a public key for RSA"""
        self.public_key = None
        super().__init__(key, cipher)

    def operate_cipher(self, text):
        """using the cipher algorithm cipher->clear"""
        return self.cipher.decode(text, self.key)

    def generate_rsa_keys(self):
        """public key used by senders"""
        p_prime = cu.generate_random_prime(8)
        q_prime = cu.generate_random_prime(8)
        while p_prime == q_prime:
            q_prime = cu.generate_random_prime(8)

        n_prime = p_prime * q_prime
        _phi = (p_prime - 1) * (q_prime - 1)

        e_prime = cu.random.randint(3, _phi - 1)
        d_prime = cu.modular_inverse(e_prime, _phi)
        while not d_prime:    # It is important that e has a modulo inverse based on _phi
            e_prime = cu.random.randint(3, _phi - 1)
            d_prime = cu.modular_inverse(e_prime, _phi)

        self.key = (n_prime, d_prime)
        self.public_key = (n_prime, e_prime)


class Hacker(Receiver):
    """For forcefully generating best possible clear text"""

    def hacking(self, encoded):
        """Uses brute force to fin best matching english sentence using all possible keys"""
        results = {}
        file = open("english_words.txt", "r")
        english_words = file.read().split("\n")
        file.close()

        for key in self.cipher.possible_keys:
            self.key = key
            decoded = self.operate_cipher(encoded)
            for word in decoded.split(" "):
                if word.isalpha() and word in english_words:
                    try:
                        results[decoded] += 1
                    except KeyError:
                        results[decoded] = 1

        return self.biggest_key(results)

    @staticmethod
    def biggest_key(dic):
        """returns key with biggest integer value in a dictionary"""
        biggest_value = 0
        key = ""
        for k in dic:
            if dic[k] > biggest_value:
                key = k
                biggest_value = dic[k]
        return key

# TESTING GROUNDS -----------------------------------------------


def tester(text, key, cipher):
    """test basic algorithms and hackers"""
    print(
        "----------------------------------------------------\n" +
        "Original:",
        text)
    sender = Sender(key, cipher)
    receiver = Receiver(key, cipher)
    hacker = Hacker(None, cipher)

    encrypt = sender.operate_cipher(text)
    print("Sender encrypts using", key, ":", encrypt)

    hacked = hacker.hacking(encrypt)
    print("--> Hacker tried hacking; ", hacked)

    decrypt = receiver.operate_cipher(encrypt)
    print("Receiver encrypts using", key, ":", decrypt)

    if decrypt == text:
        print("-->", cipher, "works!")
    else:
        print("-->", cipher, "workn'th!")


def rsa_tester(text, rsa):
    """Can only test the rsa cipher"""
    print(
        "----------------------------------------------------\n" +
        "Original:",
        text)
    receiver = Receiver(None, rsa)
    receiver.generate_rsa_keys()
    sender = Sender(receiver.public_key, rsa)

    encrypt = sender.operate_cipher(text)
    print("Sender encrypts using (n, e)", receiver.public_key, ":", encrypt)

    decrypt = receiver.operate_cipher(encrypt)
    print("Receiver encrypts using (n, d)", receiver.key, ":", decrypt)

    if decrypt == text:
        print("-->", rsa, "works!")
    else:
        print("-->", rsa, "workn'th!")


def main():
    """testing and executing"""

    text = "we are the world/we are the children"

    tester(text, 199, Caesar())
    tester(text, 4, Multi())
    tester(text, (27, 13), Affine())
    tester(text, "flag", Unbreakable())
    rsa_tester(text, RSA())

    # Set>liste: O(1) access time

main()
