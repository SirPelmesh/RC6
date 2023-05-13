import math
import base64
from typing import Tuple

from variables import Variables


class Utils:
    """
    Class contains the functions necessary for encryption and decryption
    Methods
    -------
    _bytes_to_bin (bytes_string):
        Coverts bytes into binary string
    _bin_to_bytes(bin_string):
        Coverts binary string into bytes
    xor(*args):
        Performs an XOR operation
    expansion_of_bin(bit_string, length):
        Expands a bit string to the required length
    circular_shift(number, w, bits, side):
        Carries out a cyclic shift
    odd(number):
        Rounds up to the nearest odd number
    adapt_data(message, key, w, r):
        Prepares the entered data for encryption/decryption
    """

    @staticmethod
    def _bytes_to_bin(bytes_string: bytes) -> str:
        """Coverts bytes into binary string
        Parameters
        ----------
        bytes_string: bytes
        """
        output = bytearray(bytes_string)
        output = [Utils.expansion_of_bin(bin(char), 8)[2:] for char in output]
        output = ''.join(output)
        return output

    @staticmethod
    def _bin_to_bytes(bin_string: str) -> bytes:
        """Coverts binary string into bytes
        Parameters
        ----------
        bin_string: str
        """
        output = [int('0b' + bin_string[block * 8: (block + 1) * 8], 2) for block in range(int(len(bin_string) / 8))]
        output = bytes(output)
        return output

    @staticmethod
    def xor(*args) -> int:
        """Performs an XOR operation"""
        length = len(bin(max(args))[2:])
        args = [Utils.expansion_of_bin(bin(arg), length)[2:] for arg in args]
        output = '0b'
        for x in range(length):
            counter = 0
            for arg in args:
                counter += int(arg[x])
            output += str(counter % 2)
        return int(output, 2)

    @staticmethod
    def expansion_of_bin(bit_string: str, length: int) -> str:
        """Expands a bit string to the required length
        Parameters
        ----------
        bit_string: str
        length: int
        """
        output = bit_string
        while len(output) != length + 2:
            output = output[:2] + '0' + output[2:]
        return output

    @staticmethod
    def circular_shift(number: int, w: int, bits: int, side: str) -> int:
        """Carries out a cyclic shift
        Parameters
        ----------
        number: int
        w: int
        bits: int
        side: str
        """
        bin_string = Utils.expansion_of_bin(bin(number), w)
        bits %= w
        bin_string = bin_string[2:]
        if side == 'L':
            return int('0b' + bin_string[bits:] + bin_string[:bits], 2)
        if side == 'R':
            return int('0b' + bin_string[-bits:] + bin_string[:-bits], 2)

    @staticmethod
    def odd(number: int) -> int:
        """Rounds up to the nearest odd number
        Parameters
        ----------
        number: int
        """
        if int(number) % 2 != 0:
            return int(number)
        else:
            return int(number) + 1

    @staticmethod
    def adapt_data(message: [str, bytes, bytearray], key: str, w: int, r: int) -> [str, str]:
        """Prepares the entered data for encryption/decryption
        Parameters
        ----------
        message: str, bytes, bytearray
        key: str
        w: int
        r: int
        """
        if isinstance(message, str):
            message = base64.b64encode(bytes(message, 'utf-8'))
        elif isinstance(message, bytes):
            message = base64.b64encode(message)
        elif isinstance(message, bytearray):
            message = base64.b64encode(bytes(message))
        else:
            print("Message must be a string, bytes ot bytearray!")
            raise TypeError
        if isinstance(key, str):
            key = base64.b64encode(bytes(key, 'utf-8'))
        else:
            print("Key must be a string!")
            raise TypeError
        if not (isinstance(r, int) and r >= 0):
            print("The number of rounds 'r' must be non-negative integer!")
            raise TypeError
        if not (w in Variables.Pw.keys()):
            print("The block 'w' must be 16, 32 or 64!")
            raise TypeError
        bin_message = Utils._bytes_to_bin(message)
        bin_key = Utils._bytes_to_bin(key)
        return bin_message, bin_key

    @staticmethod
    def bin_to_string(bin_string):
        string = str(base64.b64decode(Utils._bin_to_bytes(bin_string)))[2:-1].strip()
        return string
