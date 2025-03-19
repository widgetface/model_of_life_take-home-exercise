"""DNA Sequence analysis script

This script allows the user to load a provided DNA sequence dataset and
analyse those sequences for:

1. Number of each nucleotide (adenine, thymine, guanine, cytosine).

2. Identification of the top 5 most common k-mers for k=2, 3, 4, and 5.

3. Longest palindromic sequence of 20 base pairs or over.

4. Analysis of the longest "GC" and "AT" continuous sequences.

5. Aggregation of DNA sequence results for steps 1, 2, 3.

6. Generation of a simple markdown report.

The script relies of core Python libraries and doesn't require any
dependencies to be installed.
"""

import json
import os
from typing import List, TypedDict
from multiprocessing import Pool
from functools import partial
import time
from utils.sequence_utils import (
    count_k_mers,
    count_nucleotides,
    create_dna_sequence_record,
    generate_report,
    find_top_values,
    update_k_mer_counts,
    validate_sequence,
)

from utils.data_types import DNASequence, SequenceStatistics


# Constants
NUCLEOTIDE_LIST = {"A", "T", "G", "C"}
PALINDROME_MIN_LENGTH = 20
INDEX = 0
FILE_PATH = "./data/dna_sequences.json"
REPORT_FILE_PATH = "./report/dna_statistics_report.md"


# Using os.cpu_count() // 2 reduce load on system.
num_cores = os.cpu_count() // 2


class DNASequenceData(TypedDict):
    num_sequences: int
    sequence_length: int
    sequences: List[str]


def initialise_sequence_statistics() -> SequenceStatistics:
    """
    Creates a SequenceStatistics dict

    Returns
    -------
    SequenceStatistics

    """
    seq_stats = {
        "total_adenine_count": 0,
        "total_thymine_count": 0,
        "total_guanine_count": 0,
        "total_cytosine_count": 0,
        "total_sequences_count": 0,
        "invalid_sequences_count": 0,
        "total_k_mer_count_2": {},
        "total_k_mer_count_3": {},
        "total_k_mer_count_4": {},
        "total_k_mer_count_5": {},
        "palindromes": [],
        "dna_sequences": [],
    }
    return seq_stats


def load_sequences_file(file_path: str) -> DNASequenceData:
    """
    Loads a JSON file and parses a JSON (JavaScript Object Notation)
    string and converts it into a Python dictionary

    Parameters
    ----------
    file_path : str
        The file location.


    Returns
    -------
    DNASequenceData

    """
    with open(file_path) as f:
        data = json.load(f)
        return data


def process_data(sequence: str) -> DNASequence:
    """
    Analyses the DNA sequence

    Parameters
    ----------
    sequence : str
        The DNA sequence


    Returns
    -------
    DNASequenceData

    """
    nucleotide_counts = count_nucleotides(sequence=sequence)
    k_mers = {}

    k_mers["k_mer_n2_count"] = count_k_mers(sequence=sequence, number_nucleotides=2)

    k_mers["k_mer_n3_count"] = count_k_mers(sequence=sequence, number_nucleotides=3)

    k_mers["k_mer_n4_count"] = count_k_mers(sequence=sequence, number_nucleotides=4)

    k_mers["k_mer_n5_count"] = count_k_mers(sequence=sequence, number_nucleotides=5)

    return create_dna_sequence_record(
        id=INDEX + 1,
        nucleotide_counts=nucleotide_counts,
        sequence=sequence,
        min_length=PALINDROME_MIN_LENGTH,
        k_mers=k_mers,
    )


def process_data_parallel(data: List[str]):
    """
    Process DNA sequences. Uses multiprocessing.Pool
    to process all the sequences in a collection List[str]

    Parameters
    ----------
    data : List[str]
         A list of DNA sequences


    Returns
    -------
    List[DNASequenceData]

    """
    with Pool(processes=num_cores) as pool:
        results = pool.map(process_data, data)
    return results


def calculate_dna_sequence_statistics(
    data: List[DNASequence], total_count: int, invalid_count: int
) -> SequenceStatistics:
    """
    Aggregate DNA sequence data

    Parameters
    ----------
    data : List[DNASequence]
        A list of DNASequences


    Returns
    -------
    SequenceStatistics

    """
    seq_doc = initialise_sequence_statistics()
    seq_doc["total_sequences_count"] = total_count
    seq_doc["invalid_sequences_count"] = invalid_count

    for item in data:
        seq_doc["total_adenine_count"] += item.adenine_count
        seq_doc["total_thymine_count"] += item.thymine_count
        seq_doc["total_guanine_count"] += item.guanine_count
        seq_doc["total_cytosine_count"] += item.cytosine_count
        seq_doc["total_k_mer_count_2"] = update_k_mer_counts(
            seq_doc["total_k_mer_count_2"], item.k_mers["k_mer_n2_count"]
        )
        seq_doc["total_k_mer_count_3"] = update_k_mer_counts(
            seq_doc["total_k_mer_count_3"], item.k_mers["k_mer_n3_count"]
        )
        seq_doc["total_k_mer_count_4"] = update_k_mer_counts(
            seq_doc["total_k_mer_count_4"], item.k_mers["k_mer_n4_count"]
        )
        seq_doc["total_k_mer_count_5"] = update_k_mer_counts(
            seq_doc["total_k_mer_count_5"], item.k_mers["k_mer_n5_count"]
        )
        if item.palindrome["palindrome_length"] > PALINDROME_MIN_LENGTH:
            seq_doc["palindromes"].append(item.palindrome)
        seq_doc["dna_sequences"].append(item)

    seq_doc["total_k_mer_count_2"] = find_top_values(seq_doc["total_k_mer_count_2"], 5)
    seq_doc["total_k_mer_count_3"] = find_top_values(seq_doc["total_k_mer_count_3"], 5)
    seq_doc["total_k_mer_count_4"] = find_top_values(seq_doc["total_k_mer_count_4"], 5)
    seq_doc["total_k_mer_count_5"] = find_top_values(seq_doc["total_k_mer_count_5"], 5)
    return seq_doc


if __name__ == "__main__":
    sequence_data = load_sequences_file(FILE_PATH)
    validate_partial = partial(
        validate_sequence, letter_list=NUCLEOTIDE_LIST, min_length=2
    )
    validate = validate_partial
    cleaned_sequence_data = [
        seq for seq in sequence_data["sequences"] if validate(sequence=seq)
    ]

    total_count = sequence_data["num_sequences"]
    invalid_count = total_count - len(cleaned_sequence_data)

    start_time = time.time()
    results = process_data_parallel(cleaned_sequence_data)

    seq_statistics = calculate_dna_sequence_statistics(
        data=results, total_count=total_count, invalid_count=invalid_count
    )
    generate_report(sequence_stats=seq_statistics, output_path=REPORT_FILE_PATH)

    #  print("Time taken to run analysis:", time.time() - start_time)
