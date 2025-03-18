"""Data Types used in type hinting"""

from typing import Dict, List, NamedTuple, TypedDict


class NucleotideCount(TypedDict):
    a: int
    t: int
    g: int
    c: int


class NucleotideCounts(TypedDict):
    a: int
    b: int
    c: int
    d: int


class Palindrome(NamedTuple):
    sequence: str = ""
    longest: int = 0


class K_MERS(TypedDict):
    k_mer_n2_count: Dict[str, int]
    k_mer_n3_count: Dict[str, int]
    k_mer_n4_count: Dict[str, int]
    k_mer_n5_count: Dict[str, int]


class DNASequence(NamedTuple):
    id: int
    adenine_count: int = 0
    thymine_count: int = 0
    guanine_count: int = 0
    cytosine_count: int = 0
    palindrome: Palindrome = {}
    motifs: Dict[str, int] = {}
    k_mers: K_MERS = {}


class SequenceStatistics(TypedDict):
    total_adenine_count: int = 0
    total_thymine_count: int = 0
    total_guanine_count: int = 0
    total_cytosine_count: int = 0
    total_sequences_count: int = 0
    invalid_sequences_count: int = 0
    total_k_mer_count_2: Dict[str, int] = {}
    total_k_mer_count_3: Dict[str, int] = {}
    total_k_mer_count_4: Dict[str, int] = {}
    total_k_mer_count_5: Dict[str, int] = {}
    palidromes: List[Palindrome]
    dna_sequences: List[DNASequence] = []
