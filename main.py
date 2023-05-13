from random_data import RandomData
from rc6 import RC6
from utils import Utils
import pandas as pd
import random


def test():
    """ Function for testing the RC6 algorithm
    and the program's reaction to unsupported types """
    list_message = [
        "Shall we drink a tea?",  # string
        bytes(RandomData.generate_string(length=10), "utf-8"),  # bytes
        bytearray(bytes(RandomData.generate_string(length=10), "utf-8")),  # bytearrey
        2002,  # integer
        RandomData.generate_string(length=10),  # string
    ]
    list_key = [
        "With donuts!",  # string
        RandomData.generate_string(length=5),
        RandomData.generate_string(length=1),
        2002,  # integer
        RandomData.generate_string(length=10)
    ]
    list_w = [16, 32, 64, 1, "block"]
    list_r = [20, 30, 1, -1, "round"]
    for i in range(len(list_w)):
        print('================START================')
        message = list_message[i]
        key = list_key[i]
        w = list_w[i]  # the value may be 16, 32 or 64
        r = list_r[i]  # the recommended minimum number of rounds = 20
        print(f"RC6 m:{message}/k:{key}/w:{w}/r:{r}")
        try:
            encryption_bin_message = RC6.encode(message, key, w=w, r=r)  # encoding
            decryption_bin_message = RC6.decode(encryption_bin_message, key, w=w, r=r)  # decoding
            print(f"MESSAGE:{message}")
            print(f"KEY: {key}")
            print(f"ENCRIPTION BIN MESSAGE: {encryption_bin_message}")
            print(f"DECRIPTION BIN MESSAGE: {decryption_bin_message}")
            print(f"HIDDEN MESSAGE: {Utils.bin_to_string(decryption_bin_message)}")
        except Exception:
            continue


def avalanche_effect_text():
    """Founding d, l and average lambda for text based avalanche effect """
    print('================START================')
    result = 0
    df = pd.DataFrame()
    start_message = Utils._bytes_to_bin(bytes(RandomData.generate_string(10), "utf-8"))
    key = RandomData.generate_string(5)
    arr_bin_message1 = arr_bin_message2 = list(start_message)
    num = 100  # number of rounds
    for r in range(num):
        i_bit = random.randint(0, len(start_message) - 1)
        arr_bin_message1[i_bit] = "1"
        bin_message1 = "".join(arr_bin_message1)
        arr_bin_message2[i_bit] = "0"
        bin_message2 = "".join(arr_bin_message2)
        str_message1 = Utils._bin_to_bytes(bin_message1)
        str_message2 = Utils._bin_to_bytes(bin_message2)
        w = 32
        d = 0
        encryption_bin_message1 = RC6.encode(str_message1, key, w=w, r=r)
        encryption_bin_message2 = RC6.encode(str_message2, key, w=w, r=r)
        for j in range(len(encryption_bin_message1)):
            if encryption_bin_message1[j] != encryption_bin_message2[j]:
                d += 1
        l = d / (w * 8)
        result = result + l
        string1 = {"#": r, "message": str_message1, "key": key, "d": d, "l": l}
        string2 = {"message": str_message2}
        df = df._append(string1, ignore_index=True)
        df = df._append(string2, ignore_index=True)
    print(f"Average lambda(text): {result / num}")
    return df


def avalanche_effect_key():
    """Founding d, l and average lambda for key based avalanche effect """
    print('================START================')
    result = 0
    df = pd.DataFrame()
    message = RandomData.generate_string(10)
    start_key = Utils._bytes_to_bin(bytes(RandomData.generate_string(5), "utf-8"))
    arr_bin_key1 = arr_bin_key2 = list(start_key)
    num = 100  # number of rounds
    for r in range(num):
        i_bit = random.randint(0, len(start_key) - 1)
        arr_bin_key1[i_bit] = "1"
        str_key1 = str(Utils._bin_to_bytes("".join(arr_bin_key1)).strip())
        arr_bin_key2[i_bit] = "0"
        str_key2 = str(Utils._bin_to_bytes("".join(arr_bin_key2)).strip())
        w = 32
        d = 0
        encryption_bin_message1 = RC6.encode(message, str_key1, w=w, r=r)
        encryption_bin_message2 = RC6.encode(message, str_key2, w=w, r=r)
        for j in range(len(encryption_bin_message1)):
            if encryption_bin_message1[j] != encryption_bin_message2[j]:
                d += 1
        l = d / (w * 8)
        string1 = {"#": r, "message": message, "d": d, "key": str_key1, "l": l}
        string2 = {"key": str_key2}
        df = df._append(string1, ignore_index=True)
        df = df._append(string2, ignore_index=True)
        result = result + l
    print(f"Average lambda(key): {result / num}")
    return df


def collect_data_in_xlsx():
    """ Helps to collect all the avalanche effect data to .xlsx file """
    df1 = avalanche_effect_text()
    df2 = avalanche_effect_key()
    df3 = pd.concat([df1["l"], df2["l"]], axis=1, join="inner").dropna()
    with pd.ExcelWriter('output.xlsx') as writer:
        df1.to_excel(writer, sheet_name='message', index=False)
        df2.to_excel(writer, sheet_name='key', index=False)
        df3.to_excel(writer, sheet_name='message and key', index=False)


def start():
    """ The main function """
    message = input("Enter your message: ")
    key = input("Enter your key: ")
    w = int(input("Block length (16, 32 or 64): "))
    r = int(input("Number of rounds (recommended number - 20): "))
    print(f"RC6 m:{message}/k:{key}/w:{w}/r:{r}")
    encryption_bin_message = RC6.encode(message, key, w=w, r=r)  # encoding
    decryption_bin_message = RC6.decode(encryption_bin_message, key, w=w, r=r)  # decoding
    print(f"MESSAGE:{message}")
    print(f"KEY: {key}")
    print(f"ENCRIPTION BIN MESSAGE: {encryption_bin_message}")
    print(f"DECRIPTION BIN MESSAGE: {decryption_bin_message}")
    print(f"HIDDEN MESSAGE: {Utils.bin_to_string(decryption_bin_message)}")


if __name__ == "__main__":
    start()
