from typing import Dict, List, Set
from collections import defaultdict, Counter
from .data_types import (
    DNASequence,
    K_MERS,
    NucleotideCount,
    NucleotideCounts,
    Palindrome,
    SequenceStatistics,
)
from .markdown import MarkdownGenerator

GC_ISLAND_MOTIF = "CG"
AT_RUN_MOTIF = "AT"
MIN_PALINDROME_LENGTH = 20


def find_top_values(results: List[tuple], limit: int) -> List[tuple]:
    """
        Sorts a collection of tuples and returns the
        top limit tuples by the second tuple value

    Parameters
    ----------
    results: List[tuple]
        List of tuples
    limit: int
        Number of tuples to return

    Returns
    -------
    List(tuple)
        List of tuples
    """

    return sorted(results.items(), key=lambda item: item[1], reverse=True)[:limit]


def clean_sequence_data(
    sequences: List[str], letter_list=None, min_length=2
) -> List[str]:
    """
        Removes any sequence strings which are:
        1. Shorter than the min_length
        2. Not all letters in sequence in the letter_list

    Parameters
    ----------
    sequences: List[str]
        List of sequences
    letter_list: int
        List of letters if None = ["A", "T", "G","C"]
    min_length: int
        length threshold of sequence string
    Returns
    -------
    List(str)
        List of seqeuences strings which are
        1. Longer than the min_length
        2. All letters in sequence string in the letter_list

    """

    if letter_list is None:
        letter_list = {"A", "T", "G", "C"}
    else:
        letter_list = set(letter_list)
    clean_list = []
    for sequence in sequences:
        # Check if sequence is long enough and contains only valid letters
        if len(sequence) > min_length and all(
            letter in letter_list for letter in sequence
        ):
            # Add to clean_list if not seen before
            if sequence not in clean_list:
                clean_list.append(sequence)

    return clean_list


def find_motif(sequence: str, motif: str) -> List[str]:
    """
        Finds motifs within a sequence and returns the longest
        run of that motif

    Parameters
    ----------
    sequence: str

    motif: str
        The motif to find e.g. "GC"

    Returns
    -------
      The longest span of the motif found in a sequence

    """
    positions = [
        i for i in range(len(sequence) - 1) if sequence[i : i + len(motif)] == motif
    ]
    step = len(motif)
    pos_len = len(positions)
    longest = 0
    seen = set()
    for i in range(0, pos_len, step):
        value = sequence[i : i + step]
        if value == motif:
            longest += step
        else:
            seen.add(longest)
            longest = 0
    return max(seen) if len(seen) > 0 else 0


def reverse_complement(sequence: str) -> str:
    """
    Returns the reverse complement of a DNA sequence.

    Parameters
    ----------
    sequence: str
        A sequence string to generate its complement string from

    Returns
    -------
      The complement of the sequence string
    """
    complement = {"A": "T", "T": "A", "C": "G", "G": "C"}
    return "".join(complement[base] for base in reversed(sequence))


def find_longest_dna_palindrome(sequence, min_length=20):
    """
    Finds all palindromes in a DNA sequence of at least min_length

    Parameters
    ----------
    sequence: str
        A sequence string

    min_length: int
        The minimum length of the palindrome

    Returns
    -------
    longest: dict
      The longest palindrome dict ( {"palindrome_seq": "", "palindrome_length": 0})
    """
    longest = {"palindrome_seq": "", "palindrome_length": 0}
    seq_length = len(sequence)

    # Precompute the reverse complement of the entire sequence
    rev_complement = reverse_complement(sequence)

    # Loop over all possible subsequences starting from min_length up to the sequence length
    for length in range(min_length, seq_length + 1):
        for i in range(seq_length - length + 1):
            subseq = sequence[i : i + length]
            rev_subseq = rev_complement[
                seq_length - i - length : seq_length - i
            ]  # Get the reverse complement slice
            if subseq == rev_subseq and len(subseq) > longest["palindrome_length"]:
                longest["palindrome_seq"] = subseq
                longest["palindrome_length"] = len(subseq)

    return longest


