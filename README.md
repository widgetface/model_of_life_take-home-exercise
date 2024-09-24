## Task

You are provided with a [dataset of 200 DNA sequences](https://github.com/learningmodeloflife/take-home-exercise/edit/main/dna_sequences.json), each 1000 base pairs long. Your task is to analyse these sequences and uncover any interesting patterns or properties. This should take between 15-60 minutes.

### **File Format**

The dataset is stored as a JSON file. Here is the general structure of the file:

```
{
    "num_sequences": 200,
    "sequence_length": 1000,
    "sequences": [
        "ATCG... (sequence 1)",
        "GCTA... (sequence 2)",
        ...
        "TACG... (sequence 200)"]
}

```

### Requirements

Implement a Python script to analyse the sequences. Your script should:

a. Calculate and report basic sequence statistics:

* Overall GC content distribution
* Dinucleotide frequencies
* b. Identify the top 5 most common k-mers (substrings) for k=3, 4, and 5

c. Detect any unusual patterns, such as:

* Palindromic sequences above 20 base pairs in length that include at least 3 of the four bases (A,C,T,G)
* Any other patterns you find interesting or unusual

d. Provide a brief summary of your findings, highlighting any sequences or patterns that stand out.

Your code should be well-commented and efficiently implemented.

Provide a brief (max 300 words) write-up of your approach and findings.

## Returning your exercise

Please return a python script and write-up file as markdown to [Wilna Oosthuyzen](wilna.oosthuyzen@ed.ac.uk) by **Thursday 3rd October 18:00 UTC**.
