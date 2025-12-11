from secrets import token_bytes
from typing import Tuple


def random_key(length: int) -> int:
    """
    Docstring for random_key
    生成一个 length 长度的 bytes 随机字符串 tb
    把生成的 bytes 转换成 位字符串 并返回
    :param length: Description
    :type length: int
    :return: Description
    :rtype: int
    """
    tb: bytes = token_bytes(length)
    return int.from_bytes(tb, "big")


def encrypt(original: str) -> Tuple[int, int]:
    """
    Docstring for encrypt
    加密过程：
    将原始字符串 转换成 utf-8 序列
    生成一个随机 位序列 与该序列长度相同
    将该序列转换成int 位序列
    利用异或原理加解密序列
    A ^ B = C
    C ^ A = B
    C ^ B = A
    :param original: Description
    :type original: str
    :return: Description
    :rtype: Tuple[int, int]
    """
    original_bytes: bytes = original.encode()
    dummy: int = random_key(len(original_bytes))
    original_key: int = int.from_bytes(original_bytes, "big")
    encrypted: int = original_key ^ dummy  # XOR
    return dummy, encrypted


def decrypt(key1: int, key2: int) -> str:
    """
    Docstring for decrypt
    加密过程：
    key1 ^ key2 = original_key
    int.to_bytes 把 int 转换成 bytes
    整除(//) 8 操作前必须给解密数据长度加上7， 以确保能“向上舍入”
    避免出现边界差一 (off-by-one)错误
    :param key1: Description
    :type key1: int
    :param key2: Description
    :type key2: int
    :return: Description
    :rtype: str
    """
    decrypted: int = key1 ^ key2  # XOR
    temp: bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, "big")
    return temp.decode()


if __name__ == "__main__":
    key1, key2 = encrypt("One Time Pad!")
    result: str = decrypt(key1, key2)
    print(result)
