from enum import IntEnum
from typing import Tuple, List

Nucleotide = IntEnum("Nucleotide", ("A", "C", "G", "T"))
Codon = Tuple[Nucleotide, Nucleotide, Nucleotide]  # type alias for codons
Gene = List[Codon]  # type alias for gens


def string_to_gen(s: str) -> Gene:
    gene: Gene = []
    for i in range(0, len(s), 3):
        if (i + 2) >= len(s):
            return gene
        codon: Codon = (Nucleotide[s[i]], Nucleotide[s[i + 1]], Nucleotide[s[i + 2]])
        gene.append(codon)
    return gene


def linear_contains(gene: Gene, key_codon: Codon) -> bool:
    for codon in gene:
        if codon == key_codon:
            return True
    return False


def binary_contains(gene: Gene, key_codon: Codon) -> bool:
    low: int = 0
    high: int = len(gene) - 1
    while low <= high:
        mid = (low + high) // 2
        if gene[mid] > key_codon:
            high = mid - 1
        elif gene[mid] < key_codon:
            low = mid + 1
        else:
            return True
    return False


if __name__ == "__main__":
    gene_str: str = "ACGTGGCTCTCTAACGTACGTACGTACGGGGTTTATATATACCCTAGGACTCCCTTT"
    my_gene: Gene = string_to_gen(gene_str)

    acg: Codon = (Nucleotide.A, Nucleotide.C, Nucleotide.G)
    gat: Codon = (Nucleotide.G, Nucleotide.A, Nucleotide.T)

    print(linear_contains(my_gene, acg))  # print(acg in my_gene)
    print(linear_contains(my_gene, gat))  # print(gat in my_gene)

    my_sorted_gene: Gene = sorted(my_gene)
    print(binary_contains(my_sorted_gene, acg))
    print(binary_contains(my_sorted_gene, gat))