def count_nucleotides(sequence: str) -> NucleotideCount:
    """
    Lowercases and removes leading and trailing whitespace
    from the string. Counts all unique characters in string.

    Parameters
    ----------
    sequence: str
        A sequence string

    Returns
    -------
        A defaultdict of type NucleotideCount which maps of counts
        for each unique character in the sequence string
    """
    return defaultdict(int, Counter(sequence.lower().strip()))


def update_nucleotide_counts(
    nucleotide_counts: NucleotideCounts, sequence_stats: SequenceStatistics
) -> SequenceStatistics:
    """
    Updates the SequenceStatistics nucleotide counts

    Parameters
    ----------
    nucleotide_counts: NucleotideCounts
        A set of nucleotide counts object
    sequence_stats: SequenceStatistics
        A SequenceStatistics object

    Returns
    -------
    SequenceStatistics
        An updated SequenceStatistics object.
    """
    sequence_stats["meta_data"]["adenine_count"] += nucleotide_counts.get("a", 0)
    sequence_stats["meta_data"]["thymine_count"] += nucleotide_counts.get("t", 0)
    sequence_stats["meta_data"]["guanine_count"] += nucleotide_counts.get("g", 0)
    sequence_stats["meta_data"]["cytosine_count"] += nucleotide_counts.get("c", 0)
    return sequence_stats


def create_dna_sequence_record(
    id: int,
    nucleotide_counts: NucleotideCounts,
    sequence: str,
    min_length: int,
    k_mers: K_MERS,
) -> DNASequence:
    """
    Create a DNASequence

    Parameters
    ----------
    id: int
        A unique id
    nucleotide_counts: NucleotideCounts
        A NucleotideCounts object
    sequence: str
        A DNA sequence string
    min_length: int
        A minimum length for palindromes
    k_mers:: K_MERS
        A K_MERS object of k-mer counts

    Returns
    -------
    DNASequence
        A DNASequence object.
    """
    longest_palindrome = find_longest_dna_palindrome(
        sequence=sequence, min_length=min_length
    )
    cpg_islands = find_motif(sequence=sequence, motif=GC_ISLAND_MOTIF)
    at_runs = find_motif(sequence=sequence, motif=AT_RUN_MOTIF)

    return DNASequence(
        id=id,
        adenine_count=nucleotide_counts["a"],
        thymine_count=nucleotide_counts["t"],
        guanine_count=nucleotide_counts["g"],
        cytosine_count=nucleotide_counts["c"],
        palindrome=longest_palindrome,
        motifs={"cpg_islands": cpg_islands, "tata_boxes": at_runs},
        k_mers=k_mers,
    )


def count_k_mers(sequence, number_nucleotides) -> Dict[str, int]:
    """
    Find up top 5 k-mers of a specified size in a sequence string

    Parameters
    ----------
    sequence: str
        A DNA sequence
    number_nucleotides: int
        Size of k-mer to find

    Returns
    -------
     dict
      A dictionary of the top 5 k-mers Dict[str: int]
    """
    oligo_counts = defaultdict(int)
    sequence = sequence.lower().strip()
    sequence_length = len(sequence)
    if sequence_length < number_nucleotides:
        return {}
    for i, _ in enumerate(sequence[: -(number_nucleotides - 1)]):
        key = sequence[i : i + number_nucleotides]
        oligo_counts[key] += 1
    return dict(
        sorted(oligo_counts.items(), key=lambda item: item[1], reverse=True)[:5]
    )


def update_k_mer_counts(current_counts: dict, new_counts: dict) -> Dict:
    """
    Update k-mer counts.Counts updates all counts of
    unique k-mers in string

    Parameters
    ----------
    current_counts: dict
        A dictionary of k-mer counts
    new_counts: int
        A dictionary of k-mer counts

    Returns
    -------
     dict
      A dictionary of the updated k-mer counts
    """
    current_counts = Counter(current_counts)
    current_counts.update(new_counts)
    return dict(current_counts)


def validate_sequence(sequence: str, letter_list: Set[str], min_length=2) -> List[str]:
    """
    Check a sequence string letters are all one of letters in
    letters_list and above the min_length

    Parameters
    ----------
    sequence: str
        A sequence string
    letter_list: Set[str]
        A set of unique letters e.g. ("A","T","G", "C")
    min_length: int
        A minimum length for the sequence string to exceed
    Returns
    -------
    bool
        The sequence string is validated (True) else (False)
    """
    seen_list = []
    seen = seen_list.append

    if len(sequence) > min_length and all(letter in letter_list for letter in sequence):
        if sequence not in seen_list:
            seen(sequence)
            return True
    else:
        return False


