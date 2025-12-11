from textwrap import dedent


class CompressedGene:
    """
    Docstring for CompressedGene
    将 dna 序列压缩成二进制序列
    读取 ACT 时:
    原始序列为 1
    1. 压缩 第一位 A: 1 << 2 |= 0b00 => 100 |= 0b00 => 100
    2. 压缩 第二位 C: 100 << 2 | 0b01 => 10000 |= 0b00 => 1_00_01
    3. 压缩 第二位 C: 1_00_01 << 2 | 0b11 => 1_00_01_00 |= 0b11 => 1_00_01_11
    解析时:
    做位运算从最后一位开始，即 1_00_01_11 & 0b11 , 得到的结果顺序与读取相反， 因此最后要做一次序列翻转 `[::-1]`
    每次右移2位拿到结果， 因此步进为2， 舍去最高位的 1， 因此长度要减 1，构成序列的表达式为
    `for i in range(0, compress.bit_string.bit_length() - 1, 2)`

    python 中没有 switch ， 选择 `if elif` 与 map 查找做条件判断 需要运行一次性能测试
    """

    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        self.bit_string: int = 1  # start with sentinel
        for nucleotide in gene.upper():
            self.bit_string <<= 2  # shift left two bits
            if nucleotide == "A":
                self.bit_string |= 0b00
            elif nucleotide == "C":
                self.bit_string |= 0b01
            elif nucleotide == "G":
                self.bit_string |= 0b10
            elif nucleotide == "T":
                self.bit_string |= 0b11
            else:
                raise ValueError("Invalid Nucleotide: {}".format(nucleotide))

    def decompress(self) -> str:
        gene: str = ""
        for i in range(
            0, self.bit_string.bit_length() - 1, 2
        ):  # -1 to exclude sentinel
            bits: int = self.bit_string >> i & 0b11
            if bits == 0b00:  # A
                gene += "A"
            elif bits == 0b01:  # C
                gene += "C"
            elif bits == 0b10:  # G
                gene += "G"
            elif bits == 0b11:  # T
                gene += "T"
            else:
                raise ValueError("Invalid bits:{}".format(bits))
        return gene[::-1]  # [::-1] reverses string by slicing backward

    def __str__(self) -> str:
        return self.decompress()


if __name__ == "__main__":
    from sys import getsizeof

    original: str = (
        "TAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATATAGGGATTAACCCGTTATATATATATAGCCATGATCGATATTA"
        * 100
    )

    compressed: CompressedGene = CompressedGene(original)
    print(
        dedent(
            f"""
            orginal is {getsizeof(original)} bytes,
            compressed is {getsizeof(compressed.bit_string)} bytes,
            compress rate { (1 - getsizeof(compressed.bit_string) / getsizeof(original)) * 100 : .2f}% 
            """
        )
    )

    print(
        f"original and decompressed art the same : {original == compressed.decompress()}"
    )
