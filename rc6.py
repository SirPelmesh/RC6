import math
from utils import Utils
from variables import Variables


class RC6:
    """ Class that performs encryption / decryption using the RC6 algorithm
    Methods
    -------
    _generate_key_table(key, w, r):
        Generates an array of keys
    _encode_bin_block(message, w, r):
        Encodes blocks using the RC6 algorithm
    _decode_bin_block(message, w, r):
        Decodes blocks using the RC6 algorithm
    encode(message, key, w, r):
        Encodes message using the RC6 algorithm
    decode(message, key, w, r):
        Decodes message using the RC6 algorithm
    """

    @staticmethod
    def _generate_key_table(key: str, w: int, r: int):
        """Generates an array of keys
        Parameters
        ----------
        key: str
        w: int
        r: int
        """
        mod = Variables.mod

        """Key extension"""
        while len(key) % w != 0:
            key = key + '0'

        """Constant initialization"""
        f = int(Variables.Qw[w], 16)  # converting from the 16th number system to the 10th
        e = int(Variables.Pw[w], 16)
        Q = Utils.odd((f - 1) * mod)  # calculation of constants depending on w
        P = Utils.odd((e - 2) * mod)

        """L-array initialization"""
        c = int(len(key) / w)  # number of blocks in the key
        L = [key[i * w: (i + 1) * w] for i in range(c)]  # division into blocks
        L = [int('0b' + i, 2) for i in L]  # convert blocks to integers

        """S-array initialization"""
        S = [P]
        Variables.t = t = 2 * (r + 2)
        for i in range(1, t):
            S.append((S[i - 1] + Q) % mod)

        """Key mixing"""
        A = B = i = j = 0
        n = 3 * max(c, t)
        for _ in range(1, n):
            A = S[i] = Utils.circular_shift((S[i] + A + B) % mod, w, 3, 'L')
            B = L[j] = Utils.circular_shift((L[j] + A + B) % mod, w, (A + B) % mod, 'L')
            i = (i + 1) % t
            j = (j + 1) % c

        Variables.keys_table = S

    @staticmethod
    def _encode_bin_block(message: str, w: int, r: int) -> str:
        """Encodes blocks using the RC6 algorithm
        Parameters
        ----------
        message: str
        w: int
        r: int
        """
        mod = Variables.mod
        S = Variables.keys_table

        A = int('0b' + message[0:w], 2)  # division into blocks
        B = int('0b' + message[(w):(2 * w)], 2)
        C = int('0b' + message[(2 * w):(3 * w)], 2)
        D = int('0b' + message[(3 * w):(4 * w)], 2)

        B = (B + S[0]) % mod
        D = (D + S[1]) % mod
        for i in range(1, r):
            t = Utils.circular_shift((B * ((2 * B) % mod + 1) % mod) % mod, w, int(math.log(w)), 'L')
            u = Utils.circular_shift((D * ((2 * D) % mod + 1) % mod) % mod, w, int(math.log(w)), 'L')
            A = (Utils.circular_shift(Utils.xor(A, t), w, u, 'L') + S[2 * i]) % mod
            C = (Utils.circular_shift(Utils.xor(C, u), w, t, 'L') + S[2 * i + 1]) % mod
            A, B, C, D = B, C, D, A

        A = (A + S[Variables.t - 2]) % mod
        C = (C + S[Variables.t - 1]) % mod

        encoded_block = Utils.expansion_of_bin(bin(A), w)[2:]  # block merging
        encoded_block += Utils.expansion_of_bin(bin(B), w)[2:]
        encoded_block += Utils.expansion_of_bin(bin(C), w)[2:]
        encoded_block += Utils.expansion_of_bin(bin(D), w)[2:]

        return encoded_block

    @staticmethod
    def _decode_bin_block(message: str, w: int, r: int) -> str:
        """Decodes blocks using the RC6 algorithm
        Parameters
        ----------
        message: str
        w: int
        r: int
        """
        mod = Variables.mod
        S = Variables.keys_table

        A = int('0b' + message[0:w], 2)
        B = int('0b' + message[w:(2 * w)], 2)
        C = int('0b' + message[(2 * w):(3 * w)], 2)
        D = int('0b' + message[(3 * w):(4 * w)], 2)

        C = (C - S[Variables.t - 1]) % mod
        A = (A - S[Variables.t - 2]) % mod

        for j in range(r - 1, 0, -1):
            i = j
            A, B, C, D = D, A, B, C

            u = Utils.circular_shift((D * ((2 * D) % mod + 1) % mod) % mod, w, int(math.log(w)), 'L')
            t = Utils.circular_shift((B * ((2 * B) % mod + 1) % mod) % mod, w, int(math.log(w)), 'L')
            C = Utils.xor(Utils.circular_shift((C - S[2 * i + 1]) % mod, w, t % w, 'R'), u)
            A = Utils.xor(Utils.circular_shift((A - S[2 * i]) % mod, w, u % w, 'R'), t)

        B = (B - S[0]) % mod
        D = (D - S[1]) % mod

        decoded_block = Utils.expansion_of_bin(bin(A), w)[2:]
        decoded_block += Utils.expansion_of_bin(bin(B), w)[2:]
        decoded_block += Utils.expansion_of_bin(bin(C), w)[2:]
        decoded_block += Utils.expansion_of_bin(bin(D), w)[2:]

        return decoded_block

    @staticmethod
    def encode(message: [str, bytes, bytearray], key: str, w: int, r: int) -> str:
        """
        Encodes message using the RC6 algorithm
        Parameters
        ----------
        message: str, bytes, bytearray
        key: str
        w: int
        r: int
        """
        message, key = Utils.adapt_data(message, key, w, r)
        Variables.mod = 2 ** w
        RC6._generate_key_table(key, w=w, r=r)
        size = len(message)
        size = Utils.expansion_of_bin(bin(size), 64)
        message = size[2:] + message

        while len(message) % (4 * w) != 0:
            message += '0'
        message = [message[(block * 4 * w): ((block + 1) * 4 * w)]
                   for block in range(int(len(message) / (4 * w)))]

        encoded_message = ''
        for block in message:
            encoded_message += RC6._encode_bin_block(block, w=w, r=r)
        return encoded_message

    @staticmethod
    def decode(message: str, key: str, w: int, r: int) -> str:
        """
        Decodes message using the RC6 algorithm
        Parameters
        ----------
        message: str
        key: str
        w: int
        r: int
        """
        _, key = Utils.adapt_data(message=message, key=key, w=w, r=r)
        RC6._generate_key_table(key, w=w, r=r)
        message = [message[x * w * 4: (x + 1) * w * 4]
                   for x in range(int(len(message) / (w * 4)))]

        decoded_message = ''
        for block in message:
            decoded_message += RC6._decode_bin_block(block, w=w, r=r)

        size = int('0b' + decoded_message[:64], 2)
        decoded_message = decoded_message[64: 64 + size]
        return decoded_message