def create_palindrome_rows(
    header: List[str], palindromes: List[Palindrome]
) -> List[List[str]]:
    """
    Create a list of lists of strings

    Parameters
    ----------
    header: List[str]
        A list of strings (header for a markdon table)
    palindromes:List[Palidrome]
        a list of Palindrome objects
    Returns
    -------
    rows: List[List[str]]
        A list of lists of strings
    """
    rows = []
    rows.append(header)
    for palindrome in palindromes:
        rows.append(
            [palindrome["palindrome_seq"], str(palindrome["palindrome_length"])]
        )
    return rows


def create_k_mer_rows(header: List[str], kmers: List[tuple]) -> List[List[str]]:
    """
    Create a list of lists of strings

    Parameters
    ----------
    header: List[str]
        A list of strings
    kmers: List[tuples]
        A list of tuples
    Returns
    -------
    rows: List[List[str]]
        A list of lists of strings
    """
    rows = []
    rows.append(header)
    for k_mer in kmers:
        key, value = k_mer
        rows.append([key, str(value)])
    return rows


def generate_report(sequence_stats: SequenceStatistics, output_path: str) -> None:
    """
    Uses the MarkdonGenerator class to create a markdon document.

    Parameters
    ----------
    sequence_stats: SequenceStatistics

    output_path:str
        A path for a file tp save markdown document to

    Returns
    -------
        None
    """

    md = MarkdownGenerator()
    md.add_header("DNA Statistics Report")
    md.add_linebreak()
    md.add_text(f"Total number sequences = {sequence_stats['total_sequences_count']}")
    md.add_text(
        f"Total number invalid sequences = {sequence_stats['invalid_sequences_count']}"
    )

    md.add_text("Total nucleotide counts:")

    md.add_text(f"Adenine = {sequence_stats['total_adenine_count']}")
    md.add_text(f"Thymine = {sequence_stats['total_thymine_count']}")
    md.add_text(f"Guanine = {sequence_stats['total_guanine_count']}")
    md.add_text(f"Cytosine = {sequence_stats['total_cytosine_count']}")

    kmers_2_rows = create_k_mer_rows(
        header=["k_mer (k2)", "number"], kmers=sequence_stats["total_k_mer_count_2"]
    )
    md.add_table(kmers_2_rows)
    kmers_3_rows = create_k_mer_rows(
        header=["k_mer (k3)", "number"], kmers=sequence_stats["total_k_mer_count_3"]
    )
    md.add_table(kmers_3_rows)
    kmers_4_rows = create_k_mer_rows(
        header=["k_mer (k4)", "number"], kmers=sequence_stats["total_k_mer_count_4"]
    )
    md.add_table(kmers_4_rows)
    kmers_5_rows = create_k_mer_rows(
        header=["k_mer (k5)", "number"], kmers=sequence_stats["total_k_mer_count_5"]
    )
    md.add_table(kmers_5_rows)

    if len(sequence_stats["palindromes"]) > 0:
        md.add_text(
            f"Total palindromes over 20 base pairs = {len(sequence_stats['palindromes'])}"
        )
        longest_palindrome_length = 0
        longest_palindrome_seq = ""
        palindromes = sequence_stats["palindromes"]
        for palindrome in palindromes:
            if palindrome["palindrome_length"] > longest_palindrome_length:
                longest_palindrome_length = palindrome["palindrome_length"]
                longest_palindrome_seq = palindrome["palindrome_seq"]
        if longest_palindrome_length > 0:
            md.add_text(
                f"The longest palindrome was {longest_palindrome_length}(bp) and had a sequence of {longest_palindrome_seq}"
            )
            palindrome_rows = create_palindrome_rows(
                ["Palindrome sequence", "length(bp)"], palindromes
            )
            md.add_table(palindrome_rows)
    else:
        md.add_text("No palindromes over 20 base pairs were detected")
    md.save(output_path)
