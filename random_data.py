import random


class RandomData:
    """
    Generates a string of particular length
    """
    @staticmethod
    def generate_string(length: int) -> str:
        string = ""
        alphabet = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
        for i in range(length):
            string = string + random.choice(alphabet)
        return string
